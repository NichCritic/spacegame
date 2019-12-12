from Systems.system import System


class BoughtSink(System):
    """
    Handles the bought or sold state by ignoring it, in case other systems haven't handled it
    """

    mandatory = ["bought"]
    optional = []
    handles = ["bought"]

    def __init__(self, node_factory):
        self.node_factory = node_factory

    def handle(self, node):
        pass

class SoldSink(System):
    """
    Handles the bought or sold state by ignoring it, in case other systems haven't handled it
    """

    mandatory = ["sold"]
    optional = []
    handles = ["sold"]

    def __init__(self, node_factory):
        self.node_factory = node_factory

    def handle(self, node):
        pass
