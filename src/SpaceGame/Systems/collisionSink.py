from Systems.system import System


class CollisionSink(System):
    """
    Handles the colliding state by ignoring it, in case other systems haven't handled it, 
    so that collisions don't build up cycle by cycle
    """

    manditory = ["colliding"]
    optional = []
    handles = ["colliding"]

    def __init__(self, node_factory):
        self.node_factory = node_factory

    def handle(self, node):
        pass
