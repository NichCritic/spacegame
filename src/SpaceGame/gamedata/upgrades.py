# Upgrades are called with node, **data, where data is a dictionary of
# relevant data to apply the upgrade


def health_upgrade(node):
    node.add_or_attach_component('health', {})
    node.health.max_health += 500

def full_heal(node):
    node.add_or_attach_component('health', {})
    node.health.health = node.health.max_health


def trishot_weapon_upgrade(node):
    node.add_or_update_component('weapon', {'type': 'triple_shot'})

def rootkit_upgrade(node):
	node.add_or_update_component('rooted', {})


upgrades = {
    "trishot": {"name": "Trishot Upgrade", "fn": trishot_weapon_upgrade},
    "health": {"name": "Health Upgrade", "fn": health_upgrade},
    "heal": {"name": "Fully Heal ship", "fn": full_heal},
    "rootkit": {"name": "Rootkit", "fn": rootkit_upgrade}
}
