from Systems.system import System


class ProximitySink(System):

    mandatory = ["proximity"]
    optional = []
    handles = ["proximity"]

    def __init__(self, node_factory):
        self.node_factory = node_factory

    def handle(self, node):
        pass
