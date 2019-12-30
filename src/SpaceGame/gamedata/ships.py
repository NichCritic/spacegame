def default_ship(node):
    node.add_or_attach_component(
        'health', {"health": 1000, "max_health": 1000})

    node.add_or_attach_component('position', {})
    node.add_or_attach_component('area', {'radius': 8})
    node.add_or_attach_component('collidable', {})

    node.add_or_attach_component(
        'velocity', {})
    node.add_or_attach_component(
        'acceleration', {})
    node.add_or_attach_component(
        'force', {})
    node.add_or_attach_component(
        'rotation', {})

    node.add_or_attach_component("thrust", {"thrust": 0.015})

    node.add_or_attach_component('mass', {})
    node.add_or_attach_component('type', {'type': 'ship'})
    node.add_or_attach_component('physics_update', {})

    node.add_or_attach_component('game_state_request', {})
    node.add_or_attach_component('state_history', {})
    node.add_or_attach_component('animated', {'update_rate': 200})
    node.add_or_attach_component('collision_velocity_damage', {
                                 "damage": 200, "min_velocity": 0.2, "max_velocity": 1})
    node.add_or_attach_component('collision_movement', {})

    node.add_or_attach_component('weapon', {'type': 'beam'})

    node.add_or_attach_component('inventory', {'inventory': {}})
    node.add_or_attach_component('money', {'money': 0})
