from Systems.system import System


class ShootingSink(System):

    mandatory = ["shooting"]
    optional = []
    handles = ["shooting"]

    def __init__(self, node_factory):
        self.node_factory = node_factory

    def handle(self, node):
        pass
