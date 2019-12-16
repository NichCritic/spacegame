from Systems.system import System


class ApplyUpgradeSystem(System):
    """
    Handles the colliding state by ignoring it, in case other systems haven't handled it, 
    so that collisions don't build up cycle by cycle
    """

    mandatory = ["apply_upgrade"]
    optional = []
    handles = ["apply_upgrade"]

    def __init__(self, node_factory, upgrades):
        self.node_factory = node_factory
        self.upgrades = upgrades

    def handle(self, node):
        node.add_or_attach_component("applied_upgrades", {})
        upgrade_name = node.apply_upgrade.upgrade_name
        upgrade = self.upgrades[upgrade_name]

        # TODO: Upgrades will eventually need data
        data = {}
        node.applied_upgrades.upgrades[upgrade_name] = data
        upgrade['fn'](node, **data)
