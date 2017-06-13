'''
Created on 2014-03-22

@author: Nich
'''

class MovementSystem(object):
    '''
    classdocs
    '''


    def __init__(self, node_factory):
        '''
        Constructor
        '''
        self.node_factory = node_factory
    
    def get_nodes(self):
        return self.node_factory.create_node_list(["location", "moving"])
    
    def get_path(self):
        pass
    def path_clear(self, path):
        return True
    
    def process(self):
        nodes = self.get_nodes()
        for node in nodes:
            path = self.get_path()
            if self.path_clear(path):
                node.location.x = node.moving.x
                node.location.y = node.moving.y
                if node.moving.z:
                    node.location.z = node.moving.z
            node.remove_component("moving")
                