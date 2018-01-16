import numpy as np


from clause import Clause, Question
from actions import *


class Task(object):

    def __init__(self, num_questions=5, exit_prob=1., informant_prob=1., search_prob=1., test_cond='first order'):
        self.search_prob = search_prob
        self.exit_inform_probs = [1 - exit_prob, exit_prob*(1 - informant_prob), exit_prob*informant_prob]
        #self.theory_of_mind_test_prob = theory_of_mind_test_prob
        self.test_cond = test_cond
        assert sum(self.exit_inform_probs) == 1
        self.num_questions = num_questions

    def generate_story(self, world, knowledge):
        raise NotImplementedError("Abstract method.")


class ActionsBeliefsTask(Task):

    def generate_story(self, world, knowledge):

        story = []

        actors = world.get_actors()
        locations = world.get_locations()
        objects = world.get_objects()
        containers = world.get_containers()

        num_questions = 0

        while num_questions < self.num_questions:

            idx_support = []
            clauses = []

            random_actors = np.random.choice(actors, size=3, replace=False)
            random_location = np.random.choice(locations)
            random_object = np.random.choice(objects)

            # whether or not the person will maintain a false belief
            exit_enter = np.random.choice([0, 1, 2], p=self.exit_inform_probs)

            # Whether to include the search clause
            do_search = np.random.choice([True, False], p=[self.search_prob, 1 - self.search_prob])

            # Whether to test for theory of mind
            #theory_of_mind_test = np.random.choice([True, False], p=[self.theory_of_mind_test_prob, 1 - self.theory_of_mind_test_prob])
            test_cond = self.test_cond

            if do_search:
                random_containers = np.random.choice(containers, size=3, replace=False)
            else:
                random_containers = np.random.choice(containers, size=2, replace=False)

            if do_search:

                # Person A searches for the item somewhere
                clauses.append(
                    Clause(
                        world,
                        True,
                        [1, 2],
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
                    [1, 2],
                    random_actors[0],
                    PlaceAction(),
                    random_object,
                    random_containers[0],
                )
            )

            if exit_enter == 1 or exit_enter == 2:

                # Support is "placed" clause
                idx_support += [len(story) + len(clauses) - 1]

                # Person A exits the location
                clauses.append(
                    Clause(
                        world,
                        True,
                        [1, 2],
                        random_actors[0],
                        ExitAction(),
                        random_location,
                    )
                )

            else:

                # Support is "moved" clause
                idx_support += [len(story) + len(clauses)]

            # Person B moves the item from container X to container Y
            clauses.append(
                Clause(
                    world,
                    True,
                    [1] if exit_enter == 1 or exit_enter == 2 else [1, 2],
                    random_actors[1],
                    TransportAction(),
                    random_object,
                    random_containers[0],
                    random_containers[1],
                )
            )

            if exit_enter == 2:

                # Person A is informed
                clauses.append(
                    Clause(
                        world,
                        True,
                        [2],
                        random_actors[2],
                        InformLocationAction(),
                        random_actors[0],
                        random_object,
                        random_containers[1]
                    )
                )

            if exit_enter == 1 or exit_enter == 2:

                # Person A re-enters the location
                clauses.append(
                    Clause(
                        world,
                        True,
                        [1, 2],
                        random_actors[0],
                        EnterAction(),
                        random_location,
                    )
                )

            # Update the state of the world
            for clause in clauses:
                #clause.perform() # TODO
                pass
            story.extend(clauses)

            if test_cond == 'first order':

                believe_loc = random_containers[0] if exit_enter == 1 else random_containers[1]

                # question: where does person A believe is the item?
                story.append(
                    Question(
                        idx_support,
                        random_actors[0],
                        BelieveLocationAction(),
                        random_object,
                        believe_loc,
                    )
                )

            elif test_cond == 'second order':

                believe_loc = random_containers[1] if exit_enter == 0 else random_containers[0]

                # question: where does person B think that A believes the item is?
                story.append(
                    Question(
                        idx_support,
                        random_actors[1],
                        BelieveAgentBelieveLocationAction(),
                        random_actors[0],
                        random_object,
                        believe_loc,
                    )
                )

            elif test_cond == 'reality':

                loc = random_containers[1]

                # question: where does person B think that A will search for the item?
                story.append(
                    Question(
                        idx_support,
                        random_object,
                        Exist(),
                        loc,
                    )
                )

            elif test_cond == 'memory':

                loc = random_containers[0]

                # question: where does person B think that A will search for the item?
                story.append(
                    Question(
                        idx_support,
                        random_object,
                        ExistBeginning(),
                        loc,
                    )
                )

            else:
                raise NotImplementedError

            num_questions += 1

        return story


