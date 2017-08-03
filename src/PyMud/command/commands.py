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


def move_to(player_node, target, **kwargs):
    player_node.add_component(
        "moving", {"x": kwargs["x"], "y": kwargs["y"], "z": kwargs["z"]})


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
    "isa": {"function": isa}




}
