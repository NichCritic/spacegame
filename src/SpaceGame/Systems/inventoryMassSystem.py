from Systems.system import System
import math
import time


class InventoryMassSystem(System):

    mandatory = ["inventory", "mass"]
    handles = []

    def __init__(self, node_factory):
        self.node_factory = node_factory
        self.sim_time = 0

    def handle(self, node):
        inv_mass = 50 * sum([i["qty"]
                             for _, i in node.inventory.inv.items() if "qty" in i])

        node.add_or_attach_component("inventory_mass", {})
        node.inventory_mass.inventory_mass = inv_mass
