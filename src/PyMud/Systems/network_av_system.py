'''
Created on 2013-11-22

@author: Nich
'''

from Systems.NetworkMessageSystem import NetworkMessage


class NetworkAVSystem(object):
    '''
    classdocs
    '''
    def __init__(self, node_factory):
        
        
        self.node_factory = node_factory
        
        

    def get_nodes(self):
        return self.node_factory.create_node_list(["senses", "location", "av_messages"], optional = ["network_messages"])

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
            
    def satisfies_requirement(self, node, message, req):
        print("testing {}".format(req)) 
        if len(req) == 1:
            type = req[0]
            if type == "targeted":
                return not message.target_id == None
            if type == "is_caller":
                return node.id == message.source_id
            if type == "is_target":
                return node.id == message.target_id
        if len(req) == 2:
            type, value = req
            node_dist = self.distance(node.location, message.location)
            if type == "loudness":
                return node.senses.hearing+value > node_dist
            if type == "visibility":
                return node.senses.sight+value > node_dist
                

                
    def process(self):

        nodes = self.get_nodes()
        for node in nodes:
            print('Network AV System got message from {}'.format(node.id))
            #TODO: maybe add code to follow exits, but for now just make sure we're in the same room
            for message in node.av_messages.msg:
                print(message, node)
                
                print("testing rooms are the same: "+message.location.room+", "+node.location.room)
                if not message.location.room == node.location.room:
                    continue
                
                print("testing requirements")
                for requirements, messages in message.message_templates:
                    reqs_satisfied = [self.satisfies_requirement(node, message, req) for req in requirements]
                    
                    if(all(reqs_satisfied)):
                        for msg in messages:
                            out_msg = NetworkMessage(node.id, msg.format(player = message.source_id, target = message.target_id, text = message.text))
                            network_msg_nodes = nodes.subset(["network_messages"])
                            if not (node in network_msg_nodes):
                                node.add_component("network_messages", {})
            
                            node.network_messages.msg.append(out_msg)
                            
                        break
            node.remove_component("av_messages")
                
                    
                
                
            
            
            
            
            
            
            
    