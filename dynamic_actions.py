import numpy as np


class Action(object):

    def __init__(self, templates):
        self.templates = templates

    def render_declarative(self):
        assert 'declarative' in self.templates and \
            len(self.templates['declarative']) > 0
        return np.random.choice(self.templates['declarative'])

    def render_interrogative(self):
        assert 'interrogative' in self.templates and \
            len(self.templates['interrogative']) > 0, str(self.templates)
        return np.random.choice(self.templates['interrogative'])


class ExitAction(Action):

    def __init__(self):
        templates = {
            'declarative': [
                '%s exited the %s.',
                '%s left the %s.',
                '%s went out of the %s.',
            ],
        }
        super().__init__(templates)
        
class SearchedAction(Action):

    def __init__(self, oracle, agent, obj):
        fill = (agent, obj, oracle.get_direct_belief(agent, obj))
        templates = {
            'interrogative': [
                'Where will %s look for the %s?\t%s' % fill,
            ]
        }
        super().__init__(templates)
        
class BeliefSearchAction(Action):

    def __init__(self, oracle, a1, a2, obj):
        fill = (a1, a2, obj, oracle.get_indirect_belief(a1, a2, obj))
        templates = {
            'interrogative': [
                'Where does %s think that %s searches for the %s?\t%s' % fill,
            ]
        }
        super().__init__(templates)
        
class RealityAction(Action):

    def __init__(self, oracle, obj):
        
        fill = (obj, oracle.get_object_container(obj))
        templates = {
            'interrogative': [
                'Where is the %s really?\t%s' % fill,
            ]
        }
        super().__init__(templates)
        
class MemoryAction(Action):

    def __init__(self, oracle_start_state, obj):
        fill = (obj, oracle_start_state.get_object_container(obj))
        templates = {
            'interrogative': [
                'Where was the %s at the beginning?\t%s',
            ]
        }
        super().__init__(templates)

class LocationAction(Action):
    # TODO: possibly change to infer location

    def __init__(self, oracle, args):
        """
        Creaters string with args and modifies 
        oracle in accordance with action.
        """
        if len(args) == 2:
            statement = '%s is in the %s.' % args
            a1, loc = args
            # may be redundant
            oracle.set_location(a1, loc)
        else : # 2 people
            statement = '%s and %s are in the %s.' % args
            a1, a2, loc = args
            # may be redundant
            oracle.set_location(a1, loc)
            oracle.set_location(a2, loc)
            
        templates = {
            'declarative': [
                statement,
            ]
        }
        
        super().__init__(templates)

class ObjectLocAction(Action):

    def __init__(self, oracle, obj, observers):
        container = oracle.get_object_container(obj)
        templates = {
            'declarative': [
                'The %s is in the %s.' % (obj, container),
            ]
        }
        
        # set direct beliefs
        for observer in observers:
            oracle.set_direct_belief(observer, obj, container)
            
        # set indirect beliefs
        for observer1 in observers:
            for observer2 in observers:
                if observer1 != observer2:
                    oracle.set_indirect_belief(observer1, observer2, obj, container)
        super().__init__(templates)
        
class ExitedAction(Action):

    def __init__(self, oracle, agent):
        fill = (agent, oracle.get_location(agent))
        
        templates = {
            'declarative': [
                '%s exited the %s.' % fill,
            ]
        }
        oracle.set_location(agent, None)
        super().__init__(templates)

class MoveAction(Action):

    def __init__(self, oracle, args, observers=None):
        templates = {
            'declarative': [
                '%s moved the %s to the %s.' % args,
            ]
        }
        
        agent, obj, container = args
        oracle.set_object_container(obj, container)
        
        if not observers:
            observers = []
        observers.append(agent)
        # set direct beliefs
        for observer in observers:
            oracle.set_direct_belief(observer, obj, container)
            
        # set indirect beliefs
        for observer1 in observers:
            for observer2 in observers:
                if observer1 != observer2:
                    oracle.set_indirect_belief(observer1, observer2, obj, container)
                    
        super().__init__(templates)

class TellAction(Action):

    def __init__(self, oracle, a1, a2, obj):
        templates = {
            'declarative': [
                '%s told %s where the %s is.'% (a1, a2, obj),
            ]
        }
        
        container = oracle.get_object_container(obj)
        oracle.set_direct_belief(a2, obj, container)
        oracle.set_indirect_belief(a2, a1, obj, container)
        super().__init__(templates)
        
class EnterAction(Action):

    def __init__(self, oracle, args):
        templates = {
            'declarative': [
                '%s entered the %s.' % args,
            ]
        }
        
        agent, location = args
        oracle.set_location(agent, location)
        super().__init__(templates)

    