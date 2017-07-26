from Systems.AVEvent import AVEvent
from Systems.NetworkMessageSystem import NetworkMessage


class DroppingSystem(object):
    '''
    Generates annoying ticks that everyone with a network connection gets (Debug)
    '''

    def __init__(self, node_factory):
        self.node_factory = node_factory

    def get_nodes(self):
        return self.node_factory.create_node_list(["location", "dropping", "container"], ["holding"])

    def create_av_event_data(self, location, dropping):
        event = AVEvent("dropping", None, location,
                        dropping.entity_id, dropping.format, dropping.target)
        return event

    def object_is_held_by(self, object, held_by):
        print('Checking heldby')
        print('--object--')
        print(object)
        print('--held_by--')
        print(held_by)
        if object.has('held_by') and held_by.has('holding'):
            print("components are in place")
            if object.held_by.holding_entity_id == held_by.id and held_by.holding.held_entity_id == object.id:
                return True
            print("{0} {1}".format(object.held_by.holding_entity_id, held_by.holding.held_entity_id))


    def process(self):
        self.nodes = self.get_nodes()
        for node in self.nodes:
            for t_name, t_id in node.dropping.target.items():
                print(t_id)

                dropped_object = self.node_factory.create_node(t_id, ['names', 'container'], ['held_by'])
                if self.object_is_held_by(dropped_object, node):

                    dropped_object.remove_component("held_by")

                    room_node = self.node_factory.create_node(
                        node.location.room, [])
                    av_event_data = self.create_av_event_data(
                        node.location, node.dropping)
                    print("Dropping system got message from "+node.id)
                    room_node.add_or_attach_component("av_events", None)
                    room_node.av_events.events.append(av_event_data)

                    node.remove_component("holding")
                    #Put the object in the same room as the node
                    dropped_object.container.parent_id = node.container.parent_id

                else:
                    dropped_object.add_or_attach_component('held_by', None)
                    out_msg = NetworkMessage(node.id, "You can't drop the {thing}".format(
                        thing=dropped_object.names.name))
                    node.add_or_attach_component("network_messages", {})
                    node.network_messages.msg.append(out_msg)

            node.remove_component("dropping")
