from Systems.system import System


class HistorySystem(System):

    manditory = ["position", "renderable"]
    handles = []

    def __init__(self, node_factory):
        self.node_factory = node_factory

    def mandist(self, p1, p2):
        return p1.x + p2.x + p1.y + p2.y

    def handle(self, node):
        cameras = self.node_factory.create_node_list(['camera', 'position'])

        for camera in cameras:
            # Remove all new and leaving entities
            camera.camera.new_entities.clear()
            camera.camera.leaving_entities.clear()

            # Is the node inside or outside the camera radius?
            p1 = node.position
            p2 = camera.position
            d = self.mandist(p1, p2)
            if d < camera.camera.radius**2:
                # Was it there before?
                if node.id not in camera.camera.tracked_entities:
                    # If not Track it
                    camera.camera.new_entities.add(node.id)
                    camera.camera.tracked_entities.add(node.id)
            else:
                # Was it there before?
                if node.id in camera.camera.tracked_entities:
                    # remove it
                    camera.camera.tracked_entities.remove(node.id)
                    camera.camera.leaving_entities.add(node.id)
