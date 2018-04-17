import numpy as np


from clause import Clause, Question
from oracle import Oracle
from dynamic_actions import *
from collections import defaultdict
import random

def sample_question(oracle_start_state, oracle, agent1, agent2, obj, question):
    idx_dummy = [0]
    questions = [Question(idx_dummy, SearchedAction(oracle, agent1, obj)),
                 Question(idx_dummy, SearchedAction(oracle, agent2, obj)),
                 Question(idx_dummy, BeliefSearchAction(oracle, agent1, agent2, obj)), 
                 Question(idx_dummy, RealityAction(oracle, obj)),
                 Question(idx_dummy, MemoryAction(oracle_start_state, obj))
                ]
    if question:
        if question == 'memory':
            return questions[-1]
        elif question == 'reality':
            return questions[3]
        elif question == 'belief':
            return questions[2]
        elif question == 'search':
            return questions[1] # first agent search unused
    return np.random.choice(questions)

#######################################
############## Chapters ###############
#######################################

def write_true_belief_chapter(start_state, oracle, location, agent_ids, all_agents, question=None):
    """
    Creates list of clauses that constitute
    a true belief task.
    
    agent_ids: list that gives indices of agents
      in container. should be length 2.
    all_agents: list of all agents
    container: container to which the object is
      moved
    question: one of ['memory', 'reality', 'belief', 'search', None]
      if None, then pick randomly
    
    Warning: clauses will advance that state
    of the simulation, should clauses should
    be appended in order.
    """
    a1, a2 = all_agents[agent_ids[0]], all_agents[agent_ids[1]]
    agent_ids = [aid+1 for aid in agent_ids]
    
    # pick random object at location
    obj = np.random.choice(oracle.get_objects_at_location(location))
    container_1 = oracle.get_object_container(obj)
    
    # pick random container in locations
    container_candidates = oracle.get_containers(location)[:]
    container_candidates.remove(container_1)
    container_2 = np.random.choice(container_candidates) # set would be more elegant
    
    chapter = []
    
    # move agents into location
    if oracle.get_location(a1) == location:
        chapter.extend([Clause([agent_ids[0]], LocationAction(oracle, (a1, location)))])
    else:
        chapter.extend([Clause([agent_ids[0]], EnterAction(oracle, (a1, location)))])
        
    if oracle.get_location(a2) == location:
        chapter.extend([Clause(agent_ids, LocationAction(oracle, (a2, location)))])
    else:
        chapter.extend([Clause(agent_ids, EnterAction(oracle, (a2, location), [a1]))])
            
    chapter.extend([ 
        Clause(agent_ids, ObjectLocAction(oracle, obj, [a1, a2])),
        Clause(agent_ids, MoveAction(oracle, (a1, obj, container_2), [a2])),
        #TODO: fancy inheritance to copy start state
        sample_question(start_state, oracle, a1, a2, obj, question)
    ])
    
    return chapter

def write_false_belief_chapter(start_state, oracle, location, agent_ids, all_agents, question=None):
    """
    Creates list of clauses that constitute
    a true belief task.
    
    agent_ids: list that gives indices of agents
      in container. should be length 2.
    all_agents: list of all agents
    container: container to which the object is
      moved
    
    Warning: clauses will advance that state
    of the simulation, should clauses should
    be appended in order.
    """
    a1, a2 = all_agents[agent_ids[0]], all_agents[agent_ids[1]]
    agent_ids = [aid+1 for aid in agent_ids]
    
    # pick random object at location
    obj = np.random.choice(oracle.get_objects_at_location(location))
    container_1 = oracle.get_object_container(obj)
    
    # pick random container in locations
    container_candidates = oracle.get_containers(location)[:]
    container_candidates.remove(container_1)
    container_2 = np.random.choice(container_candidates) # set would be more elegant
    
    chapter = []
    
    # move agents into location
    if oracle.get_location(a1) == location:
        chapter.extend([Clause([agent_ids[0]], LocationAction(oracle, (a1, location)))])
    else:
        chapter.extend([Clause([agent_ids[0]], EnterAction(oracle, (a1, location)))])
        
    if oracle.get_location(a2) == location:
        chapter.extend([Clause(agent_ids, LocationAction(oracle, (a2, location)))])
    else:
        chapter.extend([Clause(agent_ids, EnterAction(oracle, (a2, location), [a1]))])

    chapter.extend([
        Clause(agent_ids, ObjectLocAction(oracle, obj, [a1, a2])),
        Clause(agent_ids, ExitedAction(oracle, (a2))),
        Clause([agent_ids[0]], MoveAction(oracle, (a1, obj, container_2))),
        #Clause(agent_ids, EnterAction(oracle, (a2, location))),
        # TODO: fancy inheritance to copy start state
        sample_question(start_state, oracle, a1, a2, obj, question)
    ])
    
    return chapter

