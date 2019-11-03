
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

	ShootingSystem.prototype.handle = function(node) {
		var x_vel = Math.sin(node.rotation.rotation) * 0.1 + node.velocity.x;
        var y_vel = -Math.cos(node.rotation.rotation) * 0.1 + node.velocity.y;
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
		            'expiry_time_ms': 500,
		            'creation_time': now
            	},
		})
	}

	return ShootingSystem; 
})();