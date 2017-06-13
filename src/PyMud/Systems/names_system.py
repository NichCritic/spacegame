'''
Created on 2014-03-31

@author: Nich
'''


class NamesSystem(object):
    '''
    Attach all the things that a person can see to that person so that the parser knows what's available
    '''


    def __init__(self, node_factory):
        self.node_factory = node_factory
        
        
    def get_nodes(self):
        nodes = self.node_factory.create_node_list(["visible_objects"])
        return nodes
    
    def process(self):
        
        nodes = self.get_nodes()
        for node in nodes:
            #for now just dump the ids in a big list
            names = []
            for name_id in node.visible_objects.objects:
                name_node = self.node_factory.create_node(name_id, ["names"])
                names += name_node.names.identifiers
                
                node.add_or_attach_component("visible_names", None)
                node.visible_names.names = names
                
            
        