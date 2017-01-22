import numpy as np


class Clause(object):

    def __init__(self, world, truth_value, actor, action, *args):

        self.world = world
        self.truth_value = truth_value
        self.actor = actor
        self.action = action
        self.args = args

    def render(self):
        return self.action.render_declarative(self.actor, *self.args)

    def is_valid(self):
        return self.action.is_valid(self.world, self.actor, *self.args)

    def perform(self):
        if self.truth_value:
            self.action.perform(self.world, self.actor, *self.args)

    def __eq__(self, other):
        return self.world == other.world and self.actor == other.actor and self.args == other.args

    def sample_valid(world, truth_values, actors, actions, *args, retries=100):

        for _ in range(retries):

            truth_value = np.random.choice(truth_values)
            actor = np.random.choice(actors)
            action = np.random.choice(actions)

            args = []

            raise NotImplementedError #TODO


class Question(Clause):

    def __init__(self, idx_support, actor, action, *args):
        self.idx_support = idx_support
        super().__init__(None, None, actor, action, *args)

    def render(self):
        return self.action.render_interrogative(self.actor, *self.args)

