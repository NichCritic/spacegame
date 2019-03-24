
var ShootingSystem = (function() {
	var manditory = ["shooting", "velocity", "rotation", "position"];
	var optional = [];
	var handles = [];

	function ShootingSystem(node_factory, inputs) {
		this.node_factory = node_factory;
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
		var x_vel = math.sin(node.rotation.rotation) + node.velocity.x * 50
        var y_vel = -math.cos(node.rotation.rotation) + node.velocity.y * 50
		var bullet = node_factory.create_node(
			{
            'force': {},
            'acceleration': {},
            'velocity': {'x': x_vel, 'y': y_vel},
            'position': {'x': x_pos, 'y': y_pos},
            'rotation': {'rotation': node.rotation.rotation},
            'area': {'radius': 6},
            'mass': {},
            // 'server_updated': {},
            'type': {'type': 'bolt'},
            // 'physics_update': {'last_update': now},
            // 'state_history': {},
            // 'expires': {
            //     'expiry_time_ms': 2000,
            //     'creation_time': now
            // },
		})
	}

	return ShootingSystem; 
})();