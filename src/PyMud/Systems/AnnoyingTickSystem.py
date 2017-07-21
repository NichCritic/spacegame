'''
Created on 2013-11-21

@author: Nich
'''
from Systems.NetworkMessageSystem import NetworkMessage


class AnnoyingTickSystem(object):
    '''
    Generates annoying ticks that everyone with a network connection gets (Debug)
    '''


    def __init__(self, node_factory):
        self.node_factory = node_factory
        
        
        
    
    
    def get_nodes(self):
        return self.node_factory.create_node_list(["player_controlled"], optional = ["network_messages"])
            
        
        
    def send_annoying_tick(self):
        self.nodes = self.get_nodes()
        print('annoying tick dispatch to '+str(len(self.nodes))+' users') 
        for node in self.nodes:
            network_msg_nodes = self.nodes.subset(["network_messages"])
            
            if not (node in network_msg_nodes):
                node.add_component("network_messages", {})
            
            node.network_messages.msg.append(NetworkMessage(node.id, "****TICK****"))
        