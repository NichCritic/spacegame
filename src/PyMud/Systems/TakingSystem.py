from Systems.AVEvent import AVEvent
from Systems.NetworkMessageSystem import NetworkMessage


class TakingSystem(object):
    '''
    Generates annoying ticks that everyone with a network connection gets (Debug)
    '''

    def __init__(self, node_factory):
        self.node_factory = node_factory

    def get_nodes(self):
        return self.node_factory.create_node_list(["location", "taking", "container"])

    def create_av_event_data(self, location, taking, target):
        event = AVEvent("taking", None, location.detach(),
                        taking.entity_id, taking.format, target)
        return event

    def object_is_held(self, node):
        return node.container.type == 'held'

    def process(self):
        self.nodes = self.get_nodes()
        for node in self.nodes:
            for t_name, t_id in node.taking.target.items():
                print(t_id)
                taken_object = self.node_factory.create_node(
                    t_id, ['names', 'container'])
                if self.object_is_held(taken_object):
                    out_msg = NetworkMessage(node.id, "You can't pick up the {thing} because it's held by {person}".format(
                        thing=taken_object.names.name, person=taken_object.container.parent.entity_id))
                    node.add_or_attach_component("network_messages", {})
                    node.network_messages.msg.append(out_msg)

                # Todo: Capacity

                else:
                    # Pick up the object so that it moves with the player and
                    # doesn't appear in the room
                    taken_object.container.parent_id = node.container.id
                    taken_object.container.type = "held"

                    room_node = self.node_factory.create_node(
                        node.location.room, [])
                    av_event_data = self.create_av_event_data(
                        node.location, node.taking, t_id)
                    print("Taking system got message from " + node.id)
                    room_node.add_or_attach_component("av_events", None)
                    room_node.av_events.events.append(av_event_data)

            node.remove_component("taking")
