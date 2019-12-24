from Systems.system import System
import logging
import math


class AttachSystem(System):
    """
    Handles the colliding state by ignoring it, in case other systems haven't handled it, 
    so that collisions don't build up cycle by cycle
    """

    mandatory = ["attached"]
    optional = []
    handles = []

    def __init__(self, node_factory):
        self.node_factory = node_factory

    def handle(self, node):
        parent_node = self.node_factory.create_node(
            node.attached.target_id, ["position", "rotation"])

        p_x = parent_node.position.x
        p_y = parent_node.position.y
        p_rot = parent_node.rotation.rotation

        node.add_or_attach_component("position", {})
        node.add_or_attach_component("rotation", {})

        node.position.x = (node.attached.x * math.cos(p_rot) -
                           node.attached.y * math.sin(p_rot)) + p_x
        node.position.y = (node.attached.x * math.sin(p_rot) +
                           node.attached.y * math.cos(p_rot)) + p_y
        node.rotation.rotation = p_rot + node.attached.rotation
