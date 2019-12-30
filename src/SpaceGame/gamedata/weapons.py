import math
import time


def beam(node_factory, node, creation_time, count):
    now = time.time() * 1000
    start_time = node.physics_update.last_update + creation_time

    dt = now - start_time

    if dt < 0:
        dt = 0

    x_pos = node.position.x
    y_pos = node.position.y

    ignored_nodes = [node.id]
    if node.entity_has("attached"):
        node.add_or_attach_component("attached", {"target_id": node.id})
        ignored_nodes.append(node.attached.target_id)

    # logging.info("Bullets fired: "+str(count))
    bullet = node_factory.create_new_node({
        'position': {'x': x_pos, 'y': y_pos},
        'rotation': {'rotation': node.rotation.rotation},
        'beam': {'length': 1000, 'width': 3},
        # "collidable": {},
        # "collision_damage": {"damage": 25},
        "ignore_collisions": {"ids": ignored_nodes},
        "attached": {"target_id": node.id},
        "charging": {}  # How long? Then what?
    })

    if node.entity_has("allies"):
        node.add_or_attach_component("allies", {})
        bullet.add_or_attach_component("allies", {"team": node.allies.team})


def homing_missile(node_factory, node, creation_time, count):
    x_vel = node.velocity.x
    y_vel = node.velocity.y

    now = time.time() * 1000
    start_time = node.physics_update.last_update + creation_time

    dt = now - start_time

    if dt < 0:
        dt = 0

    x_pos = node.position.x + \
        math.sin(node.rotation.rotation) * 15 + x_vel * dt
    y_pos = node.position.y - \
        math.cos(node.rotation.rotation) * 15 + y_vel * dt

    ignored_nodes = [node.id]
    if node.entity_has("attached"):
        node.add_or_attach_component("attached", {"target_id": node.id})
        ignored_nodes.append(node.attached.target_id)

    # logging.info("Bullets fired: "+str(count))
    bullet = node_factory.create_new_node({
        'force': {},
        'acceleration': {},
        'velocity': {'x': x_vel, 'y': y_vel},
        'position': {'x': x_pos, 'y': y_pos},
        'rotation': {'rotation': node.rotation.rotation},
        'area': {'radius': 6},
        'mass': {'mass': 40},
        'thrust': {'thrust': 0.005},
        'server_updated': {},
        'type': {'type': 'missile'},
        'physics_update': {'last_update': now},
        'state_history': {},
        'expires': {
            'expiry_time_ms': 10000,
            'creation_time': start_time
        },
        "collidable": {},
        "collision_damage": {"damage": 250},
        "ignore_collisions": {"ids": ignored_nodes},
        'orient_towards_target': {},
        'proximity_target_behaviour': {"exclusion_list": ignored_nodes},

        'no_target_allies': {}
        # "client_sync": {"sync_key": count}
        # "no_sync": {}
    })

    if node.entity_has("allies"):
        node.add_or_attach_component("allies", {})
        bullet.add_or_attach_component("allies", {"team": node.allies.team})


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

    ignored_nodes = [node.id]
    if node.entity_has("attached"):
        node.add_or_attach_component("attached", {"target_id": node.id})
        ignored_nodes.append(node.attached.target_id)

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
        "ignore_collisions": {"ids": ignored_nodes}
        # "client_sync": {"sync_key": count}
        # "no_sync": {}
    })

    if node.has("player_controlled"):
        bullet.add_or_attach_component('no_sync', {})


def triple_shot(node_factory, node, creation_time, count):
    twentydegreesrad = 0.349066

    x_vel1 = math.sin(node.rotation.rotation) * 0.5 + node.velocity.x
    y_vel1 = -math.cos(node.rotation.rotation) * 0.5 + node.velocity.y
    x_vel2 = math.sin(node.rotation.rotation +
                      twentydegreesrad) * 0.5 + node.velocity.x
    y_vel2 = -math.cos(node.rotation.rotation +
                       twentydegreesrad) * 0.5 + node.velocity.y
    x_vel3 = math.sin(node.rotation.rotation -
                      twentydegreesrad) * 0.5 + node.velocity.x
    y_vel3 = -math.cos(node.rotation.rotation -
                       twentydegreesrad) * 0.5 + node.velocity.y

    now = time.time() * 1000
    start_time = node.physics_update.last_update + creation_time

    dt = now - start_time

    if dt < 0:
        dt = 0

    x_pos = node.position.x + \
        math.sin(node.rotation.rotation) * 15 + x_vel1 * dt
    y_pos = node.position.y - \
        math.cos(node.rotation.rotation) * 15 + y_vel1 * dt

    ignored_nodes = [node.id]
    if node.entity_has("attached"):
        node.add_or_attach_component("attached", {"target_id": node.id})
        ignored_nodes.append(node.attached.target_id)

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
        "ignore_collisions": {"ids": ignored_nodes}
        # "client_sync": {"sync_key": count}
        # "no_sync": {}
    })

    top_bullet = node_factory.create_new_node({
        'force': {},
        'acceleration': {},
        'velocity': {'x': x_vel2, 'y': y_vel2},
        'position': {'x': x_pos, 'y': y_pos},
        'rotation': {'rotation': node.rotation.rotation + twentydegreesrad},
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
        "ignore_collisions": {"ids": ignored_nodes}
        # "client_sync": {"sync_key": count}
        # "no_sync": {}
    })

    bottom_bullet = node_factory.create_new_node({
        'force': {},
        'acceleration': {},
        'velocity': {'x': x_vel3, 'y': y_vel3},
        'position': {'x': x_pos, 'y': y_pos},
        'rotation': {'rotation': node.rotation.rotation - twentydegreesrad},
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
        "ignore_collisions": {"ids": ignored_nodes}
        # "client_sync": {"sync_key": count}
        # "no_sync": {}
    })

    if node.has("player_controlled"):
        center_bullet.add_or_attach_component('no_sync', {})
        top_bullet.add_or_attach_component('no_sync', {})
        bottom_bullet.add_or_attach_component('no_sync', {})


weapons = {
    'single_shot': single_shot,
    'triple_shot': triple_shot,
    'homing_missile': homing_missile,
    'beam': beam
}
