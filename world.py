class World(object):

    def __init__(self, world_actions=[], entities={}):
        self.actions = world_actions
        self.entities = entities

    def load(self, fname):

        lines = open(fname, 'r').readlines()
        i = 0

        while i < len(lines):
            line = lines[i].rstrip('\n')
            if line != '' and not line.startswith('#'):
                if line.startswith('create'):
                    self.entities[line.split(' ')[1]] = {}
                elif line.startswith('set'):
                    self.entities[line.split(' ')[1]][line.split(' ')[-1]] = True

            i += 1

    def get_entity(self, predicates):

        if not isinstance(predicates, list):
            raise InputError(predicates, 'is not a list.')

        return_val = []

        for k in self.entities:
            if all([predicate in self.entities[k] and
                    self.entities[k][predicate] is True
                    for predicate in predicates]):
                return_val += [k]

        return return_val

    def get_actors(self):
        return self.get_entity(['is_actor', 'is_god'])

    def get_containers(self):
        return self.get_entity(['is_thing', 'is_container'])

    def get_locations(self):
        return self.get_entity(['is_location'])

    def get_objects(self):
        return self.get_entity(['is_thing', 'is_gettable'])
