from Systems.system import System


class QuestUpdateSink(System):
    """
    Handles the bought or sold state by ignoring it, in case other systems haven't handled it
    """

    mandatory = ["quest_status_updated"]
    optional = []
    handles = ["quest_status_updated"]

    def __init__(self, node_factory):
        self.node_factory = node_factory

    def handle(self, node):
        pass