class BeliefsActionsTask(Task):

    def generate_story(self, world, knowledge):

        story = []

        actors = world.get_actors()
        locations = world.get_locations()
        objects = world.get_objects()
        containers = world.get_containers()

        num_questions = 0

        while num_questions < self.num_questions:

            idx_support = []
            clauses = []

            random_actors = np.random.choice(actors, size=3, replace=False)
            random_location = np.random.choice(locations)
            random_object = np.random.choice(objects)
            random_containers = np.random.choice(containers, size=2, replace=False)

            # whether or not the person will maintain a false belief
            exit_enter = np.random.choice([0, 1, 2], p=self.exit_inform_probs)

            # Whether to test for theory of mind
            #theory_of_mind_test = np.random.choice([True, False], p=[self.theory_of_mind_test_prob, 1 - self.theory_of_mind_test_prob])
            test_cond = self.test_cond

            if exit_enter == 1 or exit_enter == 2:

                # Person A believes a false state of affairs
                clauses.append(
                    Clause(
                        world,
                        True,
                        [2],
                        random_actors[0],
                        BelieveLocationAction(),
                        random_object,
                        random_containers[0]
                    )
                )

                # Support is false "belief" clause
                idx_support += [len(story) + len(clauses) - 1]

                # Person A exits the location
                clauses.append(
                    Clause(
                        world,
                        True,
                        [1, 2],
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
                    [1] if exit_enter in [1, 2] else [1, 2],
                    random_actors[1],
                    TransportAction(),
                    random_object,
                    random_containers[0],
                    random_containers[1]
                )
            )

            if exit_enter == 2:

                # Person A is informed
                clauses.append(
                    Clause(
                        world,
                        True,
                        [2],
                        random_actors[2],
                        InformLocationAction(),
                        random_actors[0],
                        random_object,
                        random_containers[1]
                    )
                )

            if exit_enter == 1 or exit_enter == 2:

                # Person A re-enters the location
                clauses.append(
                    Clause(
                        world,
                        True,
                        [1, 2],
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
                        [2],
                        random_actors[0],
                        BelieveLocationAction(),
                        random_object,
                        random_containers[1]
                    )
                )

                # Support is true "belief" clause
                idx_support += [len(story) + len(clauses) - 1]

            # Update the state of the world
            for clause in clauses:
                #clause.perform() # TODO
                pass
            story.extend(clauses)

            # Clause: where does person A seach for the item?
            #if not theory_of_mind_test:
            if test_cond == 'first order':

               believe_loc = random_containers[0] if exit_enter == 1 else random_containers[1]

               # question: where does person A search for the item?
               story.append(
                   Question(
                       idx_support,
                       random_actors[0],
                       SearchAction(),
                       random_object,
                       believe_loc,
                   )
               )

            elif test_cond == 'second order':

                believe_loc = random_containers[1] if exit_enter == 0 else random_containers[0]

                # question: where does person B think that A will search for the item?
                story.append(
                    Question(
                        idx_support,
                        random_actors[1],
                        BelieveAgentSearchLocationAction(),
                        random_actors[0],
                        random_object,
                        believe_loc,
                    )
                )

            elif test_cond == 'reality':

                loc = random_containers[1]

                # question: where does person B think that A will search for the item?
                story.append(
                    Question(
                        idx_support,
                        random_object,
                        Exist(),
                        loc,
                    )
                )

            elif test_cond == 'memory':

                loc = random_containers[0]

                # question: where does person B think that A will search for the item?
                story.append(
                    Question(
                        idx_support,
                        random_object,
                        ExistBeginning(),
                        loc,
                    )
                )

            else:
                raise NotImplementedError

            num_questions += 1

        return story


