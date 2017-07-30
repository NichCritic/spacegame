'''
Created on 2013-11-18

@author: Nich
'''
class CommandContextBuilder(object):
    
    def __init__(self, node_factory, spells):
        self.node_factory = node_factory
        self.spells = spells
    
    def build_command_context(self, source):
        avatar_id = source.avatar_id
        node = self.node_factory.create_node(avatar_id, ["location", "names", "visible_names"])
        command_context = {"player_node":node,
                           "calling_player_id":avatar_id,
                                "calling_player_location": node.location,
                                "names":node.visible_names,
                                "spells": self.spells
                           }
        
        
        
        return command_context