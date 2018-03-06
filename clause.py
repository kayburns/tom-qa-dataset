import numpy as np


class Clause(object):

    def __init__(self, observers, action):

        if observers is not None:
            assert 0 not in observers, "Observer IDs must be 1-indexed"
        self.observers = observers
        self.action = action

    def render(self):
        return self.action.render_declarative() + \
            ('\t' + ' '.join([str(x) for x in self.observers])
             if self.observers is not None else '')


class Question(Clause):

    def __init__(self, idx_support, action):
        self.idx_support = idx_support
        super().__init__(None, action)

    def render(self):
        return self.action.render_interrogative()
