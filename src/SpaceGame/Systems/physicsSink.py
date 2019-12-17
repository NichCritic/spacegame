from Systems.system import System


class PhysicsSink(System):
    """
    Handles the colliding state by ignoring it, in case other systems haven't handled it, 
    so that collisions don't build up cycle by cycle
    """

    mandatory = ["physics_update"]
    optional = []
    handles = []

    def __init__(self, node_factory):
        self.node_factory = node_factory

    def handle(self, node):
        node.physics_update.packets = []
