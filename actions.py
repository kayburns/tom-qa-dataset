import numpy as np


class Action(object):

    def __init__(self, templates):
        self.templates = templates

    def render_declarative(self, *args):
        assert 'declarative' in self.templates and len(self.templates['declarative']) > 0
        return np.random.choice(self.templates['declarative']) % args

    def render_interrogative(self, *args):
        assert 'interrogative' in self.templates and len(self.templates['interrogative']) > 0, str(self.templates)
        return np.random.choice(self.templates['interrogative']) % args


class ExistBeginning(Action):

    def __init__(self):
        templates = {
            'interrogative': [
                'Where was the %s at the beginning?\t%s',
                'Where was the %s before?\t%s',
            ]
        }
        super().__init__(templates)


class Exist(Action):

    def __init__(self):
        templates = {
            'interrogative': [
                'Where is the %s?\t%s',
                'Where is the %s located?\t%s',
            ]
        }
        super().__init__(templates)


class PlaceAction(Action):

    def __init__(self):
        templates = {
            'declarative': [
                '%s placed the %s in the %s.',
                '%s put the %s in the %s.',
            ],
            'interrogative': [
                'Where did %s place the %s?\t%s',
                'Where did %s put the %s?\t%s',
            ]
        }
        super().__init__(templates)


class SearchAction(Action):

    def __init__(self):
        templates = {
            'declarative': [
                '%s searched for the %s in the %s.',
                '%s looked for the %s in the %s.',
            ],
            'interrogative': [
                'Where did %s search for the %s?\t%s',
                'Where did %s look for the %s?\t%s',
            ],
        }
        super().__init__(templates)


class TransportAction(Action):

    def __init__(self):
        templates = {
            'declarative': [
                '%s shifted the %s from the %s to the %s.',
            ],
        }
        super().__init__(templates)


class EnterAction(Action):

    def __init__(self):
        templates = {
            'declarative': [
                '%s entered the %s.',
                '%s came into the %s.',
            ],
        }
        super().__init__(templates)


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


class BelieveLocationAction(Action):

    def __init__(self):
        templates = {
            'declarative': [
                '%s thinks the %s is in the %s.',
                '%s believes the %s is in the %s.',
            ],
            'interrogative': [
                'Where does %s think the %s is?\t%s',
                'Where does %s believe the %s is?\t%s',
            ],
        }
        super().__init__(templates)


class BelieveAgentBelieveLocationAction(Action):

    def __init__(self):
        templates = {
            'interrogative': [
                'Where does %s think that %s believes the %s is?\t%s',
                'Where does %s believe that %s believes the %s is?\t%s',
                'Where does %s think that %s thinks the %s is?\t%s',
                'Where does %s believe that %s thinks the %s is?\t%s',
            ],
        }
        super().__init__(templates)


class BelieveAgentSearchLocationAction(Action):

    def __init__(self):
        templates = {
            'interrogative': [
                'Where does %s think that %s looks for the %s?\t%s',
                'Where does %s believe that %s looks for the %s?\t%s',
                'Where does %s think that %s searches for the %s?\t%s',
                'Where does %s believe that %s search for the %s?\t%s',
            ],
        }
        super().__init__(templates)


class InformLocationAction(Action):

    def __init__(self):
        templates = {
            'declarative': [
                '%s told %s that the %s is in the %s.',
                '%s informed %s that the %s is in the %s.',
            ],
        }
        super().__init__(templates)
