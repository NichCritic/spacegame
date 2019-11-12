from Systems.system import System
from Systems.input_system import PhysicsPacket
import time


class CollisionMovementSystem(System):
    """
    Handles the colliding state by ignoring it, in case other systems haven't handled it, 
    so that collisions don't build up cycle by cycle
    """

    manditory = ["colliding", "position",
                 "force", "rotation", "mass", "velocity"]
    optional = ["inventory_mass"]
    handles = ["colliding"]

    def __init__(self, node_factory):
        self.node_factory = node_factory

    def handle(self, node):
        for collision in node.colliding.collisions:
            c_node = self.node_factory.create_node(
                collision["collider"], ["force", "rotation"], ["position"])

            # Another system could have removed the node before we got to it
            if not c_node.has("position"):
                continue

            x = (node.position.x - c_node.position.x) / collision["dist"]
            y = (node.position.y - c_node.position.y) / collision["dist"]

            node.position.x = node.position.x + x * collision["delta"]
            node.position.y = node.position.y + y * collision["delta"]

            mom1_x = node.velocity.x**2 * node.mass.mass + \
                (node.inventory_mass.inventory_mass if node.has(
                    "inventory_mass") else 0)
            mom1_y = node.velocity.y**2 * node.mass.mass + \
                (node.inventory_mass.inventory_mass if node.has(
                    "inventory_mass") else 0)

            node.velocity.x = 0
            node.velocity.y = 0

            if c_node.entity_has('mass') and c_node.entity_has('velocity'):
                c_node.add_or_attach_component("mass", {})
                c_node.add_or_attach_component("inventory_mass", {})
                c_node.add_or_attach_component("velocity", {})
                mom2_x = c_node.velocity.x**2 * \
                    (c_node.mass.mass + c_node.inventory_mass.inventory_mass)
                mom2_y = c_node.velocity.y**2 * \
                    (c_node.mass.mass + c_node.inventory_mass.inventory_mass)

                node.add_or_attach_component("physics_update", {})
                p = PhysicsPacket()
                p.rotation = node.rotation.rotation
                p.force.x = node.force.x + ((mom1_x + mom2_x) / 2) * x
                p.force.y = node.force.y + ((mom1_x + mom2_y) / 2) * y
                p.dt = 1
                p.time = time.time() * 1000
                p.brake = True

                c_node.velocity.x = 0
                c_node.velocity.y = 0

                c_node.add_or_attach_component("physics_update", {})
                p2 = PhysicsPacket()
                p2.rotation = c_node.rotation.rotation
                p2.force.x = c_node.force.x - ((mom1_x + mom2_x) / 2) * x
                p2.force.y = c_node.force.y - ((mom1_x + mom2_y) / 2) * y
                p2.dt = 1
                p2.time = time.time() * 1000
                p2.brake = True

                c_node.physics_update.packets.append(p2)

            else:
                node.add_or_attach_component("physics_update", {})
                p = PhysicsPacket()
                p.rotation = node.rotation.rotation
                p.force.x = node.force.x - mom1_x * x / 2
                p.force.y = node.force.y - mom1_y * y / 2
                p.dt = 5
                p.time = time.time() * 1000
                p.brake = True
                node.physics_update.packets.append(p)

            c_node.remove_component("colliding")
