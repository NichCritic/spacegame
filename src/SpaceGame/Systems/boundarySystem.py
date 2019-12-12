from Systems.system import System


class BoundarySystem(System):
    """
    Handles the colliding state by ignoring it, in case other systems haven't handled it, 
    so that collisions don't build up cycle by cycle
    """

    mandatory = ["position"]
    optional = []
    handles = []

    def __init__(self, node_factory):
        self.node_factory = node_factory
        self.min_x = -15000
        self.max_x = 25000
        self.min_y = -20000
        self.max_y = 20000

    def handle(self, node):

        if node.position.x > self.max_x:
            diff = node.position.x - self.max_x
            node.position.x = self.min_x + diff

        if node.position.y > self.max_y:
            diff = node.position.y - self.max_y
            node.position.y = self.min_y + diff

        if node.position.x < self.min_x:
            diff = self.min_x - node.position.x 
            node.position.x = self.max_x - diff
            
        if node.position.y < self.min_y:
            diff = self.min_y - node.position.y
            node.position.y = self.max_y - diff
