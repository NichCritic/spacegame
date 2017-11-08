from Systems.system import System


class GameStateRequestSystem(System):

    manditory = ["game_state_request"]
    handles = ["game_state_request"]

    def handle(self, node):
        game_state = {"player_id": node.id, "entities": []}

        nodes = self.node_factory.create_node_list(
            ["position", "velocity", "mass", "acceleration", "force", "rotation", "physics_update"])

        for node in nodes:
            game_state["entities"].append({
                "id": node.id,
                "position": {"x": node.position.x,
                             "y": node.position.y
                             },
                "velocity": {"x": node.position.x,
                             "y": node.position.y
                             },
                "acceleration": {"x": node.position.x,
                                 "y": node.position.y
                                 },
                "force": {"x": node.position.x,
                          "y": node.position.y
                          },
                "mass": node.mass.mass,
                "rotation": node.rotation.rotation,
                "last_update": node.physics_update.last_update
            })
        print("Returning game state request")

        node.message(game_state)
