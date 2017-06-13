'''
Created on 2013-11-30

@author: Nich
'''

class LocationSystem(object):
    '''
    classdocs
    '''


    def __init__(self, node_factory):
        self.node_factory = node_factory
    
    def get_nodes(self):
        return self.node_factory.create_node_list(["location"])
        
    def process(self):
        room_bag = {}
        for node in self.get_nodes():
            if not node.location.room in room_bag:
                room_bag[node.location.room] = []
            room_bag[node.location.room].append(node.id)
        
        for room_id in room_bag.keys():
            room = self.node_factory.create_node(room_id, [])
            room.add_or_attach_component("object_container", None)
            room.object_container.objects = room_bag[room_id]
        
       
    def get_locations_near(self, node):
        obj_node = self.node_factory.create_node(node.id, ["location"])
        loc_node = self.node_factory.create_node(obj_node.location.location, ["node"])
        
        return [obj_node.location.location] + [loc for loc in loc_node.node.neighbours()]
        
    def get_objects_within_dist(self, node, dist):
        obj_node =  self.node_factory.create_node(node.id, ["location"])
        loc_node = self.node_factory.create_node(obj_node.location.location, ["node", "location"])
        loc_nodes = [self.node_factory.create_node(l.id, ["location", "objects"]) for l in self.get_locations_within_dist(loc_node, dist)]
        results = []
        for l in loc_nodes:
            for o in l.objects.get_objects():
                if not o.id == node.id:
                    results.append(o)
        return results
   
    def get_locations_within_dist(self, start, dist):
        queue = []
        visited = set()
        
        start_node = self.node_factory.create_node(start.id, ["location", "node"])
        
        queue.append(start_node)
        visited.add(start_node.id)
        
        for n in queue:
            yield n
            for node in n.node.neighbours():
                loc_node = self.node_factory.create_node(node.id, ["node", "location"])
                if loc_node.id not in visited and self.distance(loc_node.location, start_node.location) < dist:
                    queue.append(loc_node)
                    visited.add(loc_node.id) 
        
    
    
    def distance(self, location1, location2):
        
        import math
        x1 = location1.x
        y1 = location1.y
        z1 = location1.z
        
        x2 = location2.x
        y2 = location2.y
        z2 = location2.z
        
        dist = math.sqrt((x2-x1)**2 + (y2-y1)**2 + (z2-z1)**2)
        return dist    
        
    
        