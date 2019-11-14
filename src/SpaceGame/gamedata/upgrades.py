#Upgrades are called with node, **data, where data is a dictionary of relevant data to apply the upgrade


def health_upgrade(node, amount):
	node.add_or_attach_component('health', {})
	node.health.max_health += amount

def trishot_weapon_upgrade(node):
	node.add_or_update_component('weapon', {'type': 'triple_shot'})
