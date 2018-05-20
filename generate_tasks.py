"""python generate_tasks.py -sa -w worlds/world_tiny.txt -w worlds/world_small.txt -w worlds/world_large.txt -n 1000 -n 10000 -ps 0. -ps .5 -ps 1. -pe 0. -pe .5 -pe 1."""
import argparse
import logging
import glob
import numpy as np
import os
import sys
import random
import itertools


from stringify import stringify
from tasks import \
    All_Tasks, \
    Specify_Tasks
#from reorder_tasks import Specify_Tasks_Reorder
from utils import is_file, mkdir_p, remove_extension
from world import World

def generate_tasks_with_oracle_fixed_count_old(world_paths, output_dir_path, n, noise=.1):
    """
    Generates stories with guarantee that
    each task is seen n times.
    """
    mkdir_p(output_dir_path)
    n = n[0] # TODO: remove

    for world in world_paths:

        w = World()
        w.load(world)
        world_name = remove_extension(world)

        task = Specify_Tasks()

        folder_name = '%s_nex_%d_%d' % (world_name, n, noise*100)
        logging.info("Creating New task in %s..." % folder_name)
        mkdir_p(os.path.join(output_dir_path, folder_name))

        with open(os.path.join(output_dir_path, folder_name, 'qa21_task_AB_train.txt'), 'w') as f:
            stories = []

            # generate all combinations of tasks and questions
            tasks = ['tb', 'fb', 'sofb']
            questions = ['memory', 'reality', 'search', 'belief']
            task_questions = list(itertools.product(tasks, questions)) * n
            random.shuffle(task_questions)

            # fixed to 5 per story
            for ts, qs in task_questions:
                noise_ts = np.random.choice(['tb', 'fb', 'sofb'], 4).tolist()
                noise_qs = np.random.choice(questions, 4).tolist()
                story = task.generate_story(w, 5, tasks=noise_ts+[ts], questions=noise_qs+[qs], num_agents=4, num_locations=6)
                f.write('\n'.join(stringify(story)))
                f.write('\n')

        with open(os.path.join(output_dir_path, folder_name, 'true_belief_val_test.txt'), 'w') as f:
            stories = []

            for i in range(n):

                story = task.generate_story(w, 4, ['tb']*4, questions, num_agents=4, num_locations=6, statement_noise=noise)
                f.write('\n'.join(stringify(story)))
                f.write('\n')
        with open(os.path.join(output_dir_path, folder_name, 'false_belief_val_test.txt'), 'w') as f:
            stories = []
            for i in range(n):

                story = task.generate_story(w, 4, ['fb']*4, questions, num_agents=4, num_locations=6, statement_noise=noise)
                f.write('\n'.join(stringify(story)))
                f.write('\n')

        with open(os.path.join(output_dir_path, folder_name, 'sofb_val_test.txt'), 'w') as f:
            stories = []
            for i in range(n):

                story = task.generate_story(w, 4, ['sofb']*4, questions, num_agents=4, num_locations=6, statement_noise=noise)
                f.write('\n'.join(stringify(story)))
                f.write('\n')

        with open(os.path.join(output_dir_path, folder_name, 'true_belief_test.txt'), 'w') as f:
            stories = []

            for i in range(n):

                story = task.generate_story(w, 4, ['tb']*4, questions, num_agents=4, num_locations=6, statement_noise=noise)
                f.write('\n'.join(stringify(story)))
                f.write('\n')

        with open(os.path.join(output_dir_path, folder_name, 'false_belief_test.txt'), 'w') as f:
            stories = []
            for i in range(n):

                story = task.generate_story(w, 4, ['fb']*4, questions, num_agents=4, num_locations=6, statement_noise=noise)
                f.write('\n'.join(stringify(story)))
                f.write('\n')

        with open(os.path.join(output_dir_path, folder_name, 'sofb_test.txt'), 'w') as f:
            stories = []
            for i in range(n):

                story = task.generate_story(w, 4, ['sofb']*4, questions, num_agents=4, num_locations=6, statement_noise=noise)
                f.write('\n'.join(stringify(story)))
                f.write('\n')


