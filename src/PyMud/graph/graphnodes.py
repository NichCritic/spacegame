'''
Created on 2013-02-27

@author: Nich
'''

from collections import namedtuple
import uuid


class Container():
    def __init__(self, data):
        self.data = data
        self.contents = {}
    
    def add_content(self, content):
        if not content.id in self.contents:
            self.contents[content.id] = content
        else:
            raise Exception("A container can't have more then one thing with the same id")

class Node():
    def __init__(self):
        self.links = []
        
    def add_link(self, link):
        self.links.append(link)
        
    def get_neighbours(self):
        return [l.get_neighbour(self) for l in self.links]
    
class Link():
    def __init__(self, a, b):
        if not a is b:
            self.a = a
            self.b = b
            a.add_link(self)
            b.add_link(self)
        else:
            raise Exception("Nodes can not link to themselves")
        
    def get_neighbour(self, node):
        if node == self.a:
            return self.b
        elif node == self.b:
            return self.a
        else:
            raise Exception("The node specified is not part of this link")
        


class DataNode(Node):
    def __init__(self, data):
        Node.__init__(self)
        self.data = data
        
    

# A Room is a container for locations
class Room(Container):
    def __init__(self, name, data=None):
        
        self.id = uuid.uuid4()
        self.name = name
        self.data = {} if data is None else data
        super(Room, self).__init__(data)
        
    
    def add_location(self, location_name):
        l = LocationNode(Location(uuid.uuid4(), location_name, self, {}))
        self.add_content(l)
        return l
    
    def get_locations(self):
        return self.data
    
    

# A location is a container for objects, and a node for other locations
class LocationNode(DataNode, Container):
    def __init__(self, data):
        DataNode.__init__(self, data)
        Container.__init__(self, data)
        
        self.data = data
        self.id = self.data.id
        
    
    def add_object(self, object):
        dir(self)
        self.add_content(object)
        return object
    
    def get_objects(self):
        return self.data
        
    def __iter__(self):
        return walk_tree_bf(self)     
        
    def __repr__(self):
        return "<"+self.data.room.name+"."+self.data.name+">"
    


def walk_tree_bf(starting_node):
    queue = []
    visited = set()
    
    queue.append(starting_node)
    visited.add(starting_node)
    
    for n in queue:
        yield n
        for node in n.get_neighbours():
            if node not in visited:
                queue.append(node)
                visited.add(node)
        
# An object is ... lots of things. For right now, we'll just give them names and ids
Object = namedtuple("Object", ["id", "name", "type"])
Location = namedtuple("Location", ["id", "name", "room", "data"])
