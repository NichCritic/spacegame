'''
Created on 2013-11-12

@author: Nich
'''


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


def create(player_node, target=None, **kwargs):
    player_node.add_component("creating", {})


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
    "create": {"function": create,
},
    "take": {"function": take, "messages":[([("visibility",60), ("is_caller")], ["You take {target}"]),
                                           ([("visibility",60)], ["{player} takes {target}"])
                                          ]},

    "drop": {"function": drop, "messages":[([("visibility",60), ("is_caller")], ["You drop {target}"]),
                                           ([("visibility",60)], ["{player} dropped {target}"])
                                          ]}




}
