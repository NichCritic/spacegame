from Systems.NetworkMessageSystem import NetworkMessage
import time


def teleport(node_factory, on_hold, held_entity_id, holding_entity_id, new_location):
    node = node_factory.create_node(holding_entity_id, ['location', 'container'])
    loc_node = node_factory.create_node(new_location, ['names', 'container'])
    
    on_hold.data = {'new_location':node.location.room}
    node.location.room = new_location
    node.container.parent_id = loc_node.container.id

    out_msg = NetworkMessage(node.id, "POP! You teleported to {}".format(loc_node.names.name))
    node.add_or_attach_component("network_messages", {})
    node.network_messages.msg.append(out_msg)

scripts = {
	'teleport':teleport
}