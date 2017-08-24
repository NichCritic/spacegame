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
                return message.target_id is not None
            if type == "is_caller":
                return node.id == message.source_id
            if type == "is_target":
                return node.id == message.target_id
        if len(req) == 2:
            type, value = req
            if type == "loudness":
                return node.senses.hearing > value
            if type == "visibility":
                return node.senses.sight > value

    def format_text(self, message, text):
        print('The message is {}'.format(text))
        if message.source_id is None:
            source = "No one"
        else:
            source_node = self.node_factory.create_node(
                message.source_id, ['names'])
            source = source_node.names.name

        if message.target_id is None:
            target = "Nothing"
        else:
            target_node = self.node_factory.create_node(
                message.target_id, ['names'])
            target = target_node.names.name

        return text.format(player=source,
                           target=target,
                           text=message.text,
                           **message.kwargs)

    def send_network_message(self, node, data):
        out_msg = NetworkMessage(node.id, data)
        node.add_or_attach_component("network_messages", {})
        node.network_messages.msg.append(out_msg)

    def process(self):
        super().process()

    def handle(self, node):

        for event in node.av_events.events:
            for requirements, texts in event.message_templates:
                reqs_satisfied = [self.satisfies_requirement(
                    node, event, req) for req in requirements]

                if(all(reqs_satisfied)):
                    for text in texts:
                        data = self.format_text(event, text)
                        self.send_network_message(node, data)
                    break
            event.handle()
