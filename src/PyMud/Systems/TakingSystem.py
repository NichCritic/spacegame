from Systems.system import System
from Systems.av_event_mixin import AVEventMixin
from Systems.NetworkMessageSystem import NetworkMessage


class TakingSystem(System, AVEventMixin):
    manditory = ["names", "location", "taking", "container"]
    handles = ["taking"]

    def object_is_held(self, node):
        return node.container.type == 'held'

    def handle(self, node):
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
                self.av_event(node, {
                              'target': taken_object.names.name, 'player': node.names.name}, node.taking.format)
