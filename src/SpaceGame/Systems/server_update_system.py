from Systems.system import System
import time


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


class ServerUpdateSystem(System):
    # todo: Rotation shouldn't be manditory. This is doing two jobs ticking the entity and
    # deciding the forces applied to it, because the input handler is also
    # doing both
    manditory = ["server_updated", "physics_update", "rotation"]
    handles = []

    def handle(self, node):

        packet = PhysicsPacket()
        packet.dt = 100
        packet.time = time.time() * 1000
        packet.rotation = node.rotation.rotation
        node.physics_update.packets.append(packet)
