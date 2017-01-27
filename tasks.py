import numpy as np


from clause import Clause, Question
from actions import *


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

            idx_support = []
            clauses = []

            random_actors = np.random.choice(actors, size=2, replace=False)
            random_location = np.random.choice(locations)
            random_object = np.random.choice(objects)

            # whether or not the person will maintain a false belief
            exit_enter = np.random.choice([True, False], p=[self.exit_prob, 1 - self.exit_prob])

            do_search = np.random.choice([True, False], p=[self.search_prob, 1 - self.search_prob])

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

            if exit_enter:

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
                    [1] if exit_enter else [1, 2],
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

            if exit_enter:

                # question: where does person A believe is the item?
                story.append(
                    Question(
                        idx_support,
                        random_actors[0],
                        BelieveLocationAction(),
                        random_object,
                        random_containers[0],
                    )
                )

            else:

                # question: where does person A believe is the item?
                story.append(
                    Question(
                        idx_support,
                        random_actors[0],
                        BelieveLocationAction(),
                        random_object,
                        random_containers[1],
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

            idx_support = []
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
                    [1] if exit_enter else [1, 2],
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
            if exit_enter:

                story.append(
                    Question(
                        idx_support,
                        random_actors[0],
                        SearchAction(),
                        random_object,
                        random_containers[0],
                    )
                )

            else:

                story.append(
                    Question(
                        idx_support,
                        random_actors[0],
                        SearchAction(),
                        random_object,
                        random_containers[1],
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

            idx_support = []
            clauses = []

            random_actors = np.random.choice(actors, size=2, replace=False)
            random_location = np.random.choice(locations)
            random_object = np.random.choice(objects)
            random_containers = np.random.choice(containers, size=2, replace=False)

            # whether or not the person will maintain a false belief
            exit_enter = np.random.choice([True, False], p=[self.exit_prob, 1 - self.exit_prob])

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

            if exit_enter:

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
                    [1] if exit_enter else [1, 2],
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

            if exit_enter:

                # question: where does person A seach for the item?
                story.append(
                    Question(
                        idx_support,
                        random_actors[0],
                        SearchAction(),
                        random_object,
                        random_containers[0],
                    )
                )

            else:

                # question: where does person A seach for the item?
                story.append(
                    Question(
                        idx_support,
                        random_actors[0],
                        SearchAction(),
                        random_object,
                        random_containers[1],
                    )
                )

            num_questions += 1

        return story
