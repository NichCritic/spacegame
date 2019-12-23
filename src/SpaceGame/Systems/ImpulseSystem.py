from Systems.system import System
import math
import time
import logging


class ImpulseSystem(System):

    mandatory = ["impulses"]
    optional = []
    handles = ["impulses"]

    def __init__(self, node_factory):
        self.node_factory = node_factory
        self.sim_time = 0

    def handle(self, node):
        node.add_or_attach_component("player_input", {})

        left = node.impulses.left >= 100 and node.impulses.left > node.impulses.right
        right = node.impulses.right >= 100 and node.impulses.right > node.impulses.left
        shoot = node.impulses.shoot >= 100
        thrust = node.impulses.thrust >= 100 and node.impulses.thrust > node.impulses.brake
        brake = node.impulses.brake >= 100 and node.impulses.brake > node.impulses.thrust
        mine = node.impulses.mine >= 100

        node.player_input.data.extend([{
            "left": left,
            "right": right,
            "dt": 50,
            "time": time.time() * 1000,
            "shoot": shoot,
            "thrust": thrust,
            "mining": mine,
            "brake": brake,
            "was_processed": False
        }])
