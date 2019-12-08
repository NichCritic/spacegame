from Systems.system import System


class BoughtSoldSink(System):
    """
    Handles the bought or sold state by ignoring it, in case other systems haven't handled it
    """

    manditory = []
    optional = ["bought"]
    handles = ["bought", "sold"]

    def __init__(self, node_factory):
        self.node_factory = node_factory

    def handle(self, node):
        pass
