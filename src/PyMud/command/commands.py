'''
Created on 2013-11-12

@author: Nich
'''
from Systems.NetworkMessageSystem import NetworkMessage


def isa(player_node, targets, text, **kwargs):
    player_node.add_component("changing", {"target": targets, "text": text})


def take(player_node, targets, **kwargs):
    player_node.add_component(
        "taking", {"target": targets, "format": verbs["take"]["messages"]})


def drop(player_node, targets, **kwargs):
    player_node.add_component(
        "dropping", {"target": targets, "format": verbs["drop"]["messages"]})


def say(text, player_node, targets=None, **kwargs):
    player_node.add_component(
        "speaking", {"text": text, "target": targets, "format": verbs["say"]["messages"]})


def look(player_node, targets=None, **kwargs):
    player_node.add_component("looking", {"target": targets})


def enter(player_node, targets, **kwargs):
    player_node.add_component("entering", {"target": targets})


def ascend(player_node, **kwargs):
    player_node.add_component("ascending", {})


def move(player_node, targets, p_type, **kwargs):
    if p_type == 'to':
        move_to(player_node, targets, **kwargs)
    elif p_type == 'through':
        move_through(player_node, targets, **kwargs)


def move_to(player_node, targets, **kwargs):
    player_node.add_component(
        "moving", {"target":targets, "format":verbs["move to"]["messages"]})


def move_through(player_node, targets, **kwargs):
    player_node.add_component("exiting", {"target": targets})


def create(player_node, text, **kwargs):
    player_node.add_component(
        "creating", {"format": verbs["create"]["messages"], "new_name": text})


def help(player_node, **kwargs):
    out_msg = NetworkMessage(player_node.id, '\n'.join(verbs.keys()))
    player_node.add_or_attach_component("network_messages", {})
    player_node.network_messages.msg.append(out_msg)

def write(player_node, rune, targets, **kwargs):
    player_node.add_or_attach_component("writing", {"target":targets, "rune":rune, "format":verbs["write"]["messages"]})


def put_in(player_node, targets, p_type, **kwargs):
    player_node.add_or_attach_component("putting", {"targets":targets, "type":p_type, "format":verbs["put in"]["messages"]})


def put_on(player_node, targets, p_type, **kwargs):
    player_node.add_or_attach_component("putting", {"targets":targets, "type":p_type, "format":verbs["put on"]["messages"]})


def put_under(player_node, targets, p_type, **kwargs):
    player_node.add_or_attach_component("putting", {"targets":targets, "type":p_type, "format":verbs["put under"]["messages"]})


def put(player_node, targets, p_type, **kwargs):
    if p_type == 'in':
        put_in(player_node, targets, p_type, **kwargs)
    if p_type == 'on':
        put_on(player_node, targets, p_type, **kwargs)
    if p_type == 'under':
        put_under(player_node, targets, p_type, **kwargs)

verbs = {"say": {

    "function": say,

    "messages": [([("loudness", 50), ("targeted",), ("is_caller",)], ['You say to {target}, "{text}".']),
                 ([("loudness", 50), ("targeted",), ("is_target",)], [
                     '{player} says to you, "{text}".']),
                 ([("loudness", 50), ("targeted",), ],
                  ['{player} says to {target}, "{text}".']),
                 ([("loudness", 50), ("is_caller",)],
                  ['You say, "{text}".']),
                 ([("loudness", 50)],
                  ['{player} says, "{text}".']),
                 ([("visibility", 60), ("is_caller")],
                  ["You can't hear your own voice!"]),

                 ([("visibility", 60), ("is_caller")], [
                     "{player}'s lips move, but you can't make out what they're saying."])
                 ],

},

    "look": {
    "function": look,
},
"write": {
    "function": write, "messages": [([("visibility", 60), ("is_caller")], ["You inscribe a rune on {target}"]),
                                            ([("visibility", 60)], [
                                                "{player} inscribes a rune on {target}"])
                                            ]
},
    "go": {
      "function": move
},
    "move": {
    "function": move,
},

    "move to": {
    "function": move_to,
    "messages": [([("visibility", 60), ("is_caller")], ["You move to {target}"]),
                                            ([("visibility", 60)], [
                                                "{player} moves by {target}"])
                                            ]
},
    "move through": {
    "function": move_through,
},

    "enter": {
    "function": enter,
},
    "ascend": {
    "function": ascend,
},
    "create": {"function": create, "messages": [([("visibility", 60), ("is_caller")], ["You create a {target}"]),
                                                ([("visibility", 60)], [
                                                    "{player} created a {target}"])
                                                ]},
    "take": {"function": take, "messages": [([("visibility", 60), ("is_caller")], ["You take {target}"]),
                                            ([("visibility", 60)], [
                                                "{player} took {target}"])
                                            ]},

    "drop": {"function": drop, "messages": [([("visibility", 60), ("is_caller")], ["You drop {target}"]),
                                            ([("visibility", 60)], [
                                                "{player} dropped {target}"])
                                            ]},
    "help": {"function": help},
    "isa": {"function": isa},
    "put": {"function": put},
    "put in": {"messages":[([("visibility", 60), ("is_caller")], ["You put the {subject} in the {object}"]),
                                            ([("visibility", 60)], [
                                                "{player} put the {subject} in the {object}"])
                                            ]},
    "put on": {"messages": [([("visibility", 60), ("is_caller")], ["You put the {subject} on the {object}"]),
                                            ([("visibility", 60)], [
                                                "{player} put the {subject} on the {object}"])
                                            ]},
    "put under": {"messages": [([("visibility", 60), ("is_caller")], ["You put the {subject} under the {object}"]),
                                            ([("visibility", 60)], [
                                                "{player} put the {subject} under the {object}"])
                                            ]},




}
