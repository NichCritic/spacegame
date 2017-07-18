'''
Created on 2014-03-15

@author: Nich
'''

from messages.message_types import AVMessage

class AVEventSystem(object):
    '''
    classdocs
    '''


    def __init__(self, node_factory):
        self.node_factory = node_factory
        
    def get_nodes(self):
        return self.node_factory.create_node_list(["container", "av_events"])
    
    def process(self):
        for node in self.get_nodes():
            print("AVEvent system got message from "+node.id)
            for obj in node.container.children:
                o_node = self.node_factory.create_node(obj.entity_id, [])
                for event in node.av_events.events:
                    msg = AVMessage(event.msg_type, event.text, event.location, event.source_id, event.message_templates, event.target_id)
                    o_node.add_or_attach_component("av_messages", None)
                    o_node.av_messages.msg.append(msg)
            node.remove_component("av_events")
                
        
        
        