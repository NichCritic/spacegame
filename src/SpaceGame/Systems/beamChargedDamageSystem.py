from Systems.system import System
import time
import logging
import math

class BeamChargedDamageSystem(System):
    """
    Handles the colliding state by ignoring it, in case other systems haven't handled it, 
    so that collisions don't build up cycle by cycle
    """

    mandatory = ["position", "rotation", "beam", "charged", "proximity"]
    optional = []
    handles = []

    def __init__(self, node_factory):
        self.node_factory = node_factory

    def handle(self, node):
        possible_colliders = self.node_factory.create_node_list(["position", "area", "health"], entity_ids= node.proximity.proximity_map.keys())

        #Find the unit vector for the beam
        u_x = math.sin(node.rotation.rotation)
        u_y = -math.cos(node.rotation.rotation)

        for c_node in possible_colliders:
            c_x = c_node.position.x - node.position.x
            c_y = c_node.position.y - node.position.y

            adotb = c_x * u_x + c_y * u_y

            if adotb < 0:
                #Beam is behind the ship
                continue

            p_x = adotb * u_x
            p_y = adotb * u_y

            t_x = c_x - p_x
            t_y = c_y - p_y

            len_p = math.sqrt(p_x**2 + p_y**2) 
            len_t = math.sqrt(t_x**2 + t_y**2)

            if len_p - c_node.area.radius > node.beam.length:
                #Beam is too short to reach c_node
                continue

            if len_t - c_node.area.radius > node.beam.width:
                #Beam is too skinny to reach c_node
                continue

            c_node.health.health -= 20

            if c_node.health.health <= 0:
                c_node.add_or_attach_component("dead", {})


            
