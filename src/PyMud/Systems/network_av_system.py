'''
Created on 2013-11-22

@author: Nich
'''

from Systems.NetworkMessageSystem import NetworkMessage
from Systems.system import System


class NetworkAVSystem(System):
    '''
    classdocs
    '''

    manditory = ["senses", "location", "av_events"]
    optional = ["network_messages"]
    handles = []

    def satisfies_requirement(self, node, message, req):
        print("testing {}".format(req))
        if len(req) == 1:
            type = req[0]
            if type == "targeted":
                return "target_id" in message.data
            if type == "is_caller":
                return "source_id" in message.data and node.id == message.data['source_id']
            if type == "is_target":
                return "source_id" in message.data and node.id == message.data['target_id']
        if len(req) == 2:
            type, value = req
            if type == "loudness":
                return node.senses.hearing > value
            if type == "visibility":
                return node.senses.sight > value

    def send_network_message(self, node, data):
        out_msg = NetworkMessage(node.id, data)
        node.add_or_attach_component("network_messages", {})
        node.network_messages.msg.append(out_msg)

    def handle(self, node):

        for event in node.av_events.events:
            for requirements, texts in event.format:
                reqs_satisfied = [self.satisfies_requirement(
                    node, event, req) for req in requirements]

                if(all(reqs_satisfied)):
                    for text in texts:
                        f_text = text.format(**event.data)
                        self.send_network_message(node, f_text)
                    break
            event.handle()