class ActionsBeliefsActionsTask(Task):

    def generate_story(self, world, knowledge):

        story = []

        actors = world.get_actors()
        locations = world.get_locations()
        objects = world.get_objects()
        containers = world.get_containers()

        num_questions = 0

        while num_questions < self.num_questions:

            idx_support = []
            clauses = []

            random_actors = np.random.choice(actors, size=3, replace=False)
            random_location = np.random.choice(locations)
            random_object = np.random.choice(objects)
            random_containers = np.random.choice(containers, size=2, replace=False)

            # whether or not the person will maintain a false belief
            exit_enter = np.random.choice([0, 1, 2], p=self.exit_inform_probs)

            # Whether to test for theory of mind
            #theory_of_mind_test = np.random.choice([True, False], p=[self.theory_of_mind_test_prob, 1 - self.theory_of_mind_test_prob])
            test_cond = self.test_cond

            # person A drops the item in container X
            clauses.append(
                Clause(world,
                    True,
                    [1, 2],
                    random_actors[0],
                    PlaceAction(),
                    random_object,
                    random_containers[0]
                )
            )

            if exit_enter in [1, 2]:

                # Support is "placed" clause
                idx_support += [len(story) + len(clauses) - 1]

                # person A exits the location
                clauses.append(
                    Clause(world,
                        True,
                        [1, 2],
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
                    [1] if exit_enter in [1, 2] else [1, 2],
                    random_actors[1],
                    TransportAction(),
                    random_object,
                    random_containers[0],
                    random_containers[1]
                )
            )

            if exit_enter == 2:

                # Person A is informed
                clauses.append(
                    Clause(
                        world,
                        True,
                        [2],
                        random_actors[2],
                        InformLocationAction(),
                        random_actors[0],
                        random_object,
                        random_containers[1]
                    )
                )

            if exit_enter in [1, 2]:

                # person A re-enters the location
                clauses.append(
                    Clause(
                        world,
                        True,
                        [1, 2],
                        random_actors[0],
                        EnterAction(),
                        random_location
                    )
                )

            else:
                
                # Support is "transported" clause
                idx_support += [len(story) + len(clauses) - 1]

            # Update the state of the world
            for clause in clauses:
                #clause.perform() # TODO
                pass
            story.extend(clauses)

            # Question
            if test_cond == 'first order':

               believe_loc = random_containers[0] if exit_enter == 1 else random_containers[1]

               # question: where does person A search for the item?
               story.append(
                   Question(
                       idx_support,
                       random_actors[0],
                       SearchAction(),
                       random_object,
                       believe_loc,
                   )
               )

            elif test_cond == 'second order':

                believe_loc = random_containers[1] if exit_enter == 0 else random_containers[0]

                # question: where does person B think that A believes the item is?
                story.append(
                    Question(
                        idx_support,
                        random_actors[1],
                        BelieveAgentSearchLocationAction(),
                        random_actors[0],
                        random_object,
                        believe_loc,
                    )
                )

            elif test_cond == 'reality':

                loc = random_containers[1]

                # question: where does person B think that A will search for the item?
                story.append(
                    Question(
                        idx_support,
                        random_object,
                        Exist(),
                        loc,
                    )
                )

            elif test_cond == 'memory':

                loc = random_containers[0]

                # question: where does person B think that A will search for the item?
                story.append(
                    Question(
                        idx_support,
                        random_object,
                        ExistBeginning(),
                        loc,
                    )
                )

            else:
                raise NotImplementedError

            num_questions += 1

        return story
