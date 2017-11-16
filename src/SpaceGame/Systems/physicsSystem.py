from Systems.system import System
import math
import time
from itertools import takewhile


class PhysicsSystem(System):

    manditory = ["player_input", "position", "velocity",
                 "mass", "acceleration", "force", "rotation", "physics_update"]
    handles = []

    def __init__(self, node_factory):
        self.node_factory = node_factory
        self.sim_time = 0

    def physics(self, node, inp, pos, vel, mass, rot, dt):
        leftrot = rot - 1 / mass * dt
        rightrot = rot + 1 / mass * dt

        node.rotation.rotation = leftrot if inp[
            "left"] else (rightrot if inp["right"] else rot)

        node.force.x = math.sin(node.rotation.rotation) * \
            dt * 0.1 if inp["thrust"] else 0
        node.force.y = - \
            math.cos(node.rotation.rotation) * dt * \
            0.1 if inp["thrust"] else 0

        # print(f"{node.force.y}, {dt}")

        node.acceleration.x = node.force.x / mass
        node.acceleration.y = node.force.y / mass

        # print(f'{node.acceleration.x}, {node.acceleration.y}')

        node.velocity.x = vel.x + node.acceleration.x * dt
        node.velocity.y = vel.y + node.acceleration.y * dt

        if not inp['brake']:
            node.velocity.x = node.velocity.x * (0.99 ** dt)
            node.velocity.y = node.velocity.y * (0.99 ** dt)

        # print(f'{node.velocity.x}, {node.velocity.y}')

        node.position.x = pos.x + node.velocity.x * dt
        node.position.y = pos.y + node.velocity.y * dt

    def get_unhandled_input(self, input_data_list):
        return reversed(list(takewhile(lambda l: not l["was_processed"], reversed(input_data_list))))

    def handle(self, node):

        # Sample clock to find start time
        now = time.time() * 1000
        # Read client user input messages from network
        # Execute client user input messages

        inputlist = self.get_unhandled_input(node.player_input.data)

        # print(list(inputlist))

        for inp in inputlist:
            pos = node.position
            vel = node.velocity
            mass = node.mass.mass
            rot = node.rotation.rotation

            self.physics(node, inp, pos, vel, mass, rot, inp["dt"])

            node.physics_update.last_update = inp["time"]
            inp["was_processed"] = True

        # Simulate server-controlled objects using simulation time from last full pass
        # TODO

        # Sample clock to find end time

        # End time minus start time is the simulation time for the next frame

        # last_update = node.physics_update.last_update
        # last_input = node.player_input.data[-1]["time"]
        # now = time.time() * 1000
        # if last_update < last_input < now:
        #     dt1 = last_input - last_update
        #     dt2 = now - last_input
        # else:
        #     dt1 = -1
        #     dt2 = now - last_update

        # print(f"{dt1}, {dt2}")

        # if dt1 > 0:
        #     prev_inp = node.player_input.data[-2]
        #     # print(inp)
        #     pos = node.position
        #     vel = node.velocity
        #     mass = node.mass.mass
        #     rot = node.rotation.rotation

        #     self.physics(node, prev_inp, pos, vel, mass, rot, dt1)

        #     node.physics_update.last_update = last_input

        # if dt2 <= 0:
        #     return

        # inp = node.player_input.data[-1]
        # pos = node.position
        # vel = node.velocity
        # mass = node.mass.mass
        # rot = node.rotation.rotation

        # self.physics(node, inp, pos, vel, mass, rot, dt2)

        # # print(f'{node.position.x}, {node.position.y}')

        # node.physics_update.last_update = now
