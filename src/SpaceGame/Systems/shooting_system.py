from Systems.system import System
import math
import time
import logging


class ShootingSystem(System):

    mandatory = ["shooting", "position",
                 "velocity", "rotation", "weapon", "physics_update"]
    optional = ["player_controlled"]
    # handles = ["shooting"]

    def __init__(self, node_factory, weapons):
        super().__init__(node_factory)
        self.weapons = weapons

    def handle(self, node):
        node.add_or_attach_component("shooting_vars", {})

        weapon_fn = self.weapons[node.weapon.type]

        inputs = node.shooting.inputs
        firing_rate = node.weapon.firing_rate

        now = time.time() * 1000
        dt_last_update = now - node.shooting_vars.last_update

        running_time = min(node.shooting_vars.residual_cooldown + dt_last_update,
                           firing_rate) if node.shooting_vars.residual_cooldown is not None else firing_rate
        logging.info(running_time)
        total_time = 0
        bullets_fired = node.shooting_vars.bullets_fired

        for inp in inputs:
            dt = inp["dt"]
            if inp["shooting"]:
                if running_time + dt >= firing_rate:
                    logging.info("firing shots")
                    weapon_fn(self.node_factory, node,
                              total_time, bullets_fired, inp["shooting"], last_update = node.shooting_vars.last_update)
                    running_time -= firing_rate
                    bullets_fired += 1
            else:
                # if running_time + dt >= firing_rate:
                weapon_fn(self.node_factory, node,
                          total_time, bullets_fired, inp["shooting"])
            running_time += dt
            total_time += dt

        node.shooting_vars.last_update = time.time() * 1000
        node.shooting_vars.bullets_fired = bullets_fired
        node.shooting_vars.residual_cooldown = running_time