def generate_tasks_with_oracle_fixed_count(world_paths, output_dir_path, n, noise=.1):
    """
    Generates stories with guarantee that
    each task is seen n times.
    """
    mkdir_p(output_dir_path)
    n = n[0] # TODO: remove

    for world in world_paths:

        w = World()
        w.load(world)
        world_name = remove_extension(world)

        task = Specify_Tasks()
        
        folder_name = '%s_nex_%d_%d' % (world_name, n, noise*100)
        logging.info("Creating New task in %s..." % folder_name)
        mkdir_p(os.path.join(output_dir_path, folder_name))
        
        tasks = ['tb', 'fb', 'sofb']
        questions = ['memory', 'reality', 'search', 'belief']
        with open(os.path.join(output_dir_path, folder_name, 'qa21_task_AB_train.txt'), 'w') as f:
            stories = []
            
            # generate all combinations of tasks and questions
            task_questions = list(itertools.product(tasks, questions)) * n
            random.shuffle(task_questions)
            
            # fixed to 5 per story
            for k in zip(*[iter(task_questions)]*5):
                ts, qs = zip(*k)
                story = task.generate_story(w, 5, tasks=ts, questions=qs, num_agents=4, num_locations=6)
                f.write('\n'.join(stringify(story)))
                f.write('\n')
            """
            # fixed to 5 per story
            for ts, qs in task_questions:
                noise_ts = np.random.choice(['tb', 'fb', 'sofb'], 4).tolist()
                noise_qs = np.random.choice(questions, 4).tolist()
                story = task.generate_story(w, 5, tasks=noise_ts+[ts], questions=noise_qs+[qs], num_agents=4, num_locations=6)
                f.write('\n'.join(stringify(story)))
                f.write('\n')
            """
        #task = Specify_Tasks_Reorder()
        for task_type, question, data_set in itertools.product(tasks, questions, ['val', 'test']):

            path = '%s_%s_%s_test.txt' % (task_type, question, data_set)

            with open(os.path.join(output_dir_path, folder_name, path), 'w') as f:
                stories = []

                for i in range(n):
    
                    story = task.generate_story_qs_at_end(w, 4, [task_type]*4, [question], num_agents=4, num_locations=6, statement_noise=noise)
                    f.write('\n'.join(stringify(story)))
                    f.write('\n')
 
def generate_tasks_with_oracle_fixed_count_1_task_1_story(world_paths, output_dir_path, n, noise=.1):
    """
    Generates stories with guarantee that
    each task is seen n times.
    """
    mkdir_p(output_dir_path)
    n = n[0] # TODO: remove

    for world in world_paths:

        w = World()
        w.load(world)
        world_name = remove_extension(world)

        task = Specify_Tasks()

        folder_name = '%s_nex_%d_%d' % (world_name, n, noise*100)
        logging.info("Creating New task in %s..." % folder_name)
        mkdir_p(os.path.join(output_dir_path, folder_name))

        tasks = ['tb', 'fb', 'sofb']
        questions = ['memory', 'reality', 'search', 'belief']
        with open(os.path.join(output_dir_path, folder_name, 'qa21_task_AB_train.txt'), 'w') as f:
            stories = []

            # generate all combinations of tasks and questions
            task_questions = list(itertools.product(tasks, questions)) * n
            random.shuffle(task_questions)

            # fixed to 5 per story
            for ts, qs in task_questions:
                story = task.generate_story(w, 1, tasks=[ts], questions=[qs], num_agents=4, num_locations=6)
                f.write('\n'.join(stringify(story)))
                f.write('\n')

        #task = Specify_Tasks_Reorder()
        for task_type, question, data_set in itertools.product(tasks, questions, ['val', 'test']):

            path = '%s_%s_%s_test.txt' % (task_type, question, data_set)

            with open(os.path.join(output_dir_path, folder_name, path), 'w') as f:
                stories = []

                for i in range(n):

                    story = task.generate_story(w, 1, [task_type], [question], num_agents=4, num_locations=6, statement_noise=noise)
                    f.write('\n'.join(stringify(story)))
                    f.write('\n')
   
