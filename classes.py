import numpy as np


class Action(object):

    def __init__(self, templates):
        self.templates = templates

    def render(self, *args):
        assert len(self.templates) > 0
        return np.random.choice(self.templates) % args


class PlaceAction(Action):

    def __init__(self):
        templates = [
            '%s placed the %s in the %s.',
            '%s put the %s in the %s.',
        ]
        super().__init__(templates)


class EvalPlaceAction(Action):

    def __init__(self):
        templates = [
            'Where did %s place the %s?\t%s',
            'Where did %s put the %s?\t%s',
        ]
        super().__init__(templates)

class SearchAction(Action):

    def __init__(self):
        templates = [
            '%s searched for the %s in the %s.',
            '%s looked for the %s in the %s.',
        ]
        super().__init__(templates)


class EvalSearchAction(Action):

    def __init__(self):
        templates = [
            'Where did %s search for the %s?\t%s',
            'Where did %s look for the %s?\t%s',
        ]
        super().__init__(templates)


class TransportAction(Action):

    def __init__(self):
        templates = [
            '%s shifted the %s from the %s to the %s.',
        ]
        super().__init__(templates)


class EnterAction(Action):

    def __init__(self):
        templates = [
            '%s entered the %s.',
            '%s came into the %s.',
        ]
        super().__init__(templates)


class ExitAction(Action):

    def __init__(self):
        templates = [
            '%s exited the %s.',
            '%s left the %s.',
            '%s went out of the %s.',
        ]
        super().__init__(templates)


class BelieveLocationAction(Action):

    def __init__(self):
        templates = [
            '%s thinks the %s is in the %s.',
            '%s believes the %s is in the %s.',
        ]
        super().__init__(templates)


class EvalBelieveLocationAction(Action):

    def __init__(self):
        templates = [
            'Where does %s think the %s is?\t%s',
            'Where does %s believe the %s is?\t%s',
        ]
        super().__init__(templates)


class Error(Exception):
    """Base class for exceptions in this module."""
    pass

class InputError(Error):
    """Exception raised for errors in the input.

    Attributes:
        expr # input expression in which the error occurred
        msg  # explanation of the error
    """

    def __init__(self, expr, msg):
        self.expr = expr
        self.msg = msg


class Entity(object):

    def __init__(self, name, properties):
        pass


class World(object):

    def __init__(self, world_actions=[], entities={}):

        self.actions = world_actions or False

        self.entities = entities or {}

        if not 'god' in self.entities:
            #self.create_entity('god', {'is_god': True})
            self.entities['god'] = {'is_god': True}

    def god(self):
        return self.entities['god']

    def load(self, fname):

        lines = open(fname, 'r').readlines()
        i = 0

        while i < len(lines):
            line = lines[i].rstrip('\n')
            if line != '' and not line.startswith('#'):
                #self:perform_command('god ' .. line)
                if line.startswith('create'):
                    self.entities[line.split(' ')[1]] = {}
                elif line.startswith('set'):
                    self.entities[line.split(' ')[1]][line.split(' ')[-1]] = True

            i += 1

    def perform_command(self, command):
        pass

    def perform_action(self, action, actor):
        pass

    def create_entity(self, id, properties, name=None):

        name = name or id

        if 'id' in self.entities:
            raise InputError(id, 'id already exists')

        self.entities[id] = Entity(name, properties)

        return self.entities[id]

    def get_entity(self, predicates):

        if not isinstance(predicates, list):
            raise InputError(predicates, 'is not a list.')

        return_val = []

        for k in self.entities:

            if all([predicate in self.entities[k] and self.entities[k][predicate] is True for predicate in predicates]):

                return_val += [k]


        return return_val

    def get_actors(self):
        return self.get_entity(['is_actor', 'is_god'])

    def get_locations(self):
        return self.get_entity(['is_location'])

    def get_objects(self):
        return self.get_entity(['is_thing', 'is_gettable'])

    def get_containers(self):
        return self.get_entity(['is_thing', 'is_container'])


class Clause(object):

    def __init__(self, world, truth_value, attend_to, actor, action, *args):

        self.world = world
        self.attend_to = attend_to
        self.truth_value = truth_value
        self.actor = actor
        self.action = action
        self.args = args

    def render(self):
        s = self.action.render(self.actor, *self.args)
        if self.attend_to:
            s += ' *'
        return s

    def is_valid(self):
        return self.action.is_valid(self.world, self.actor, *self.args)

    def perform(self):
        if self.truth_value:
            self.action.perform(self.world, self.actor, *self.args)

    def __eq__(self, other):
        return self.world == other.world and self.actor == other.actor and self.args == other.args

    def sample_valid(world, truth_values, actors, actions, *args, retries=100):

        for _ in range(retries):

            truth_value = np.random.choice(truth_values)
            actor = np.random.choice(actors)
            action = np.random.choice(actions)

            args = []

            raise NotImplementedError #TODO


