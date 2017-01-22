import numpy as np


class Action(object):

    def __init__(self, templates):
        self.templates = templates

    def render_declarative(self, *args):
        assert 'declarative' in self.templates and len(self.templates['declarative']) > 0
        return np.random.choice(self.templates['declarative']) % args

    def render_interrogative(self, *args):
        assert 'interrogative' in self.templates and len(self.templates['interrogative']) > 0
        return np.random.choice(self.templates['interrogative']) % args


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
