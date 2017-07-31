
from Systems.NetworkMessageSystem import NetworkMessage
'''
Created on 2014-03-22

@author: Nich
'''


class EnteringSystem(object):
    '''
    classdocs
    '''

    def __init__(self, node_factory):
        '''
        Constructor
        '''
        self.node_factory = node_factory

    def get_nodes(self):
        return self.node_factory.create_node_list(["container", "location", "entering"])

    def get_path(self):
        pass

    def path_clear(self, path):
        return True

    def process(self):
        nodes = self.get_nodes()
        for node in nodes:
            room_id = list(node.entering.target.items())[0][1]

            loc_node = self.node_factory.create_node(
                room_id, ['names', 'container'])

            node.location.room = room_id
            node.container.parent_id = loc_node.container.id

            out_msg = NetworkMessage(node.id, "You move into the {room}".format(
                room=loc_node.names.name))

            # TODO: should be an av mesage
            node.add_or_attach_component("network_messages", {})
            node.network_messages.msg.append(out_msg)
            node.add_or_update_component("looking", {})

            node.remove_component("entering")
