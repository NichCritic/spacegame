from Systems.system import System


class GameStateRequestSystem(System):

    manditory = ["player_controlled", "player_input"]
    handles = []

    def handle(self, pnode):
        game_state = {"player_id": pnode.id, "entities": {},
                      "time": pnode.player_input.data[-1]['time']}

        print(pnode.player_input.data[-1])

        nodes = self.node_factory.create_node_list(
            ["player_input", "position", "velocity", "mass", "acceleration", "force", "rotation", "type", "physics_update"])

        for node in nodes:
            game_state["entities"][node.id] = {
                "id": node.id,
                "position": {"x": node.position.x,
                             "y": node.position.y
                             },
                "velocity": {"x": node.velocity.x,
                             "y": node.velocity.y
                             },
                "acceleration": {"x": node.acceleration.x,
                                 "y": node.acceleration.y
                                 },
                "force": {"x": node.force.x,
                          "y": node.force.y
                          },
                "mass": node.mass.mass,
                "type": node.type.type,
                "rotation": node.rotation.rotation,
                "control": node.player_input.data[-1],
                "last_update": node.physics_update.last_update
            }
        # print("Returning game state request")

        pnode.message(game_state)