def write_second_order_false_belief_chapter(start_state, oracle, location, agent_ids, all_agents, question=None):
    """
    Creates list of clauses that constitute
    a true belief task.
    
    agent_ids: list that gives indices of agents
      in container. should be length 2.
    all_agents: list of all agents
    container: container to which the object is
      moved
    
    Warning: clauses will advance that state
    of the simulation, should clauses should
    be appended in order.
    """
    a1, a2 = all_agents[agent_ids[0]], all_agents[agent_ids[1]]
    agent_ids = [aid+1 for aid in agent_ids]
    
    # pick random object at location
    obj = np.random.choice(oracle.get_objects_at_location(location))
    container_1 = oracle.get_object_container(obj)
    
    # pick random container in locations
    container_candidates = oracle.get_containers(location)[:]
    container_candidates.remove(container_1)
    container_2 = np.random.choice(container_candidates) # set would be more elegant
    
    chapter = []
    
    # move agents into location
    if oracle.get_location(a1) == location:
        chapter.extend([Clause([agent_ids[0]], LocationAction(oracle, (a1, location)))])
    else:
        chapter.extend([Clause([agent_ids[0]], EnterAction(oracle, (a1, location)))])
        
    if oracle.get_location(a2) == location:
        chapter.extend([Clause(agent_ids, LocationAction(oracle, (a2, location)))])
    else:
        chapter.extend([Clause(agent_ids, EnterAction(oracle, (a2, location), [a1]))])

    chapter.extend([
        Clause(agent_ids, ObjectLocAction(oracle, obj, [a1, a2])),
        Clause(agent_ids, ExitedAction(oracle, (a2))),
        Clause([agent_ids[0]], MoveAction(oracle, (a1, obj, container_2))),
        Clause([agent_ids[0]], ExitedAction(oracle, (a1))),
        Clause([agent_ids[1]], EnterAction(oracle, (a2, location))),
        sample_question(start_state, oracle, a1, a2, obj, question)
    ])
      
    return chapter

#######################################
############### Tasks #################
#######################################

class Task(object):

    def __init__(self,
                 num_questions=5,
                 exit_prob=1.,
                 informant_prob=1.,
                 search_prob=1.,
                 test_cond='first order'):

        self.num_questions = num_questions

        self.search_prob = search_prob

        self.exit_inform_probs = [1 - exit_prob,
                                  exit_prob * (1 - informant_prob),
                                  exit_prob * informant_prob]
        assert sum(self.exit_inform_probs) == 1

        assert test_cond in ['first order',
                             'second order',
                             'reality',
                             'memory'], \
            "Invalid test condition: %s" % test_cond
        self.test_cond = test_cond

    def generate_story(self, world):
        raise NotImplementedError("Abstract method.")

