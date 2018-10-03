import argparse
import logging
import glob
import numpy as np
import os
import sys
import random
import itertools

from stringify import stringify
from tasks import Specify_Tasks
from utils import is_file, mkdir_p, remove_extension
from world import World

def generate_tasks_with_oracle_fixed_count(
    world_paths, output_dir_path, n, noise=.1, train_noise=False
):
    """Generates stories with guarantee that each task is seen n times."""

    mkdir_p(output_dir_path)
    n = n[0]

    for world in world_paths:

        # Load information from world
        w = World()
        w.load(world)
        world_name = remove_extension(world)

        # ----------------------------- TRAINING ----------------------------- #

        # Create folder to contain data
        folder_name = '%s_nex_%d_%d' % (world_name, n, noise*100)
        logging.info("Creating New task in %s..." % folder_name)
        mkdir_p(os.path.join(output_dir_path, folder_name))
        train_file_path = os.path.join(
            output_dir_path, folder_name, 'qa21_task_AB_train.txt'
        )
        
        # Define task creator and task types
        task = Specify_Tasks()
        tasks = ['tb', 'fb', 'sofb']
        questions = ['memory', 'reality', 'search', 'belief']

        with open(train_file_path, 'w') as f:
            stories = []
            
            # Generate all combinations of tasks and questions
            task_questions = list(itertools.product(tasks, questions)) * n
            random.shuffle(task_questions)

            # Pick 5 task, question combinations and generate story
            for k in zip(*[iter(task_questions)]*5):
                ts, qs = zip(*k)
                if train_noise:
                    story = task.generate_story(
                        w, 5, tasks=ts, questions=qs,
                        num_agents=4, num_locations=6, statement_noise=noise
                    )
                else:
                    story = task.generate_story(
                        w, 5, tasks=ts, questions=qs,
                        num_agents=4, num_locations=6
                    )
                f.write('\n'.join(stringify(story)))
                f.write('\n')


        # ---------------------------- VAL + TEST ---------------------------- #

        # Iterate through all testing conditions
        conds = itertools.product(tasks, questions, ['val', 'test'])
        for task_type, question, data_set in conds:

            fname = '%s_%s_%s_test.txt' % (task_type, question, data_set)
            full_file_path = os.path.join(output_dir_path, folder_name, fname)
            with open(full_file_path, 'w') as f:

                # Create story with questions at end
                stories = []
                for i in range(n):
                    story = task.generate_story_qs_at_end(
                        w, 4, [task_type]*4, [question], num_agents=4,
                        num_locations=6, statement_noise=noise
                    )
                    f.write('\n'.join(stringify(story)))
                    f.write('\n')
 
def generate_tasks_with_oracle_fixed_count_1_task_1_story(
    world_paths, output_dir_path, n, noise=.1, train_noise=False
):
    """Generates stories with guarantee that each task is seen n times."""
    mkdir_p(output_dir_path)
    n = n[0]

    for world in world_paths:

        w = World()
        w.load(world)
        world_name = remove_extension(world)

        # ----------------------------- TRAINING ----------------------------- #

        # Create folder to contain data
        folder_name = '%s_nex_%d_%d' % (world_name, n, noise*100)
        logging.info("Creating New task in %s..." % folder_name)
        mkdir_p(os.path.join(output_dir_path, folder_name))
        train_file_path = os.path.join(
            output_dir_path, folder_name, 'qa21_task_AB_train.txt'
        )

        # Define task creator and task types
        task = Specify_Tasks()
        tasks = ['tb', 'fb', 'sofb']
        questions = ['memory', 'reality', 'search', 'belief']
        
        with open(train_file_path, 'w') as f:
            
            # Generate all combinations of tasks and questions
            task_questions = list(itertools.product(tasks, questions)) * n
            random.shuffle(task_questions)
            import pdb; pdb.set_trace()

            # Create story for each task-question combo
            stories = []
            for ts, qs in task_questions:
                if train_noise:
                    story = task.generate_story(
                        w, 1, tasks=[ts], questions=[qs], num_agents=4,
                        num_locations=6, statement_noise=noise
                    )
                else:
                    story = task.generate_story(
                        w, 1, tasks=[ts], questions=[qs], num_agents=4,
                        num_locations=6
                    )
                f.write('\n'.join(stringify(story)))
                f.write('\n')

        # ---------------------------- VAL + TEST ---------------------------- #

        # Iterate through all testing conditions
        combo = itertools.product(tasks, questions, ['val', 'test'])
        for task_type, question, data_set in combo:

            fname = '%s_%s_%s_test.txt' % (task_type, question, data_set)
            path = os.path.join(output_dir_path, folder_name, fname)

            with open(path, 'w') as f:
                stories = []
                for i in range(n):
                    story = task.generate_story(
                        w, 1, [task_type], [question], num_agents=4,
                        num_locations=6, statement_noise=noise
                    )
                    f.write('\n'.join(stringify(story)))
                    f.write('\n')
   
def parse_args(args):

    parser = argparse.ArgumentParser(
        description='Process command-line arguments.'
    )

    parser.add_argument(
        '-w', '--world_path', dest='world_paths', type=is_file, required=True,
        action='append', help='Path to a world definition file'
    )

    parser.add_argument(
        '-o', '--output_dir_path', dest='output_dir_path', type=mkdir_p,
        default='data', help='Output directory path'
    )

    parser.add_argument(
        '-b', '--babi_dir_path', dest='babi_dir_path', type=str, required=True,
        help='Path to directory containing the 20 bAbi task train + test data'
    )

    parser.add_argument(
        '-l', '--logging', type=str, default='INFO', metavar='logging',
        choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'],
        help='Logging level'
    )

    parser.add_argument(
        '-n', '--num_stories', dest='num_stories_choices', type=int,
        action='append', required=True,
        help='Number of stories (examples) in a task)'
    )

    parser.add_argument(
        '-easy', '--easy', dest='easy', action='store_true',
        help='Switch on tom-easy generation'
    )

    parser.add_argument(
        '-test', '--test_cond', dest='test_cond_choices',
        choices=['first order', 'second order', 'reality', 'memory'],
        action='append', required=True, help='Types of test question'
    )

    parser.add_argument(
        '-ptn', '--prob_test_noise', dest='test_noise', type=float,
        required=True, help='Probability of encountering random noise sentence'
    )

    parser.add_argument(
        '-tn', '--train_noise', dest='train_noise', type=bool, default=False,
        help='Whether or not to include noise at training time'
    )

    parsed = parser.parse_args(args)

    return parsed


def main(args=sys.argv[1:]):

    args = parse_args(args)
    logging.basicConfig(
        level=args.logging, format='%(asctime)s\t%(levelname)-8s\t%(message)s'
    )

    if args.easy:
        generate_tasks_with_oracle_fixed_count_1_task_1_story(
            world_paths=args.world_paths,
            output_dir_path=os.path.join(args.output_dir_path, 'tom_easy'),
            n=args.num_stories_choices,
            noise=args.test_noise,
            train_noise=args.train_noise
        )
    else:
        generate_tasks_with_oracle_fixed_count(
            world_paths=args.world_paths,
            output_dir_path=os.path.join(args.output_dir_path, 'tom'),
            n=args.num_stories_choices,
            noise=args.test_noise,
            train_noise=args.train_noise
        )


if __name__ == "__main__":
    sys.exit(main())
