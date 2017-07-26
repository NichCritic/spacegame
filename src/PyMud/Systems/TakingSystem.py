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

    def create_av_event_data(self, location, taking):
        event = AVEvent("taking", None, location,
                        taking.entity_id, taking.format, taking.target)
        return event

    def object_is_held(self, node):
        return node.entity_has('held_by')

    def player_is_holding(self, node):
        return node.entity_has('holding')

    def process(self):
        self.nodes = self.get_nodes()
        for node in self.nodes:
            for t_name, t_id in node.taking.target.items():
                print(t_id)
                taken_object = self.node_factory.create_node(
                    t_id, ['names', 'container'])
                if self.object_is_held(taken_object):
                    taken_object.add_or_attach_component('held_by', None)
                    out_msg = NetworkMessage(node.id, "You can't pick up the {thing} because it's held by {person}".format(thing=taken_object.names.name, person=taken_object.held_by.holding_entity_id))
                    node.add_or_attach_component("network_messages", {})
                    node.network_messages.msg.append(out_msg)

                elif self.player_is_holding(node):

                    node.add_or_attach_component('holding', None)
                    out_msg = NetworkMessage(node.id, "You can't pick up the {thing} because you are already holding {thing2}".format(thing=taken_object.names.name, thing2 = node.holding.held_entity_id))
                    node.add_or_attach_component("network_messages", {})
                    node.network_messages.msg.append(out_msg)

                else:
                    taken_object.add_or_update_component(
                        "held_by", {"holding_entity_id": node.id})

                    #Pick up the object so that it moves with the player and doesn't appear in the room
                    taken_object.container.parent_id = node.container.id

                    room_node = self.node_factory.create_node(
                        node.location.room, [])
                    av_event_data = self.create_av_event_data(
                        node.location, node.taking)
                    print("Taking system got message from "+node.id)
                    room_node.add_or_attach_component("av_events", None)
                    room_node.av_events.events.append(av_event_data)

                    node.add_or_update_component(
                        "holding", {"held_entity_id": t_id})

            
                    

            node.remove_component("taking")