class Task(object):

    def __init__(self, world):

        assert isinstance(world, World)
        self.world = world

    def generate_story(self, world, knowledge):
        raise NotImplementedError("Abstract method.")


class ActionsBeliefsTask(Task):

    def __init__(self, exit_prob=1., num_questions=5, search_prob=1.):
        self.search_prob = search_prob
        self.exit_prob = exit_prob
        self.num_questions = num_questions

    def generate_story(self, world, knowledge):

        story = []

        actors = world.get_actors()
        locations = world.get_locations()
        objects = world.get_objects()
        containers = world.get_containers()

        num_questions = 0

        while num_questions < self.num_questions:

            clauses = []

            random_actors = np.random.choice(actors, size=2, replace=False)
            random_location = np.random.choice(locations)
            random_object = np.random.choice(objects)

            # whether or not the person will maintain a false belief
            exit_enter = np.random.choice([True, False], p=[self.exit_prob, 1 - self.exit_prob])

            do_search = np.random.choice([True, False], p=[self.search_prob, 1 - self.search_prob])

            random_containers = np.random.choice(containers, size=3, replace=False)

            if do_search:

                # Person A searches for the item somewhere
                clauses.append(
                    Clause(
                        world,
                        True,
                        False,
                        random_actors[0],
                        SearchAction(),
                        random_object,
                        random_containers[2],
                    )
                )

            clauses.append(
                Clause(
                    world,
                    True,
                    True,
                    random_actors[0],
                    PlaceAction(),
                    random_object,
                    random_containers[0],
                )
            )

            if exit_enter:

                # Person A exits the location
                clauses.append(
                    Clause(
                        world,
                        True,
                        False,
                        random_actors[0],
                        ExitAction(),
                        random_location,
                    )
                )

            # Person B moves the item from container X to container Y
            clauses.append(
                Clause(
                    world,
                    True,
                    False,
                    random_actors[1],
                    TransportAction(),
                    random_object,
                    random_containers[0],
                    random_containers[1],
                )
            )

            if exit_enter:

                # Person A re-enters the location
                clauses.append(
                    Clause(
                        world,
                        True,
                        False,
                        random_actors[0],
                        EnterAction(),
                        random_location,
                    )
                )

            # Update the state of the world
            for clause in clauses:
                #clause:perform() # TODO
                pass
            story.extend(clauses)

            if exit_enter:

                # question: where does person A believe is the item?
                story.append(
                    Clause(
                        world,
                        True,
                        False,
                        random_actors[0],
                        EvalBelieveLocationAction(),
                        random_object,
                        random_containers[0]
                    )
                )

            else:

                # question: where does person A believe is the item?
                story.append(
                    Clause(
                        world,
                        True,
                        False,
                        random_actors[0],
                        EvalBelieveLocationAction(),
                        random_object,
                        random_containers[1]
                    )
                )

            num_questions += 1

        return story


