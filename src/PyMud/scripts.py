from Systems.NetworkMessageSystem import NetworkMessage
import time


def teleport(node_factory, on_hold, held_entity_id, holding_entity_id, new_location):
    node = node_factory.create_node(
        holding_entity_id, ['location', 'container'])
    loc_node = node_factory.create_node(new_location, ['names', 'container'])

    on_hold.data = {'new_location': node.location.room}
    node.location.room = new_location
    node.container.parent_id = loc_node.container.id

    out_msg = NetworkMessage(
        node.id, "POP! You teleported to {}".format(loc_node.names.name))
    node.add_or_attach_component("network_messages", {})
    node.network_messages.msg.append(out_msg)


def luv_aq(node_factory, on_hold, held_entity_id, holding_entity_id):
    print("GO")
    held_node = node_factory.create_node(
        held_entity_id, ['names', 'rune_data'])
    holding_node = node_factory.create_node(holding_entity_id, [], ['mana'])
    rune = held_node.rune_data.rune

    if(holding_node.has('mana')):
        amt = min(holding_node.mana.mana, 10)
        holding_node.mana.mana -= amt
        rune.mana += amt
        out_msg = NetworkMessage(
            holding_node.id, f"A luv rune on {held_node.names.name} flickers and you lose {amt} mana")
        holding_node.add_or_attach_component("network_messages", {})
        holding_node.network_messages.msg.append(out_msg)

    if rune.mana >= rune.max_mana:
        rune.mana = rune.max_mana
        print("calling on_charged")
        held_node.remove_component('on_hold')
        rune.on_charged()
        out_msg = NetworkMessage(
            holding_node.id, f"A luv rune on {held_node.names.name} glows and appears fully charged")
        holding_node.add_or_attach_component("network_messages", {})
        holding_node.network_messages.msg.append(out_msg)


def luv_rel(node_factory, on_hold, held_entity_id, holding_entity_id):
    held_node = node_factory.create_node(
        held_entity_id, ['names', 'rune_data'])
    holding_node = node_factory.create_node(holding_entity_id, [])
    rune = held_node.rune_data.rune

    amt = min(rune.mana, 10)
    rune.mana -= amt
    holding_node.add_or_attach_component('change_health', {'amount': amt * 2})
    out_msg = NetworkMessage(
        holding_node.id, f"A luv rune on {held_node.names.name} glows green for a brief moment")
    holding_node.add_or_attach_component("network_messages", {})
    holding_node.network_messages.msg.append(out_msg)


scripts = {
    'teleport': teleport,
    'luv_aq': luv_aq,
    'luv_rel': luv_rel
}
