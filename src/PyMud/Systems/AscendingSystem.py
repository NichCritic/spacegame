
from Systems.NetworkMessageSystem import NetworkMessage
'''
Created on 2014-03-22

@author: Nich
'''


class AscendingSystem(object):
    '''
    classdocs
    '''

    def __init__(self, node_factory):
        '''
        Constructor
        '''
        self.node_factory = node_factory

    def get_nodes(self):
        return self.node_factory.create_node_list(["container", "location", "ascending"])

    def get_path(self):
        pass

    def path_clear(self, path):
        return True

    def process(self):
        nodes = self.get_nodes()
        for node in nodes:

            node.location.room = node.container.parent.parent.entity_id
            node.container.parent_id = node.container.parent.parent_id

            room_node = self.node_factory.create_node(
                node.location.room, ["names"])

            out_msg = NetworkMessage(node.id, "You ascend to the {} level of abstraction".format(
                room_node.names.name))

            # TODO: should be an av mesage
            node.add_or_attach_component("network_messages", {})
            node.network_messages.msg.append(out_msg)
            node.add_or_update_component("looking", {})

            node.remove_component("ascending")
