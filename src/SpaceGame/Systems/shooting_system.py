from Systems.system import System
import math
import time
import logging


class ShootingSystem(System):

    manditory = ["shooting", "position",
                 "velocity", "rotation", "physics_update"]
    handles = ["shooting"]

    def create_bullet(self, node, creation_time, count):
        x_vel = math.sin(node.rotation.rotation) * 0.5 + node.velocity.x
        y_vel = -math.cos(node.rotation.rotation) * 0.5 + node.velocity.y

        now = time.time() * 1000
        start_time = node.physics_update.last_update + creation_time

        dt = now - start_time

        if dt < 0:
            dt = 0

        x_pos = node.position.x + \
            math.sin(node.rotation.rotation) * 15 + x_vel * dt
        y_pos = node.position.y - \
            math.cos(node.rotation.rotation) * 15 + y_vel * dt

        # logging.info("Bullets fired: "+str(count))

        return self.node_factory.create_new_node({
            'force': {},
            'acceleration': {},
            'velocity': {'x': x_vel, 'y': y_vel},
            'position': {'x': x_pos, 'y': y_pos},
            'rotation': {'rotation': node.rotation.rotation},
            'area': {'radius': 6},
            'mass': {},
            'server_updated': {},
            'type': {'type': 'bolt'},
            'physics_update': {'last_update': now},
            'state_history': {},
            'expires': {
                'expiry_time_ms': 2000,
                'creation_time': start_time
            },
            "collidable": {},
            "collision_damage": {"damage": 100},
            # "client_sync": {"sync_key": count}
            "no_sync": {}
        })

    def handle(self, node):
        node.add_or_attach_component("shooting_vars", {})

        inputs = node.shooting.inputs
        firing_rate = node.shooting.firing_rate

        now = time.time() * 1000
        dt_last_update = now - node.shooting_vars.last_update

        running_time = min(node.shooting_vars.residual_cooldown + dt_last_update,
                           firing_rate) if node.shooting_vars.residual_cooldown is not None else firing_rate
        # logging.info(running_time)
        total_time = 0
        bullets_fired = node.shooting_vars.bullets_fired

        for inp in inputs:
            dt = inp["dt"]
            if inp["shooting"]:
                if running_time + dt >= firing_rate:
                    self.create_bullet(node, total_time, bullets_fired)
                    running_time -= firing_rate
                    bullets_fired += 1
            running_time += dt
            total_time += dt

        node.shooting_vars.last_update = time.time() * 1000
        node.shooting_vars.bullets_fired = bullets_fired
        node.shooting_vars.residual_cooldown = running_time
