from Systems.system import System


class InputSystem(System):

    manditory = ["player_input"]
    handles = ["player_input"]

    def handle(self, node):

        node.message(node.player_input.data)
