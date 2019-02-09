from Systems.system import System


class GameStateRequestSystem(System):

    manditory = ["player_controlled", "player_input"]
    handles = []

    def handle(self, pnode):
        game_state = {"player_id": pnode.id, "entities": {},
                      "time": pnode.player_input.data[-1]['time']}

        # print(pnode.player_input.data[-1])
        # print("BOOOOOOOOOYYYYYYYYY")

        nodes = self.node_factory.create_node_list(
            ["position", "type"], ["velocity", "mass", "area", "acceleration", "force", "rotation", "physics_update", "player_input", "state_history"])

        for node in nodes:

            velx = node.velocity.x if node.has('velocity') else 0
            vely = node.velocity.y if node.has('velocity') else 0
            mass = node.mass.mass if node.has('mass') else 1
            radius = node.area.radius if node.has('area') else 1
            accelx = node.acceleration.x if node.has('acceleration') else 0
            accely = node.acceleration.y if node.has('acceleration') else 0
            forcex = node.force.x if node.has('force') else 0
            forcey = node.force.y if node.has('force') else 0
            rotation = node.rotation.rotation if node.has('rotation') else 0
            control = node.player_input.data[
                -1] if node.has('player_input') else None,
            last_update = node.physics_update.last_update if node.has(
                'physics_update') else 0
            state_history = node.state_history.history if node.has(
                'state_history') else []

            game_state["entities"][node.id] = {
                "id": node.id,
                "position": {"x": node.position.x,
                             "y": node.position.y
                             },
                "velocity": {"x": velx,
                             "y": vely
                             },
                "acceleration": {"x": accelx,
                                 "y": accely
                                 },
                "force": {"x": forcex,
                          "y": forcey
                          },
                "mass": mass,
                "radius": radius,
                "type": node.type.type,
                "rotation": rotation,
                "control": control,
                "last_update": last_update,
                "state_history": state_history
            }
        # print("Returning game state request")

        pnode.message(game_state)
