'''
Created on 2014-03-31

@author: Nich
'''

class VisibleThingsSystem(object):
    '''
    Attach all the things that a person can see to that person so that the parser knows what's available
    '''


    def __init__(self, node_factory):
        self.node_factory = node_factory
        
        
    def get_nodes(self):
        nodes = self.node_factory.create_node_list(["senses", "location"])
        return nodes
    
    def process(self):
        
        nodes = self.get_nodes()
        for node in nodes:
            #for now just dump the ids in a big list
            room_id = node.location.room
            room_node = self.node_factory.create_node(room_id, ["container"])
            node.add_or_attach_component("visible_objects", None)
            objects = list(room_node.container.children)
            object_ids = [o.entity_id for o in objects]
            object_ids.remove(node.id)
            node.visible_objects.objects = object_ids
            
        