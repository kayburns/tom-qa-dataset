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
                              informant_prob_choices,
                              test_cond_choices,
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

        true_belief_test_story_firstord = []
        i = 0
        while i < np.max(num_stories_choices):
            task = np.random.choice(tasks)
            true_belief_test_story_firstord.append(
                '\n'.join(stringify(task(exit_prob=0., test_cond='first order').generate_story(w)))
            )
            i += 1 * num_questions

        false_belief_test_story_firstord = []
        i = 0
        while i < np.max(num_stories_choices):
            task = np.random.choice(tasks)
            false_belief_test_story_firstord.append(
                '\n'.join(stringify(task(exit_prob=1., informant_prob=0., test_cond='first order').generate_story(w)))
            )
            i += 1 * num_questions

        false_false_belief_test_story_firstord = []
        i = 0
        while i < np.max(num_stories_choices):
            task = np.random.choice(tasks)
            false_false_belief_test_story_firstord.append(
                '\n'.join(stringify(task(exit_prob=1., informant_prob=1., test_cond='first order').generate_story(w)))
            )
            i += 1 * num_questions

        true_belief_test_story_secondord = []
        i = 0
        while i < np.max(num_stories_choices):
            task = np.random.choice(tasks)
            true_belief_test_story_secondord.append(
                '\n'.join(stringify(task(exit_prob=0., test_cond='second order').generate_story(w)))
            )
            i += 1 * num_questions

        false_belief_test_story_secondord = []
        i = 0
        while i < np.max(num_stories_choices):
            task = np.random.choice(tasks)
            false_belief_test_story_secondord.append(
                '\n'.join(stringify(task(exit_prob=1., informant_prob=0., test_cond='second order').generate_story(w)))
            )
            i += 1 * num_questions

        false_false_belief_test_story_secondord = []
        i = 0
        while i < np.max(num_stories_choices):
            task = np.random.choice(tasks)
            false_false_belief_test_story_secondord.append(
                '\n'.join(stringify(task(exit_prob=1., informant_prob=1., test_cond='second order').generate_story(w)))
            )
            i += 1 * num_questions

        true_belief_test_story_reality = []
        i = 0
        while i < np.max(num_stories_choices):
            task = np.random.choice(tasks)
            true_belief_test_story_reality.append(
                '\n'.join(stringify(task(exit_prob=0., test_cond='reality').generate_story(w)))
            )
            i += 1 * num_questions

        false_belief_test_story_reality = []
        i = 0
        while i < np.max(num_stories_choices):
            task = np.random.choice(tasks)
            false_belief_test_story_reality.append(
                '\n'.join(stringify(task(exit_prob=1., informant_prob=0., test_cond='reality').generate_story(w)))
            )
            i += 1 * num_questions

        false_false_belief_test_story_reality = []
        i = 0
        while i < np.max(num_stories_choices):
            task = np.random.choice(tasks)
            false_false_belief_test_story_reality.append(
                '\n'.join(stringify(task(exit_prob=1., informant_prob=1., test_cond='reality').generate_story(w)))
            )
            i += 1 * num_questions

        true_belief_test_story_memory = []
        i = 0
        while i < np.max(num_stories_choices):
            task = np.random.choice(tasks)
            true_belief_test_story_memory.append(
                '\n'.join(stringify(task(exit_prob=0., test_cond='memory').generate_story(w)))
            )
            i += 1 * num_questions

        false_belief_test_story_memory = []
        i = 0
        while i < np.max(num_stories_choices):
            task = np.random.choice(tasks)
            false_belief_test_story_memory.append(
                '\n'.join(stringify(task(exit_prob=1., informant_prob=0., test_cond='memory').generate_story(w)))
            )
            i += 1 * num_questions

        false_false_belief_test_story_memory = []
        i = 0
        while i < np.max(num_stories_choices):
            task = np.random.choice(tasks)
            false_false_belief_test_story_memory.append(
                '\n'.join(stringify(task(exit_prob=1., informant_prob=1., test_cond='memory').generate_story(w)))
            )
            i += 1 * num_questions

        for num_stories in num_stories_choices:
            for exit_prob in exit_prob_choices:
                for search_prob in search_prob_choices:
                    for informant_prob in informant_prob_choices:
                        folder_name = '%s_nex_%d_exitp_%.2f_searchp_%.2f_informp_%.2f' % (world_name, num_stories, exit_prob, search_prob, informant_prob)
                        logging.info("Creating Sally-Anne task in %s..." % folder_name)
                        mkdir_p(os.path.join(output_dir_path, folder_name))

                        '''
                        # Symlink the bAbi data
                        babi_subdir = 'en' if num_stories < 5000 else 'en-10k'
                        for filepath in glob.glob(os.path.join(babi_dir_path, babi_subdir, '*train.txt')):
                            os.symlink(filepath, os.path.join(output_dir_path, folder_name, os.path.basename(filepath)))
                        '''

                        # Write test stories to file
                        with open(os.path.join(output_dir_path, folder_name, 'true_belief_task_firstord_test.txt'), 'w') as f:
                            f.write('\n'.join(true_belief_test_story_firstord[:int(num_stories / num_questions)]))
                        with open(os.path.join(output_dir_path, folder_name, 'false_belief_task_firstord_test.txt'), 'w') as f:
                            f.write('\n'.join(false_belief_test_story_firstord[:int(num_stories / num_questions)]))
                        with open(os.path.join(output_dir_path, folder_name, 'false_false_belief_task_firstord_test.txt'), 'w') as f:
                            f.write('\n'.join(false_false_belief_test_story_firstord[:int(num_stories / num_questions)]))

                        with open(os.path.join(output_dir_path, folder_name, 'true_belief_task_secondord_test.txt'), 'w') as f:
                            f.write('\n'.join(true_belief_test_story_secondord[:int(num_stories / num_questions)]))
                        with open(os.path.join(output_dir_path, folder_name, 'false_belief_task_secondord_test.txt'), 'w') as f:
                            f.write('\n'.join(false_belief_test_story_secondord[:int(num_stories / num_questions)]))
                        with open(os.path.join(output_dir_path, folder_name, 'false_false_belief_task_secondord_test.txt'), 'w') as f:
                            f.write('\n'.join(false_false_belief_test_story_secondord[:int(num_stories / num_questions)]))

                        with open(os.path.join(output_dir_path, folder_name, 'true_belief_task_reality_test.txt'), 'w') as f:
                            f.write('\n'.join(true_belief_test_story_reality[:int(num_stories / num_questions)]))
                        with open(os.path.join(output_dir_path, folder_name, 'false_belief_task_reality_test.txt'), 'w') as f:
                            f.write('\n'.join(false_belief_test_story_reality[:int(num_stories / num_questions)]))
                        with open(os.path.join(output_dir_path, folder_name, 'false_false_belief_task_reality_test.txt'), 'w') as f:
                            f.write('\n'.join(false_false_belief_test_story_reality[:int(num_stories / num_questions)]))

                        with open(os.path.join(output_dir_path, folder_name, 'true_belief_task_memory_test.txt'), 'w') as f:
                            f.write('\n'.join(true_belief_test_story_memory[:int(num_stories / num_questions)]))
                        with open(os.path.join(output_dir_path, folder_name, 'false_belief_task_memory_test.txt'), 'w') as f:
                            f.write('\n'.join(false_belief_test_story_memory[:int(num_stories / num_questions)]))
                        with open(os.path.join(output_dir_path, folder_name, 'false_false_belief_task_memory_test.txt'), 'w') as f:
                            f.write('\n'.join(false_false_belief_test_story_memory[:int(num_stories / num_questions)]))

                        # AB
                        filename = 'qa21_task_AB_train.txt'
                        tasks = [
                            ActionsBeliefsTask,
                        ]
                        story = []

                        i = 0
                        while i < num_stories:
                            task = np.random.choice(tasks)
                            for test_cond in test_cond_choices:
                                story.extend(
                                    stringify(task(exit_prob=exit_prob, informant_prob=informant_prob, search_prob=search_prob, test_cond=test_cond).generate_story(w))
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
                            for test_cond in test_cond_choices:
                                story.extend(
                                    stringify(task(exit_prob=exit_prob, informant_prob=informant_prob, search_prob=search_prob, test_cond=test_cond).generate_story(w))
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
                            for test_cond in test_cond_choices:
                                story.extend(
                                    stringify(task(exit_prob=exit_prob, informant_prob=informant_prob, search_prob=search_prob, test_cond=test_cond).generate_story(w))
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
                            for test_cond in test_cond_choices:
                                story.extend(
                                    stringify(task(exit_prob=exit_prob, informant_prob=informant_prob, search_prob=search_prob, test_cond=test_cond).generate_story(w))
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
                            for test_cond in test_cond_choices:
                                story.extend(
                                    stringify(task(exit_prob=exit_prob, informant_prob=informant_prob, search_prob=search_prob, test_cond=test_cond).generate_story(w))
                                )
                            i += 1 * num_questions
                        story = '\n'.join(story)

                        # Write the stories to file
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

    parser.add_argument('-pi', '--prob_informant', dest='informant_prob_choices', type=float,
                        action='append',
                        help='Probability that, given an exit occurred, that the agent who left will \
                        be informed about a change in the state of the world, \
                        in Sally-Anne training tasks, all types')

    parser.add_argument('-test', '--test_cond', dest='test_cond_choices',
                        choices=['first order', 'second order', 'reality', 'memory'],
                        action='append', required=True,
                        help='Types of test question')


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


if __name__ == "__main__":
    sys.exit(main())
