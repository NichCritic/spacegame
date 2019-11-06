from Systems.system import System
import time

class CollisionDamageSystem(System):
    """
    Handles the colliding state by ignoring it, in case other systems haven't handled it, 
    so that collisions don't build up cycle by cycle
    """

    manditory = ["colliding", "collision_damage"]
    optional = []
    handles = ["colliding"]

    def __init__(self, node_factory):
        self.node_factory = node_factory

    def handle(self, node):
        for collision in node.colliding.collisions:
            c_node = self.node_factory.create_node(
                collision["collider"], [], ["health"])

            # Another system could have removed the node before we got to it
            if not c_node.has("health"):
                continue

            # TODO: This is kind of crude. Should really add a damaged state to the node to give a chance
            # For other systems to respond
            c_node.health.health -= node.collision_damage.damage

            if c_node.health.health <= 0:
                now = time.time() * 1000
                c_node.add_or_attach_component('position', {})
                pos = c_node.position
                c_node.remove_all_components()
                c_node.add_or_update_component('type', {'type': 'explosion'})
                c_node.add_or_update_component('position', {'x':pos.x, 'y':pos.y})
                c_node.add_or_update_component('expires', {
                    'expiry_time_ms': 5000,
                    'creation_time': now
                })