'''
Created on 2013-11-21

@author: Nich
'''
import uuid
import tornado
from tornado import template
import os


class NetworkMessage(object):

    def __init__(self, id, msg):
        self.id = id
        self.msg = msg

    def __repr__(self):
        return "<" + str(self.id) + ">:<" + self.msg + ">"


class NetworkMessageSystem(object):

    def __init__(self, node_factory, player_factory):
        self.node_factory = node_factory
        self.player_factory = player_factory
        message_template_loader = template.Loader(
            os.path.join(os.getcwd(), "templates"))
        self.message_template = message_template_loader.load("message.html")

    def get_nodes(self):
        return self.node_factory.create_node_list(["player_controlled", "network_messages"])

    def send_message(self, message_buffer, message):
        msg = message.msg
        html_message = {
            "id": str(uuid.uuid4()),
            "from": "System",
            "body": msg.split('\n')}
        html_message["html"] = tornado.escape.to_basestring(
            self.message_template.generate(message=html_message))
        message_buffer.new_messages([html_message])

    def process(self):
        players = self.player_factory.get_players()

        for node in self.get_nodes():

            p = node.player_controlled.pid
            '''Sometimes we have nodes with temporary or false ID's. Don't send
             messages to those'''

            print("network messages {}".format(type(p)))
            if p in players:
                print("happens")
                message_buffer = players[p].message_buffer
                print("also happens")
                print(node.network_messages.msg)
                for message in node.network_messages.msg:
                    self.send_message(message_buffer, message)
            node.remove_component("network_messages")


'''
class NetworkMessageSystem(object):
    

    def __init__(self, node_factory, player_factory, Session):
        #Todo: Maybe change to use network component if that isn't silly in the future
        self.message_buffers = {}
        self.player_factory = player_factory
        self.node_factory = node_factory
        players = player_factory.get_players()
        session = Session()
        
        for node in node_factory.create_node_list(["player_controlled"]):
            p = node.player_controlled.pid
            if p in players:
                self.message_buffers[node.id] = players[p].message_buffer
        
        
        
        self.network_message_queue = Queue()
        message_template_loader = template.Loader(os.path.join(os.path.dirname("./"), "templates"))
        self.message_template = message_template_loader.load("message.html")                                                
        
        session.commit()
        
    
    def refresh_buffers(self):
        self.message_buffers = {}
        players = self.player_factory.get_players()
        for node in self.node_factory.create_node_list(["player_controlled"]):
            p = node.player_controlled.pid
            #Sometimes we have nodes with temporary or false ID's. Don't send messages to those
            if p in players:
                self.message_buffers[node.id] = players[p].message_buffer
        #print(self.message_buffers)
    
    def handle_network_messages(self):
        self.refresh_buffers()
        while not self.network_message_queue.empty():
            message = self.network_message_queue.get()
            id = message.id
            msg = message.msg
            if id in self.message_buffers:
                message = {
                            "id": str(uuid.uuid4()),
                            "from": "System",
                            "body": msg,
                            }
                
                message["html"] = tornado.escape.to_basestring(self.message_template.generate(message=message))
                self.message_buffers[id].new_messages([message])
                 
            
'''
