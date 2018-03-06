"""
The Oracle class keeps track of all object
and agent locations as well as a map of
beliefs about object and agent locations.
"""

class LocationMap(object):

    def __init__(self, agents, locations, objects, containers):
        
        # Maps agents to their locations.
        self.locations = {agent : None for agent in agents}
        
        # Maps agents to their locations.
        self.container_locations = {container : None for container in containers}
        
        # Maps locations to their containers
        self.containers = {location : None for location in locations}
        
        # Maps containers to the objects they hold
        self.container_objs = {container : [] for container in containers}
        
        # Maps objects to their containers
        self.obj_containers = {obj : None for obj in objects}

class MemoryMap(object):
    
    def __init__(self, agents, objects):
        
        obj_dict = {obj : None for obj in objects}
        mem_dict = {agent : obj_dict.copy() for agent in agents}
        
        # Dictionary of dictionaries mapping
        # agents to objects to containers. Represents
        # agents' belief about location of containers.
        self.direct_beliefs = mem_dict
        
        # Dictionary of dictionaries of dictionaries
        # mapping agents to direct belief dictionaries.
        # Represents agents' belief about other agents'
        # beliefs about location of containers.
        self.indirect_beliefs = {agent : mem_dict.copy() for agent in agents}

class Oracle(object):

    def __init__(self, agents, locations, objects, containers):
        self.memory_map = MemoryMap(agents, objects)
        self.locations = LocationMap(agents, locations, objects, containers)
        
    #########################################
    ################ Beliefs ################
    #########################################
    
    def get_direct_belief(self, agent, obj):
        beliefs = self.memory_map.direct_beliefs
        return beliefs[agent][obj]
    
    def set_direct_belief(self, agent, obj, container):
        beliefs = self.memory_map.direct_beliefs
        beliefs[agent][obj] = container
    
    def get_indirect_belief(self, a1, a2, obj):
        indirect_beliefs = self.memory_map.indirect_beliefs
        return indirect_beliefs[a1][a2][obj]
            
    def set_indirect_belief(self, a1, a2, obj, container):
        indirect_beliefs = self.memory_map.indirect_beliefs
        indirect_beliefs[a1][a2][obj] = container
    
    #########################################
    ############### Locations ###############
    #########################################
    
    def get_location(self, agent):
        return self.locations.locations[agent]
    
    def set_location(self, agent, location):
        self.locations.locations[agent] = location
        
    def get_containers(self, location):
        # Returns a list of containers at location
        return self.locations.containers[location]
    
    def set_containers(self, location, containers):
        # May need to change to move containers bt locs
        # Containers is a list of containers at location
        for container in containers:
            self._set_container_location(container, location)
        self.locations.containers[location] = containers
        
    def get_objects_at_location(self, location):
        objects = []
        for container in self.get_containers(location):
            objects.extend(self.get_container_obj(container))
        return objects
       
    def get_container_location(self, containers):
        return self.locations.container_locations[container]
    
    def _set_container_location(self, container, location):
        self.locations.container_locations[container] = location
        
    def get_container_obj(self, container):
        # get list of objects in container
        return self.locations.container_objs[container]
    
    def _add_container_obj(self, container, obj):
        self.locations.container_objs[container].append(obj)
        
    def _remove_container_obj(self, container, obj):
        self.locations.container_objs[container].remove(obj)
    
    def get_object_container(self, obj):
        # get container that holds object
        return self.locations.obj_containers[obj]
    
    def set_object_container(self, obj, container):
        # set container that holds object
        prev_container = self.get_object_container(obj)
        if prev_container:
            self._remove_container_obj(prev_container, obj)
        self._add_container_obj(container, obj)
        self.locations.obj_containers[obj] = container
    
            