def generate_tasks_with_oracle_randomly(world_paths, output_dir_path, num_stories):

    mkdir_p(output_dir_path)
    num_stories = num_stories[0] # TODO: remove

    for world in world_paths:

        w = World()
        w.load(world)
        world_name = remove_extension(world)

        task = All_Tasks()
        
        folder_name = '%s_nex_%d' % (world_name, num_stories)
        logging.info("Creating New task in %s..." % folder_name)
        mkdir_p(os.path.join(output_dir_path, folder_name))
        
        with open(os.path.join(output_dir_path, folder_name, 'qa21_task_AB_train.txt'), 'w') as f:
            stories = []
            for i in range(num_stories):
                
                story = task.generate_story(w)
                #stories.extend(list(itertools.chain(*story)))
                f.write('\n'.join(stringify(story)))
                f.write('\n')
        
        with open(os.path.join(output_dir_path, folder_name, 'true_belief_test.txt'), 'w') as f:
            stories = []
            for i in range(num_stories):
                
                story = task.generate_story(w, task_dist=[1, 0, 0])
                #stories.extend(list(itertools.chain(*story)))
                f.write('\n'.join(stringify(story)))
                f.write('\n')
        
        with open(os.path.join(output_dir_path, folder_name, 'false_belief_test.txt'), 'w') as f:
            stories = []
            for i in range(num_stories):
                
                story = task.generate_story(w, task_dist=[0, 1, 0])
                #stories.extend(list(itertools.chain(*story)))
                f.write('\n'.join(stringify(story)))
                f.write('\n')
                
        with open(os.path.join(output_dir_path, folder_name, 'sofb_test.txt'), 'w') as f:
            stories = []
            for i in range(num_stories):
                
                story = task.generate_story(w, task_dist=[0, 0, 1])
                #stories.extend(list(itertools.chain(*story)))
                f.write('\n'.join(stringify(story)))
                f.write('\n')

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

    parser.add_argument('-pi', '--prob_informant', dest='informant_prob_choices', type=float,
                        action='append',
                        help='Probability that, given an exit occurred, that the agent who left will \
                        be informed about a change in the state of the world, \
                        in Sally-Anne training tasks, all types')

    parser.add_argument('-test', '--test_cond', dest='test_cond_choices',
                        choices=['first order', 'second order', 'reality', 'memory'],
                        action='append', required=True,
                        help='Types of test question')

    # ORACLE PARAMS
    parser.add_argument('-ptn', '--prob_test_noise', dest='test_noise', type=float,
                        required=True, help='Probability of encountering random noise sentence')

    parsed = parser.parse_args(args)

    if parsed.sally_anne is True and \
       parsed.search_prob_choices is None or \
       parsed.informant_prob_choices is None or \
       parsed.exit_prob_choices is None or \
       parsed.test_cond_choices is None:
        raise argparse.ArgumentTypeError("Parameters undefined for the Sally-Anne task.")

    return parsed


def main(args=sys.argv[1:]):

    args = parse_args(args)
    logging.basicConfig(level=args.logging, format='%(asctime)s\t%(levelname)-8s\t%(message)s')

    if args.sally_anne is True:
        generate_sally_anne_tasks(world_paths=args.world_paths,
                                  output_dir_path=os.path.join(args.output_dir_path, 'sally_anne'),
                                  babi_dir_path=args.babi_dir_path,
                                  num_stories_choices=args.num_stories_choices,
                                  exit_prob_choices=args.exit_prob_choices,
                                  search_prob_choices=args.search_prob_choices,
                                  informant_prob_choices=args.informant_prob_choices,
                                  test_cond_choices=args.test_cond_choices,
                                  )
    else:
         generate_tasks_with_oracle_fixed_count(world_paths=args.world_paths,
                           output_dir_path=os.path.join(args.output_dir_path, 'sally_anne'),
                           n=args.num_stories_choices,
                           noise=args.test_noise
                          )


if __name__ == "__main__":
    sys.exit(main())
