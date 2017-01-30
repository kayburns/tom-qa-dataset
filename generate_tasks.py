"""python generate_tasks.py -sa -w worlds/world_tiny.txt -w worlds/world_small.txt -w worlds/world_large.txt -n 1000 -n 10000 -ps 0. -ps .5 -ps 1. -pe 0. -pe .5 -pe 1."""
import argparse
import logging
import glob
import numpy as np
import os
import sys


from stringify import stringify
from tasks import \
    ActionsBeliefsTask, \
    BeliefsActionsTask, \
    ActionsBeliefsActionsTask
from utils import is_file, mkdir_p, remove_extension
from world import World


def generate_sally_anne_tasks(world_paths,
                              output_dir_path,
                              babi_dir_path,
                              num_stories_choices,
                              exit_prob_choices,
                              search_prob_choices,
                              num_questions=5,
                             ):

    mkdir_p(output_dir_path)

    for world in world_paths:

        w = World()
        w.load(world)
        world_name = remove_extension(world)

        # Test
        tasks = [
            ActionsBeliefsActionsTask,
        ]

        true_belief_test_story = []
        i = 0
        while i < np.max(num_stories_choices):
            task = np.random.choice(tasks)
            true_belief_test_story.append(
                '\n'.join(stringify(task(exit_prob=0.).generate_story(w, None)))
            )
            i += 1 * num_questions

        false_belief_test_story = []
        i = 0
        while i < np.max(num_stories_choices):
            task = np.random.choice(tasks)
            false_belief_test_story.append(
                '\n'.join(stringify(task(exit_prob=1.).generate_story(w, None)))
            )
            i += 1 * num_questions

        for num_stories in num_stories_choices:
            for exit_prob in exit_prob_choices:
                for search_prob in search_prob_choices:

                    folder_name = '%s_nex_%d_exitp_%.2f_searchp_%.2f' % (world_name, num_stories, exit_prob, search_prob)
                    logging.info("Creating Sally-Anne task in %s..." % folder_name)
                    mkdir_p(os.path.join(output_dir_path, folder_name))

                    # Symlink the bAbi data
                    babi_subdir = 'en' if num_stories < 5000 else 'en-10k'
                    for filepath in glob.glob(os.path.join(babi_dir_path, babi_subdir, '*train.txt')):
                        os.symlink(filepath, os.path.join(output_dir_path, folder_name, os.path.basename(filepath)))

                    # Write test
                    with open(os.path.join(output_dir_path, folder_name, 'true_belief_task_test.txt'), 'w') as f:
                        f.write('\n'.join(true_belief_test_story[:int(num_stories / num_questions)]))
                    with open(os.path.join(output_dir_path, folder_name, 'false_belief_task_test.txt'), 'w') as f:
                        f.write('\n'.join(false_belief_test_story[:int(num_stories / num_questions)]))

                    # AB
                    filename = 'qa21_task_AB_train.txt'
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
                        i += 1 * num_questions
                    story = '\n'.join(story)

                    with open(os.path.join(output_dir_path, folder_name, filename), 'w') as f:
                        f.write(story)

                    # BA
                    filename = 'qa22_task_BA_train.txt'
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
                        i += 1 * num_questions
                    story = '\n'.join(story)

                    with open(os.path.join(output_dir_path, folder_name, filename), 'w') as f:
                        f.write(story)

                    # ABA
                    filename = 'qa23_task_ABA_train.txt'
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
                        i += 1 * num_questions
                    story = '\n'.join(story)

                    with open(os.path.join(output_dir_path, folder_name, filename), 'w') as f:
                        f.write(story)

                    # AB + BA
                    filename = 'qa24_task_AB_BA_train.txt'
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
                        i += 1 * num_questions
                    story = '\n'.join(story)

                    with open(os.path.join(output_dir_path, folder_name, filename), 'w') as f:
                        f.write(story)

                    # AB + BA + ABA
                    filename = 'qa25_task_AB_BA_ABA_train.txt'
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
                        i += 1 * num_questions
                    story = '\n'.join(story)

                    with open(os.path.join(output_dir_path, folder_name, filename), 'w') as f:
                        f.write(story)


def parse_args(args):

    parser = argparse.ArgumentParser(description='Process command-line arguments.')

    parser.add_argument('-w', '--world_path', dest='world_paths', type=is_file,
                        required=True, action='append',
                        help='Path to a world definition file')

    parser.add_argument('-o', '--output_dir_path', dest='output_dir_path', type=mkdir_p,
                        default='data',
                        help='Output directory path')

    parser.add_argument('-b', '--babi_dir_path', dest='babi_dir_path', type=str,
                        required=True,
                        help='Path to directory containing the 20 bAbi task training and test data')

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
                                  args.babi_dir_path,
                                  args.num_stories_choices,
                                  args.search_prob_choices,
                                  args.exit_prob_choices,
                                 )


if __name__ == "__main__":
    sys.exit(main())
