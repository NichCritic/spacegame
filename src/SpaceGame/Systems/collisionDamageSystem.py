from Systems.system import System
import time
import logging

class CollisionDamageSystem(System):
    """
    Handles the colliding state by ignoring it, in case other systems haven't handled it, 
    so that collisions don't build up cycle by cycle
    """

    mandatory = ["colliding", "collision_damage"]
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
            logging.info(f"{c_node.id} colliding with {node.id}")
            c_node.health.health -= node.collision_damage.damage

            if c_node.health.health <= 0:
                c_node.add_or_attach_component("dead", {})
