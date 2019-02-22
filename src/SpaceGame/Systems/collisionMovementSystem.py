from Systems.system import System


class CollisionMovementSystem(System):
    """
    Handles the colliding state by ignoring it, in case other systems haven't handled it, 
    so that collisions don't build up cycle by cycle
    """

    manditory = ["colliding", "position", "force", "mass", "velocity"]
    optional = ["inventory_mass"]

    def __init__(self, node_factory):
        self.node_factory = node_factory

    def handle(self, node):
        for collision in node.colliding.collisions:
            c_node = self.node_factory.create_node(
                collision["collider"], ["position"])

            x = (node.position.x - c_node.position.x) / collision["dist"]
            y = (node.position.y - c_node.position.y) / collision["dist"]

            node.position.x = node.position.x + x * collision["delta"]
            node.position.y = node.position.y + y * collision["delta"]

            mom1_x = node.velocity.x * node.mass.mass + \
                (node.inventory_mass.inventory_mass if node.has(
                    "inventory_mass") else 0)
            mom1_y = node.velocity.y * node.mass.mass + \
                (node.inventory_mass.inventory_mass if node.has(
                    "inventory_mass") else 0)

            if c_node.entity_has('mass') and c_node.entity_has('velocity'):
                c_node.add_or_attach_component("mass", {})
                c_node.add_or_attach_component("inventory_mass", {})
                c_node.add_or_attach_component("velocity", {})
                mom2_x = c_node.velocity.x * \
                    (c_node.mass.mass + c_node.inventory_mass.inventory_mass)
                mom2_y = c_node.velocity.y * \
                    (c_node.mass.mass + c_node.inventory_mass.inventory_mass)

                node.force.x = -(node.force.x + (mom1_x + mom2_x) / 2)
                node.force.y = -(node.force.y + (mom1_x + mom2_y) / 2)
            else:
                node.force.x = mom1_x
                node.force.y = mom1_y
