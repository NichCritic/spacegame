from Systems.system import System
import math


class InputSystem(System):

    manditory = ["player_input"]
    handles = ["player_input"]

    def handle(self, node):

        offset_state = zip(node.player_input.data, node.player_input.data[1:])

        for s1, s2 in offset_state:
            dt = s2.time - s1.time
            left = s1['left']
            right = s1['right']
            thrust = s1['thrust']
            brake = s1['brake']
            fire = s1['fire']
            time = s1['time']
