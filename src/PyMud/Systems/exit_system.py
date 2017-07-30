
from Systems.NetworkMessageSystem import NetworkMessage
'''
Created on 2014-03-22

@author: Nich
'''


class ExitSystem(object):
    '''
    classdocs
    '''

    def __init__(self, node_factory):
        '''
        Constructor
        '''
        self.node_factory = node_factory

    def get_nodes(self):
        return self.node_factory.create_node_list(["container", "location", "exiting"])

    def get_path(self):
        pass

    def path_clear(self, path):
        return True

    def process(self):
        nodes = self.get_nodes()
        for node in nodes:
            exit_id = list(node.exiting.target.items())[0][1]
            exit_node = self.node_factory.create_node(
                exit_id, ["names"], ["exit"])
            if(exit_node.has("exit")):
                destination_id = exit_node.exit.dest_id

                loc_node = self.node_factory.create_node(
                    destination_id, ['names', 'container'])

                node.location.room = destination_id
                node.container.parent_id = loc_node.container.id

                out_msg = NetworkMessage(node.id, "You walk through the {exit} into the {room}".format(
                    exit=exit_node.names.name, room=loc_node.names.name))

                # TODO: should be an av mesage
                node.add_or_attach_component("network_messages", {})
                node.network_messages.msg.append(out_msg)
                node.add_or_update_component("looking", {})
            else:
                out_msg = NetworkMessage(
                    node.id, "{exit} is not an exit".format(exit=exit_node.names.name))

                # TODO: should be an av mesage
                node.add_or_attach_component("network_messages", {})
                node.network_messages.msg.append(out_msg)
                node.add_or_update_component("looking", {})
                pass

            node.remove_component("exiting")
