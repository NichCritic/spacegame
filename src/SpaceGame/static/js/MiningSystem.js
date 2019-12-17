
var MiningSystem = (function() {
	var manditory = ['position', 'mining'];
	var optional = [];
	var handles = [];

	function MiningSystem(node_factory, textures) {
		this.node_factory = node_factory;
		this.textures = textures;
	}

	MiningSystem.prototype.process = function() {
		var nodes = this.node_factory.create_node_list(manditory, optional);
		for(let i = 0; i < nodes.length; i++) {
			let node = nodes[i];
			this.handle(node);
			this.cleanup(node);
		}

	};

	MiningSystem.prototype.cleanup = function(node) {
		return;
	}
	
	MiningSystem.prototype.get_closest_minable = function(node) {
		let nodes = this.node_factory.create_node_list(['minable', 'position', 'area']);
		let smallest = 251; //Max laser range + 1
		let current = nodes[0];

		for(let i = 0; i < nodes.length; i++) {
			let n = nodes[i];
			let dist = Math.sqrt((node.position.x - n.position.x)**2 + (node.position.y - n.position.y)**2);

			if(dist < smallest) {
				smallest = dist;
				current = n;
			}
		}

		return {
			dist:smallest,
			closest:current
		}

	}

	MiningSystem.prototype.handle = function(node) {

		let o = this.get_closest_minable(node);

		let dist = o.dist;
		let closest = o.closest;

		if(dist === 251) {
			//Nothing to mine in range
			return
		}

		let v_x = node.position.x - closest.position.x;
		let v_y = node.position.y - closest.position.y;

		let n_x = v_x / dist;
		let n_y = v_y / dist;

		let t_x = -n_y;
		let t_y = n_x;

		let vel_mag = (Math.random()*99 + 1) / 300;
        let t_vel_mag = (Math.random()*40 - 20) / 300;
        let vel_x = n_x * vel_mag + t_x * t_vel_mag;
        let vel_y = n_y * vel_mag + t_y * t_vel_mag;

        let start_x = closest.position.x + n_x * closest.area.radius
        let start_y = closest.position.y + n_y * closest.area.radius

        let now = Date.now();
		// logging.info("Creating spawn")
        this.node_factory.create_node({
            'force': {x:0, y:0},
            'acceleration': {x:0, y:0},
            'velocity': {'x': vel_x, 'y': vel_y},
            'position': {'x': start_x, 'y': start_y},
            'rotation': {'rotation': 0},
            'mass': {'mass':1},
            'type': {'type': 'asteroid'},
            'area': {'radius': 4},
            'server_controlled': {},
            'renderable': {'spritesheet': this.textures['asteroid'],
                               'image':this.textures['asteroid'].idle[0],
                               'width': 4,
                               'height': 4},
            'expires': {
                'expiry_time_ms': 100,
                'creation_time': now
            }
        })
	}

	return MiningSystem; 
})();