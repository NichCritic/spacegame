from Systems.system import System


class GameStateRequestSystem(System):

    mandatory = ["player_controlled", "player_input", "sector", "tracked_ids"]
    optional = ["ping_neighbours"]
    handles = []

    def handle(self, pnode):
        game_state = {"player_id": pnode.id, "entities": {},
                      "time": pnode.player_input.data[-1]['time']}

        for n_id in pnode.sector.neighbours:
            if n_id not in pnode.tracked_ids.ids or pnode.has("ping_neighbours"):
                node = self.node_factory.create_node(n_id, [], [])
                node.add_or_attach_component("updated", {})

        nodes = self.node_factory.create_node_list(
            ["position", "updated"], ["type", "velocity", "mass", "inventory_mass", "area", "acceleration", "force", "rotation", "rotational_velocity", "physics_update", "player_input", "state_history", "mining", "minable", "collidable", "animated", "health", "weapon", "client_sync", "expires", "no_sync", "quest_status_updated", "pickup", "beam", "charged", "charging"], entity_ids=pnode.sector.neighbours)

        for node in nodes:
            if node.has('no_sync'):
                continue

            ntype = node.type.type if node.has('type') else None
            velx = node.velocity.x if node.has('velocity') else 0
            vely = node.velocity.y if node.has('velocity') else 0
            mass = (node.mass.mass if node.has('mass') else 1) + \
                (node.inventory_mass.inventory_mass if node.has(
                    "inventory_mass") else 0)
            radius = node.area.radius if node.has('area') else 1
            accelx = node.acceleration.x if node.has('acceleration') else 0
            accely = node.acceleration.y if node.has('acceleration') else 0
            forcex = node.force.x if node.has('force') else 0
            forcey = node.force.y if node.has('force') else 0
            rotation = node.rotation.rotation if node.has('rotation') else 0
            rotational_velocity = node.rotational_velocity.vel if node.has('rotational_velocity') else 0
            control = node.player_input.data[
                -1] if node.has('player_input') else None,
            last_update = node.physics_update.last_update if node.has(
                'physics_update') else 0
            # state_history = node.state_history.history if node.has(
            # 'state_history') else []
            mining = node.has("mining")
            minable = node.has("minable")
            collidable = node.has("collidable")
            animated = {"update_rate": node.animated.update_rate} if node.has(
                "animated") else None

            weapon = node.weapon.type if node.has("weapon") else None
            expires = {"expiry_time_ms": node.expires.expiry_time_ms,
                       "creation_time": node.expires.creation_time} if node.has("expires") else None

            pickup = True if node.has("pickup") else None

            beam = {"width": node.beam.width,
                    "length": node.beam.length} if node.has("beam") else None
            charging = True if node.has("charging") else False
            charged = {"charge_time":node.charged.charge_time} if node.has("charged") else None

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
                "weapon": {"type": weapon},
                "mass": mass,
                "radius": radius,
                "type": ntype,
                "rotation": rotation,
                "rotational_velocity": rotational_velocity,
                "control": control,
                "mining": mining,
                "minable": minable,
                "pickup": pickup,
                "collidable": collidable,
                "animated": animated,
                "beam": beam,
                "charging": charging,
                "charged": charged,
                "expires": expires,
                "last_update": last_update,
                # "state_history": state_history
            }
            if node.has('health'):
                game_state["entities"][node.id]["health"] = {
                    "health": node.health.health,
                    "max_health": node.health.max_health
                }
            if node.has('client_sync'):
                game_state["entities"][node.id]["client_sync"] = {
                    "sync_key": node.client_sync.sync_key
                }
            if node.has("quest_status_updated"):
                game_state["entities"][node.id]["quest_status_updated"] = {"quest": node.quest_status_updated.quest,
                                                                           "stage": node.quest_status_updated.stage}
            node.remove_component("updated")
        # print("Returning game state request")
        if node.has("ping_neighbours"):
            node.remove_component("ping_neighbours")
            pass
        pnode.message(game_state)
