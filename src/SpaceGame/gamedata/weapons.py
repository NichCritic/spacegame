import math
import time

def single_shot(node_factory, node, creation_time, count):
        x_vel = math.sin(node.rotation.rotation) * 0.5 + node.velocity.x
        y_vel = -math.cos(node.rotation.rotation) * 0.5 + node.velocity.y

        now = time.time() * 1000
        start_time = node.physics_update.last_update + creation_time

        dt = now - start_time

        if dt < 0:
            dt = 0

        x_pos = node.position.x + \
            math.sin(node.rotation.rotation) * 15 + x_vel * dt
        y_pos = node.position.y - \
            math.cos(node.rotation.rotation) * 15 + y_vel * dt

        # logging.info("Bullets fired: "+str(count))
        bullet = node_factory.create_new_node({
            'force': {},
            'acceleration': {},
            'velocity': {'x': x_vel, 'y': y_vel},
            'position': {'x': x_pos, 'y': y_pos},
            'rotation': {'rotation': node.rotation.rotation},
            'area': {'radius': 6},
            'mass': {},
            'server_updated': {},
            'type': {'type': 'bolt'},
            'physics_update': {'last_update': now},
            'state_history': {},
            'expires': {
                'expiry_time_ms': 2000,
                'creation_time': start_time
            },
            "collidable": {},
            "collision_damage": {"damage": 100},
            # "client_sync": {"sync_key": count}
            # "no_sync": {}
        })

        if node.has("player_controlled"):
            bullet.add_or_attach_component('no_sync', {})

def triple_shot(node_factory, node, creation_time, count):
        twentydegreesrad = 0.349066


        x_vel1 = math.sin(node.rotation.rotation) * 0.5 + node.velocity.x
        y_vel1 = -math.cos(node.rotation.rotation) * 0.5 + node.velocity.y
        x_vel2 = math.sin(node.rotation.rotation+twentydegreesrad) * 0.5 + node.velocity.x
        y_vel2 = -math.cos(node.rotation.rotation+twentydegreesrad) * 0.5 + node.velocity.y
        x_vel3 = math.sin(node.rotation.rotation-twentydegreesrad) * 0.5 + node.velocity.x
        y_vel3 = -math.cos(node.rotation.rotation-twentydegreesrad) * 0.5 + node.velocity.y

        now = time.time() * 1000
        start_time = node.physics_update.last_update + creation_time

        dt = now - start_time

        if dt < 0:
            dt = 0

        x_pos = node.position.x + \
            math.sin(node.rotation.rotation) * 15 + x_vel1 * dt
        y_pos = node.position.y - \
            math.cos(node.rotation.rotation) * 15 + y_vel1 * dt

        # logging.info("Bullets fired: "+str(count))
        center_bullet = node_factory.create_new_node({
            'force': {},
            'acceleration': {},
            'velocity': {'x': x_vel1, 'y': y_vel1},
            'position': {'x': x_pos, 'y': y_pos},
            'rotation': {'rotation': node.rotation.rotation},
            'area': {'radius': 6},
            'mass': {},
            'server_updated': {},
            'type': {'type': 'bolt'},
            'physics_update': {'last_update': now},
            'state_history': {},
            'expires': {
                'expiry_time_ms': 2000,
                'creation_time': start_time
            },
            "collidable": {},
            "collision_damage": {"damage": 100},
            # "client_sync": {"sync_key": count}
            # "no_sync": {}
        })

        top_bullet = node_factory.create_new_node({
            'force': {},
            'acceleration': {},
            'velocity': {'x': x_vel2, 'y': y_vel2},
            'position': {'x': x_pos, 'y': y_pos},
            'rotation': {'rotation': node.rotation.rotation+twentydegreesrad},
            'area': {'radius': 6},
            'mass': {},
            'server_updated': {},
            'type': {'type': 'bolt'},
            'physics_update': {'last_update': now},
            'state_history': {},
            'expires': {
                'expiry_time_ms': 2000,
                'creation_time': start_time
            },
            "collidable": {},
            "collision_damage": {"damage": 100},
            # "client_sync": {"sync_key": count}
            # "no_sync": {}
        })

        bottom_bullet = node_factory.create_new_node({
            'force': {},
            'acceleration': {},
            'velocity': {'x': x_vel3, 'y': y_vel3},
            'position': {'x': x_pos, 'y': y_pos},
            'rotation': {'rotation': node.rotation.rotation-twentydegreesrad},
            'area': {'radius': 6},
            'mass': {},
            'server_updated': {},
            'type': {'type': 'bolt'},
            'physics_update': {'last_update': now},
            'state_history': {},
            'expires': {
                'expiry_time_ms': 2000,
                'creation_time': start_time
            },
            "collidable": {},
            "collision_damage": {"damage": 100},
            # "client_sync": {"sync_key": count}
            # "no_sync": {}
        })



        if node.has("player_controlled"):
            center_bullet.add_or_attach_component('no_sync', {})
            top_bullet.add_or_attach_component('no_sync', {})
            bottom_bullet.add_or_attach_component('no_sync', {})


weapons = {
    'single_shot':single_shot,
    'triple_shot':triple_shot
}