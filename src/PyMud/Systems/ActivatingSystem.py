from Systems.system import System
from Systems.AVEvent import AVEvent
from Systems.NetworkMessageSystem import NetworkMessage


class ActivatingSystem(System):
    '''
    Generates annoying ticks that everyone with a network connection gets (Debug)
    '''
    manditory = ["location", "activating"]

    def create_av_event_data(self, location, activating, target):
        event = AVEvent("activating", None, location.detach(),
                        activating.entity_id, activating.format, target)
        return event

    def handle(self, node):
        for t_name, t_id in node.activating.target.items():
            item_node = self.node_factory.create_node(
                t_id, [], ['rune_data', 'rune_active'])
            if item_node.has('rune_data') and not item_node.has('rune_active'):
                item_node.add_component("rune_active", {})

                out_msg = NetworkMessage(node.id, f"You activate the runes on the {t_name}")
                node.add_or_attach_component("network_messages", {})
                node.network_messages.msg.append(out_msg)

            else:
                out_msg = NetworkMessage(node.id, f"There is nothing to activate on the {t_name}")
                node.add_or_attach_component("network_messages", {})
                node.network_messages.msg.append(out_msg)
        node.remove_component("activating")
