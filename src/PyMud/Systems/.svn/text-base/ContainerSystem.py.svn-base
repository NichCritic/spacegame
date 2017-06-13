'''
Created on 2013-11-25

@author: Nich
'''

class ContainerSystem(object):
    '''
    classdocs
    '''


    def __init__(self, node_factory):
        '''
        Constructor
        '''
        self.node_factory = node_factory
        self.container_nodes = {}
        
            
    def get_contents(self, container_id):
        self.update()
        return self.container_nodes[container_id].contents
    
    def update(self):
        nodes = self.node_factory.create_node_list(["container"])
        for n in nodes:
            self.container_nodes[n.id] = n  
        
        