from Systems.system import System
import math
import time


class PhysicsSystem(System):

    manditory = ["player_input", "position", "velocity",
                 "mass", "acceleration", "force", "rotation", "physics_update"]
    handles = []

    def handle(self, node):
        last_update = node.physics_update.last_update
        now = time.time()
        dt = now - last_update

        if dt <= 0:
            return

        inp = node.player_input.data
        pos = node.position
        vel = node.velocity
        mass = node.mass.mass
        rot = node.rotation.rotation

        leftrot = rot - 1 / mass * dt
        rightrot = rot + 1 / mass * dt

        node.rotation.rotation = rightrot if inp["right"] else (
            leftrot if inp["left"] else rot)

        node.force.x = math.sin(node.rotation.rotation) * \
            dt if inp["thrust"] else 0
        node.force.y = -math.cos(node.rotation.rotation) * \
            dt if inp["thrust"] else 0

        node.acceleration.x = node.force.x / mass
        node.acceleration.y = node.force.y / mass

        node.velocity.x = vel.x + node.acceleration.x * dt
        node.velocity.y = vel.y + node.acceleration.y * dt

        node.position.x = pos.x + node.velocity.x * dt
        node.position.y = pos.y + node.velocity.y * dt

        node.physics_update.last_update = now
