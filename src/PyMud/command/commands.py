'''
Created on 2013-11-12

@author: Nich
'''
from Systems.NetworkMessageSystem import NetworkMessage

def take(player_node, targets, **kwargs):
    player_node.add_component("taking", {"target": targets, "format": verbs["take"]["messages"]})


def drop(player_node, targets, **kwargs):
    player_node.add_component("dropping", {"target": targets, "format": verbs["drop"]["messages"]})


def say(text, player_node, targets=None, **kwargs):
    player_node.add_component(
        "speaking", {"text": text, "target": targets, "format": verbs["say"]["messages"]})


def look(player_node, target=None, **kwargs):
    player_node.add_component("looking", {"target": target})


def move(player_node, target=None, **kwargs):
    player_node.add_component(
        "moving", {"x": kwargs["x"], "y": kwargs["y"], "z": kwargs["z"]})


def create(player_node, **kwargs):
    player_node.add_component("creating", {"format": verbs["create"]["messages"]})

def help(player_node, **kwargs):
    out_msg = NetworkMessage(player_node.id, '\n'.join(verbs.keys()))
    player_node.add_or_attach_component("network_messages", {})
    player_node.network_messages.msg.append(out_msg)


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
    "move": {
    "function": move,
},
    "create": {"function": create, "messages":[([("visibility",60), ("is_caller")], ["You create a {target}"]),
                                           ([("visibility",60)], ["{player} created a {target}"])
                                          ]
},
    "take": {"function": take, "messages":[([("visibility",60), ("is_caller")], ["You take {target}"]),
                                           ([("visibility",60)], ["{player} took {target}"])
                                          ]},

    "drop": {"function": drop, "messages":[([("visibility",60), ("is_caller")], ["You drop {target}"]),
                                           ([("visibility",60)], ["{player} dropped {target}"])
                                          ]},
    "help": {"function": help}




}
