

def damage(node, damage):
	node.health.hp -= damage

def damage_over_time(node, damage, tick, end):
	node.add_or_attach_component("damage_over_time", {"damage":damage, "tick":tick, "end":end})

def listen_for_target(rune, on_target):
	rune.add_or_attach_component("listening", {"on_message":on_target})
