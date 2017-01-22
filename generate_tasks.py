import argparse
import logging
import numpy as np
import os
import sys


from classes import \
    ActionsBeliefsTask, \
    BeliefsActionsTask, \
    ActionsBeliefsActionsTask, \
    World, \
    stringify
from utils import is_file, mkdir_p, remove_extension


def generate_sally_anne_tasks(world_paths,
                              output_dir_path,
                              num_stories_choices,
                              exit_prob_choices,
                              search_prob_choices,
                             ):

    mkdir_p(output_dir_path)

    for world in world_paths:

        w = World()
        w.load(world)
        world_name = remove_extension(world)

        for num_stories in num_stories_choices:
            for exit_prob in exit_prob_choices:
                for search_prob in search_prob_choices:

                    folder_name = '%s_nex_%d_exitp_%.2f_searchp_%.2f' % (world_name, num_stories, exit_prob, search_prob)

                    logging.info("Creating Sally-Anne task in %s..." % folder_name)
                    mkdir_p(os.path.join(output_dir_path, folder_name))

                    # AB
                    filename = 'qa1_task_AB_train.txt'
                    tasks = [
                        ActionsBeliefsTask,
                    ]
                    story = []

                    i = 0
                    while i < num_stories:
                        task = np.random.choice(tasks)
                        story.extend(
                            stringify(task(exit_prob=exit_prob, search_prob=search_prob).generate_story(w, None))
                        )
                        i += 1
                    story = '\n'.join(story)

                    with open(os.path.join(output_dir_path, folder_name, filename), 'w') as f:
                        f.write(story)

                    # BA
                    filename = 'qa2_task_BA_train.txt'
                    tasks = [
                        BeliefsActionsTask,
                    ]
                    story = []

                    i = 0
                    while i < num_stories:
                        task = np.random.choice(tasks)
                        story.extend(
                            stringify(task(exit_prob=exit_prob, search_prob=search_prob).generate_story(w, None))
                        )
                        i += 1
                    story = '\n'.join(story)

                    with open(os.path.join(output_dir_path, folder_name, filename), 'w') as f:
                        f.write(story)

                    # ABA
                    filename = 'qa3_task_ABA_train.txt'
                    tasks = [
                        ActionsBeliefsActionsTask,
                    ]
                    story = []

                    i = 0
                    while i < num_stories:
                        task = np.random.choice(tasks)
                        story.extend(
                            stringify(task(exit_prob=exit_prob, search_prob=search_prob).generate_story(w, None))
                        )
                        i += 1
                    story = '\n'.join(story)

                    with open(os.path.join(output_dir_path, folder_name, filename), 'w') as f:
                        f.write(story)

                    # AB + BA
                    filename = 'qa4_task_AB_BA_train.txt'
                    tasks = [
                        ActionsBeliefsTask,
                        BeliefsActionsTask,
                    ]
                    story = []

                    i = 0
                    while i < num_stories:
                        task = np.random.choice(tasks)
                        story.extend(
                            stringify(task(exit_prob=exit_prob, search_prob=search_prob).generate_story(w, None))
                        )
                        i += 1
                    story = '\n'.join(story)

                    with open(os.path.join(output_dir_path, folder_name, filename), 'w') as f:
                        f.write(story)

                    # AB + BA + ABA
                    filename = 'qa5_task_AB_BA_ABA_train.txt'
                    tasks = [
                        ActionsBeliefsTask,
                        BeliefsActionsTask,
                        ActionsBeliefsActionsTask,
                    ]
                    story = []

                    i = 0
                    while i < num_stories:
                        task = np.random.choice(tasks)
                        story.extend(
                            stringify(task(exit_prob=exit_prob, search_prob=search_prob).generate_story(w, None))
                        )
                        i += 1
                    story = '\n'.join(story)

                    with open(os.path.join(output_dir_path, folder_name, filename), 'w') as f:
                        f.write(story)

                    # Test
                    tasks = [
                        ActionsBeliefsActionsTask,
                    ]
                    story = []

                    i = 0
                    while i < num_stories:
                        task = np.random.choice(tasks)
                        story.extend(
                            stringify(task(exit_prob=1.).generate_story(w, None))
                        )
                        i += 1
                    story = '\n'.join(story)

                    test_filenames = [
                        'qa1_task_AB_test.txt',
                        'qa2_task_BA_test.txt',
                        'qa3_task_ABA_test.txt',
                        'qa4_task_AB_BA_test.txt',
                        'qa5_task_AB_BA_ABA_test.txt',
                    ]
                    for fname in test_filenames:
                        with open(os.path.join(output_dir_path, folder_name, fname), 'w') as f:
                            f.write(story)

def parse_args(args):

    parser = argparse.ArgumentParser(description='Process command-line arguments.')

    parser.add_argument('-w', '--world_path', dest='world_paths', type=is_file,
                        required=True, action='append',
                        help='Path to a world definition file')

    parser.add_argument('-o', '--output_dir_path', dest='output_dir_path', type=mkdir_p,
                        default='data',
                        help='Output directory path')

    parser.add_argument('-l', '--logging', type=str, default='INFO', metavar='logging',
                        choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'],
                        help='Logging level')

    parser.add_argument('-n', '--num_stories', dest='num_stories_choices', type=int,
                        action='append', required=True,
                        help='Number of stories (examples) in a task)')

    # SALLY-ANNE TASK PARAMS
    parser.add_argument('-sa', '--sally_anne', dest='sally_anne', action='store_true',
                        help='Flag that enables generation of Sally-Anne tasks')

    parser.add_argument('-ps', '--prob_search', dest='search_prob_choices', type=float,
                        action='append',
                        help='Probability that a search will occur in Sally-Anne task type AB')

    parser.add_argument('-pe', '--prob_exit', dest='exit_prob_choices', type=float,
                        action='append',
                        help='Probability that an exit will occur in Sally-Anne training tasks, all types')

    parsed = parser.parse_args(args)

    if parsed.sally_anne is True and parsed.search_prob_choices is None or parsed.exit_prob_choices is None:
        raise argparse.ArgumentTypeError("Parameters undefined for the Sally-Anne task.")

    return parsed


def main(args=sys.argv[1:]):

    args = parse_args(args)
    logging.basicConfig(level=args.logging, format='%(asctime)s\t%(levelname)-8s\t%(message)s')

    if args.sally_anne is True:
        generate_sally_anne_tasks(args.world_paths,
                                  os.path.join(args.output_dir_path, 'sally_anne'),
                                  args.num_stories_choices,
                                  args.search_prob_choices,
                                  args.exit_prob_choices,
                                 )


if __name__ == "__main__":
    sys.exit(main())
