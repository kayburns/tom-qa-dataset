class World(object):

    def __init__(self, world_actions=[], entities={}):

        self.actions = world_actions or False

        self.entities = entities or {}

        if not 'god' in self.entities:
            #self.create_entity('god', {'is_god': True})
            self.entities['god'] = {'is_god': True}

    def god(self):
        return self.entities['god']

    def load(self, fname):

        lines = open(fname, 'r').readlines()
        i = 0

        while i < len(lines):
            line = lines[i].rstrip('\n')
            if line != '' and not line.startswith('#'):
                #self:perform_command('god ' .. line)
                if line.startswith('create'):
                    self.entities[line.split(' ')[1]] = {}
                elif line.startswith('set'):
                    self.entities[line.split(' ')[1]][line.split(' ')[-1]] = True

            i += 1

    def perform_action(self, action, actor):
        pass

    def perform_command(self, command):
        pass

    def create_entity(self, id, properties, name=None):

        name = name or id

        if 'id' in self.entities:
            raise InputError(id, 'id already exists')

        self.entities[id] = Entity(name, properties)

        return self.entities[id]

    def get_entity(self, predicates):

        if not isinstance(predicates, list):
            raise InputError(predicates, 'is not a list.')

        return_val = []

        for k in self.entities:

            if all([predicate in self.entities[k] and self.entities[k][predicate] is True for predicate in predicates]):

                return_val += [k]


        return return_val

    def get_actors(self):
        return self.get_entity(['is_actor', 'is_god'])

    def get_locations(self):
        return self.get_entity(['is_location'])

    def get_objects(self):
        return self.get_entity(['is_thing', 'is_gettable'])

    def get_containers(self):
        return self.get_entity(['is_thing', 'is_container'])
