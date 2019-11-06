
var ShootingSystem = (function() {
	var manditory = ['shooting', 'velocity', 'rotation', 'position'];
	var optional = [];
	var handles = ['shooting'];

	function ShootingSystem(node_factory, textures) {
		this.node_factory = node_factory;
		this.textures = textures;
	}

	ShootingSystem.prototype.process = function() {
		var nodes = this.node_factory.create_node_list(manditory, optional);
		for(let i = 0; i < nodes.length; i++) {
			let node = nodes[i];
			this.handle(node);
			this.cleanup(node);
		}

	};

	ShootingSystem.prototype.cleanup = function(node) {
		for(let i = 0; i < handles.length; i++) {
			var comp = handles[i];
			node.delete_component(comp);
		}
	}

	ShootingSystem.prototype.create_bullet = function(node, count) {
		var x_vel = Math.sin(node.rotation.rotation) * 0.5 + node.velocity.x;
        var y_vel = -Math.cos(node.rotation.rotation) * 0.5 + node.velocity.y;
        var x_pos = node.position.x + Math.sin(node.rotation.rotation) * 15;
        var y_pos = node.position.y + -Math.cos(node.rotation.rotation) * 15;
        var now = Date.now();
		var bullet = this.node_factory.create_node(
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
	            'renderable': {'spritesheet': this.textures['bolt'],
                               'image':this.textures['bolt'].idle[0],
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
            	}
		});
		// console.log("bullets fired: " + count)
		return bullet;
	}

	ShootingSystem.prototype.handle = function(node) {
		node.add_or_attach("shooting_vars");

		let input = node.shooting.input;
		let firing_rate = node.shooting.firing_rate;

		let now = Date.now();
		let dt_last_time = now - node.shooting_vars.last_update

		let running_time = node.shooting_vars.residual_cooldown == null ? firing_rate : Math.min(node.shooting_vars.residual_cooldown + dt_last_time, firing_rate);
		
		// console.log("Running time", running_time);

		let bullets_fired = node.shooting_vars.bullets_fired;

		let dt = input.dt;
		if(running_time + dt >= firing_rate) {
			this.create_bullet(node, bullets_fired)
			running_time -= firing_rate;
			bullets_fired++;
		}

		
		running_time += dt;

		node.shooting_vars.last_update = Date.now();
		node.shooting_vars.bullets_fired = bullets_fired;
		node.shooting_vars.residual_cooldown = running_time;

		
	}

	return ShootingSystem; 
})();