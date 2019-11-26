from Systems.system import System
import math
from itertools import takewhile
import logging


class Vector():

    def __init__(self, x, y):
        self.x = x
        self.y = y


class PhysicsPacket():

    def __init__(self):
        self.rotation = 0
        self.force = Vector(0, 0)
        self.dt = 0
        self.time = 0
        self.brake = True

    def to_dict(self):
        return {
            "rotation": self.rotation,
            "force": {"x": self.force.x, "y": self.force.y},
            "dt": self.dt,
            "time": self.time,
            "brake": self.brake
        }


class InputSystem(System):

    manditory = ["player_input", "rotation", "physics_update"]
    handles = []

    def get_unhandled_input(self, input_data_list):
        rev_list = reversed(input_data_list)
        unprocessed = takewhile(lambda l: not l["was_processed"], rev_list)
        unprocessed_list = list(unprocessed)
        return reversed(unprocessed_list)

    def handle(self, node):
        # logging.info(f"input processing {node.id}")
        packets = []

        inputs = self.get_unhandled_input(node.player_input.data)
        rot = node.rotation.rotation

        for inp in inputs:
            dt = inp['dt']

            leftrot = rot - 1 / 200 * dt
            rightrot = rot + 1 / 200 * dt

            p = PhysicsPacket()
            p.rotation = leftrot if inp[
                "left"] else (rightrot if inp["right"] else rot)
            rot = p.rotation

            p.force.x = math.sin(p.rotation) * \
                dt * 0.015 if inp["thrust"] else 0
            p.force.y = - \
                math.cos(p.rotation) * dt * \
                0.015 if inp["thrust"] else 0

            p.time = inp['time']
            p.dt = inp['dt']
            p.brake = inp['brake']

            packets.append(p)

            # TODO: Firing rate should come from weapon stats
            if inp['shoot'] or node.has("shooting"):

                node.add_or_attach_component('shooting', {'firing_rate': 200})
                node.shooting.inputs.append(
                    {'shooting': inp['shoot'], 'dt': inp['dt']})

            if inp['mining']:
                node.add_or_attach_component('mining', {'time': p.time})
            else:
                if node.has("mining"):
                    node.remove_component("mining")

            inp["was_processed"] = True

        node.physics_update.packets.extend(packets)
