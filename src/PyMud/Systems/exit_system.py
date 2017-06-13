'''
Created on 2014-03-22

@author: Nich
'''

class ExitSystem(object):
    '''
    classdocs
    '''


    def __init__(self, node_factory):
        '''
        Constructor
        '''
        self.node_factory = node_factory
    
    def get_nodes(self):
        return self.node_factory.create_node_list(["location", "exiting"])
    
    def get_path(self):
        pass
    def path_clear(self, path):
        return True
    
    def process(self):
        nodes = self.get_nodes()
        for node in nodes:
            exit_node = self.node_factory.create_node(node.exiting.exit, ["exit"])
            node.location.x = exit_node.exit.dest_x
            node.location.y = exit_node.exit.dest_y
            node.location.z = exit_node.exit.dest_z
            node.remove_component("exiting")
                