class BeliefsActionsTask(Task):

    def __init__(self, exit_prob=1., num_questions=5, search_prob=1.):
        self.exit_prob = exit_prob
        self.num_questions = num_questions

    def generate_story(self, world, knowledge):

        story = []

        actors = world.get_actors()
        locations = world.get_locations()
        objects = world.get_objects()
        containers = world.get_containers()

        num_questions = 0

        while num_questions < self.num_questions:

            clauses = []

            random_actors = np.random.choice(actors, size=2, replace=False)
            random_location = np.random.choice(locations)
            random_object = np.random.choice(objects)
            random_containers = np.random.choice(containers, size=2, replace=False)

            # whether or not the person will maintain a false belief
            exit_enter = np.random.choice([True, False], p=[self.exit_prob, 1 - self.exit_prob])

            if exit_enter:

                # Person A believes a false state of affairs
                clauses.append(
                    Clause(
                        world,
                        True,
                        True,
                        random_actors[0],
                        BelieveLocationAction(),
                        random_object,
                        random_containers[0]
                    )
                )

                # Person A exits the location
                clauses.append(
                    Clause(
                        world,
                        True,
                        False,
                        random_actors[0],
                        ExitAction(),
                        random_location
                    )
                )

            # Person B moves the item from container X to container Y
            clauses.append(
                Clause(
                    world,
                    True,
                    False,
                    random_actors[1],
                    TransportAction(),
                    random_object,
                    random_containers[0],
                    random_containers[1]
                )
            )

            if exit_enter:

                # Person A re-enters the location
                clauses.append(
                    Clause(
                        world,
                        True,
                        False,
                        random_actors[0],
                        EnterAction(),
                        random_location
                    )
                )

            else:

                # Person A believes a True state of affairs
                clauses.append(
                    Clause(
                        world,
                        True,
                        True,
                        random_actors[0],
                        BelieveLocationAction(),
                        random_object,
                        random_containers[1]
                    )
                )
                
            # Update the state of the world
            for clause in clauses:
                #clause:perform() # TODO
                pass
            story.extend(clauses)

            # Clause: where does person A seach for the item?
            if exit_enter:

                story.append(
                    Clause(
                        world,
                        True,
                        False,
                        random_actors[0],
                        EvalSearchAction(),
                        random_object,
                        random_containers[0]
                    )
                )

            else:

                story.append(
                    Clause(
                        world,
                        True,
                        False,
                        random_actors[0],
                        EvalSearchAction(),
                        random_object,
                        random_containers[1]
                    )
                )

            num_questions += 1

        return story


class ActionsBeliefsActionsTask(Task):

    def __init__(self, exit_prob=1., num_questions=5, search_prob=1.):
        self.exit_prob = exit_prob
        self.num_questions = num_questions

    def generate_story(self, world, knowledge):

        story = []

        actors = world.get_actors()
        locations = world.get_locations()
        objects = world.get_objects()
        containers = world.get_containers()

        num_questions = 0

        while num_questions < self.num_questions:

            clauses = []

            random_actors = np.random.choice(actors, size=2, replace=False)
            random_location = np.random.choice(locations)
            random_object = np.random.choice(objects)
            random_containers = np.random.choice(containers, size=2, replace=False)

            # whether or not the person will maintain a false belief
            exit_enter = np.random.choice([True, False], p=[self.exit_prob, 1 - self.exit_prob])

            if exit_enter:
                attend_1 = True
            else:
                attend_1 = False

            # person A drops the item in container X
            clauses.append(
                Clause(world,
                    True,
                    attend_1,
                    random_actors[0],
                    PlaceAction(),
                    random_object,
                    random_containers[0]
                )
            )

            if exit_enter:

                # person A exits the location
                clauses.append(
                    Clause(world,
                        True,
                        False,
                        random_actors[0],
                        ExitAction(),
                        random_location
                    )
                )

            # person B moves the item from container X to container Y
            clauses.append(
                Clause(
                    world,
                    True,
                    not attend_1,
                    random_actors[1],
                    TransportAction(),
                    random_object,
                    random_containers[0],
                    random_containers[1]
                )
            )

            if exit_enter:

                # person A re-enters the location
                clauses.append(
                    Clause(
                        world,
                        True,
                        False,
                        random_actors[0],
                        EnterAction(),
                        random_location
                    )
                )

            # Update the state of the world
            for clause in clauses:
                #clause:perform() # TODO
                pass
            story.extend(clauses)

            if exit_enter:

                # question: where does person A seach for the item?
                story.append(
                    Clause(
                        world,
                        True,
                        False,
                        random_actors[0],
                        EvalSearchAction(),
                        random_object,
                        random_containers[0]
                    )
                )

            else:

                # question: where does person A seach for the item?
                story.append(
                    Clause(
                        world,
                        True,
                        False,
                        random_actors[0],
                        EvalSearchAction(),
                        random_object,
                        random_containers[1]
                    )
                )

            num_questions += 1

        return story


#def stringify(story, knowledge, config):
def stringify(story):

    lines = []

    i = 0  # The number of descriptions processed
    j = 0  # The number of lines output

    while True:

        line = story[i].render()

        # Prepend the number
        line = '%d %s' % (i+1, line)

        lines.append(line)

        # Keep track of where clauses were rendered
        #for k = i, i + template.clauses - 1 do
        #clause_lines[story[k]] = j
        #end

        # Increment counters
        #i = i + template.clauses #TODO
        i += 1
        j += 1

        if i >= len(story):
            break

    #lines = tablex.map(capitalize, lines)
    #lines = add_line_numbers(lines)

    return lines