class All_Tasks(Task):
    def generate_story(self, world, tasks_per_story=3, num_agents=6, num_locations=3, task_dist=None):
        """
        Returns a list of clauses in story for a
        simple True Belief task.
        """ 

        idx_support_dummy = [0]
        actors = world.get_actors()
        locations = world.get_locations()
        objects = world.get_objects()
        containers = world.get_containers()
        
        random_actors = np.random.choice(actors, size=num_agents, replace=False)
        random_locations = np.random.choice(locations, size=num_locations, replace=False)
        random_objects = np.random.choice(objects, size=num_locations*2, replace=False)
        random_containers = np.random.choice(containers, size=num_locations*2, replace=False)
        
        oracle = Oracle(random_actors, random_locations, random_objects, random_containers)
        
        # Populate locations in the oracle with containers
        for i in range(len(random_locations)):
            location = random_locations[i]
            containers = random_containers[2*i:2*i+2] # TODO: find better way to assign containers
            oracle.set_containers(location, list(containers))
            
        for i in range(len(random_objects)):
            oracle.set_object_container(random_objects[i], random_containers[i])
            
        start_state = oracle.locations.obj_containers.copy()
        
        chapters = [write_true_belief_chapter, write_false_belief_chapter, write_second_order_false_belief_chapter]
        questions = ['memory', 'reality', 'belief', 'search']
        
        story = []
        
        for i in range(tasks_per_story):
            
            if task_dist: # hacky way to distinguish training from test gen cases :(
                chapter = np.random.choice(chapters, p=task_dist)
            else:
                chapter = np.random.choice(chapters)
            question = np.random.choice(questions)
            location = np.random.choice(random_locations)
            agent_ids = np.random.choice(range(len(random_actors)), size=2, replace=False)
            story.extend(chapter(start_state, oracle, location, agent_ids, random_actors, question))
                        
        return story
 
class Specify_Tasks(Task):
    def generate_story(self, world, tasks_per_story, tasks, questions, num_agents=6, num_locations=3, statement_noise=0):
        """
        Allows user to specify chapter and question for
        each task in story.
        
        :tasks: list with length of tasks per story. Each
        entry is a string in the set {'tb','fb','sofb'}
        
        :questions: list with length of tasks per story.
        Each entry is a string in the set {'memory',
        'reality', 'belief', 'search'}

        :statement_noise: probability of encountering noise
        sentence like 'The dog ran through the kitchen.'
        """ 

        idx_support_dummy = [0]
        actors = world.get_actors()
        locations = world.get_locations()
        objects = world.get_objects()
        containers = world.get_containers()
        
        random_actors = np.random.choice(actors, size=num_agents, replace=False)
        random_locations = np.random.choice(locations, size=num_locations, replace=False)
        random_objects = np.random.choice(objects, size=num_locations*2, replace=False)
        random_containers = np.random.choice(containers, size=num_locations*2, replace=False)
        
        oracle = Oracle(random_actors, random_locations, random_objects, random_containers)
        
        # Populate locations in the oracle with containers
        for i in range(len(random_locations)):
            location = random_locations[i]
            containers = random_containers[2*i:2*i+2] # TODO: find better way to assign containers
            oracle.set_containers(location, list(containers))
            
        for i in range(len(random_objects)):
            oracle.set_object_container(random_objects[i], random_containers[i])
            
        start_state = oracle.locations.obj_containers.copy()

        
        chapters = {'tb':write_true_belief_chapter, 'fb':write_false_belief_chapter,
                    'sofb':write_second_order_false_belief_chapter}
        
        story = []
        
        for i in range(tasks_per_story):
            
            chapter = chapters[tasks[i]]
            location = np.random.choice(random_locations)
            agent_ids = np.random.choice(range(len(random_actors)), size=2, replace=False)
            story.extend(chapter(start_state, oracle, location, agent_ids, random_actors, questions[i]))
            
        if statement_noise:
            noisy_story = []
            prev_i = 0
            noise = [i for i in range(len(story)) if np.random.rand() < statement_noise]
            for i in noise:
                noisy_story.extend(story[prev_i:i] + [Clause([], NoiseAction())])
                prev_i = i
            noisy_story.extend(story[prev_i:])
            
            return noisy_story
                        
        return story
       
