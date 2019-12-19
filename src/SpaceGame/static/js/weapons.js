var weapons = (function(){

	function single_shot(node_factory, node, count, textures) {
		var x_vel = Math.sin(node.rotation.rotation) * 0.5 + node.velocity.x;
        var y_vel = -Math.cos(node.rotation.rotation) * 0.5 + node.velocity.y;
        var x_pos = node.position.x + Math.sin(node.rotation.rotation) * 15;
        var y_pos = node.position.y + -Math.cos(node.rotation.rotation) * 15;
        var now = Date.now();
		var bullet = node_factory.create_node(
			{
	            'force': {'x': 0, 'y': 0},
	            'acceleration': {'x':0, 'y': 0},
	            'velocity': {'x': x_vel, 'y': y_vel},
	            'position': {'x': x_pos, 'y': y_pos},
	            'rotation': {'rotation': node.rotation.rotation},
	            'area': {'radius': 6},
	            'mass': {'mass':2},
	            'server_controlled': {},
	            'type': {'type': 'bolt'},
	            'renderable': {'spritesheet': textures['bolt'],
                               'image':textures['bolt'].idle[0],
                               'width': 12,
                               'height': 12},
	            // 'physics_update': {'last_update': now},
	            // 'state_history': {},
	            'expires': {
		            'expiry_time_ms': 2000,
		            'creation_time': now
            	},
            	'server_sync': {
            		'sync_key': count
            	},
            	'check_collision': {},
            	'remove_on_collide': {}
            	// //Hacky way to make them go away when they hit something
            	// 'collidable': {},
            	// 'pickup': {}
		});
		// console.log("bullets fired: " + count)
		return bullet;
	}

	function triple_shot(node_factory, node, count, textures) {
		var twentydegreesrad = 0.349066
		var x_vel1 = Math.sin(node.rotation.rotation) * 0.5 + node.velocity.x;
        var y_vel1 = -Math.cos(node.rotation.rotation) * 0.5 + node.velocity.y;
		var x_vel2 = Math.sin(node.rotation.rotation+twentydegreesrad) * 0.5 + node.velocity.x;
        var y_vel2 = -Math.cos(node.rotation.rotation+twentydegreesrad) * 0.5 + node.velocity.y;
		var x_vel3 = Math.sin(node.rotation.rotation-twentydegreesrad) * 0.5 + node.velocity.x;
        var y_vel3 = -Math.cos(node.rotation.rotation-twentydegreesrad) * 0.5 + node.velocity.y;
        var x_pos = node.position.x + Math.sin(node.rotation.rotation) * 15;
        var y_pos = node.position.y + -Math.cos(node.rotation.rotation) * 15;
        var now = Date.now();
		var bullet = node_factory.create_node(
			{
	            'force': {'x': 0, 'y': 0},
	            'acceleration': {'x':0, 'y': 0},
	            'velocity': {'x': x_vel1, 'y': y_vel1},
	            'position': {'x': x_pos, 'y': y_pos},
	            'rotation': {'rotation': node.rotation.rotation},
	            'area': {'radius': 6},
	            'mass': {'mass':2},
	            'server_controlled': {},
	            'type': {'type': 'bolt'},
	            'renderable': {'spritesheet': textures['bolt'],
                               'image':textures['bolt'].idle[0],
                               'width': 12,
                               'height': 12},
	            // 'physics_update': {'last_update': now},
	            // 'state_history': {},
	            'expires': {
		            'expiry_time_ms': 2000,
		            'creation_time': now
            	},
            	'server_sync': {
            		'sync_key': count
            	},
            	'check_collision': {},
            	'remove_on_collide': {}
		});

		var bullet2 = node_factory.create_node(
			{
	            'force': {'x': 0, 'y': 0},
	            'acceleration': {'x':0, 'y': 0},
	            'velocity': {'x': x_vel2, 'y': y_vel2},
	            'position': {'x': x_pos, 'y': y_pos},
	            'rotation': {'rotation': node.rotation.rotation+twentydegreesrad},
	            'area': {'radius': 6},
	            'mass': {'mass':2},
	            'server_controlled': {},
	            'type': {'type': 'bolt'},
	            'renderable': {'spritesheet': textures['bolt'],
                               'image':textures['bolt'].idle[0],
                               'width': 12,
                               'height': 12},
	            // 'physics_update': {'last_update': now},
	            // 'state_history': {},
	            'expires': {
		            'expiry_time_ms': 2000,
		            'creation_time': now
            	},
            	'server_sync': {
            		'sync_key': count
            	},
            	'check_collision': {},
            	'remove_on_collide': {}
		});

		var bullet3 = node_factory.create_node(
			{
	            'force': {'x': 0, 'y': 0},
	            'acceleration': {'x':0, 'y': 0},
	            'velocity': {'x': x_vel3, 'y': y_vel3},
	            'position': {'x': x_pos, 'y': y_pos},
	            'rotation': {'rotation': node.rotation.rotation-twentydegreesrad},
	            'area': {'radius': 6},
	            'mass': {'mass':2},
	            'server_controlled': {},
	            'type': {'type': 'bolt'},
	            'renderable': {'spritesheet': textures['bolt'],
                               'image':textures['bolt'].idle[0],
                               'width': 12,
                               'height': 12},
	            // 'physics_update': {'last_update': now},
	            // 'state_history': {},
	            'expires': {
		            'expiry_time_ms': 2000,
		            'creation_time': now
            	},
            	'server_sync': {
            		'sync_key': count
            	},
            	'check_collision': {},
            	'remove_on_collide': {}
		});
		// console.log("bullets fired: " + count)
	}

	return {
		single_shot:single_shot,
		triple_shot:triple_shot
	}


})();

