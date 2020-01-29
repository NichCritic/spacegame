from Systems.system import System


class PlayerCenteredSystem(System):
    '''
    A system that processes nodes which are in range of a player
    '''

    def __init__(self, node_factory):
        self.node_factory = node_factory

    def get_nodes(self):
        players = self.node_factory.create_node_list(
            ["player_controlled", "proximity"])
        ids = sum([set(node.proximity.proximity_map.keys())
                   for node in players])
        nodes = self.node_factory.create_node_list(self.mandatory,
                                                   self.optional, entity_ids=ids)
        return nodes
