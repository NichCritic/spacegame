from Systems.system import System
import time
import math
import logging


class CollisionVelocityDamageSystem(System):
    """
    Handles the colliding state by ignoring it, in case other systems haven't handled it, 
    so that collisions don't build up cycle by cycle
    """

    manditory = ["colliding"]
    optional = []
    handles = []

    def __init__(self, node_factory):
        self.node_factory = node_factory

    def handle(self, node):
        for collision in node.colliding.collisions:
            c_node = self.node_factory.create_node(
                collision["collider"], [], ["health", "velocity", "collision_velocity_damage"])

            # Another system could have removed the node before we got to it
            if not c_node.has("health") or not c_node.has("velocity") or not c_node.has("collision_velocity_damage"):
                continue

            # TODO: This is kind of crude. Should really add a damaged state to the node to give a chance
            # For other systems to respond
            v_min = c_node.collision_velocity_damage.min_velocity
            v_max = c_node.collision_velocity_damage.max_velocity
            damage = c_node.collision_velocity_damage.damage

            velocity = math.sqrt(c_node.velocity.x**2 + c_node.velocity.y**2)

            scaled_damage = damage * ((velocity - v_min) / (v_max - v_min))

            scaled_damage = max(0, scaled_damage)

            logging.info(f"----------------Velocity: {velocity}")
            c_node.health.health -= scaled_damage

            if c_node.health.health <= 0:
                now = time.time() * 1000
                c_node.add_or_attach_component('position', {})
                pos = c_node.position
                c_node.remove_all_components()
                c_node.add_or_update_component('type', {'type': 'explosion'})
                c_node.add_or_update_component(
                    'position', {'x': pos.x, 'y': pos.y})
                # c_node.add_or_update_component(
                #     'health', {'health': 0, 'max_health': 0})
                c_node.add_or_update_component('expires', {
                    'expiry_time_ms': 1000,
                    'creation_time': now
                })
                c_node.add_or_attach_component('area', {'radius': 25})
                c_node.add_or_attach_component(
                    'animated', {'update_rate': 200})
