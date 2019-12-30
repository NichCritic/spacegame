
var ShootingSystem = (function() {
	var manditory = ['shooting', 'velocity', 'rotation', 'position', 'weapon'];
	var optional = [];
	var handles = [];

	function ShootingSystem(node_factory, textures, weapons) {
		this.node_factory = node_factory;
		this.textures = textures;
		this.weapons = weapons
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
		node.add_or_attach("shooting_vars");
 		let weapon_fn = this.weapons[node.weapon.type];
		let input = node.shooting.input;
		let firing_rate = node.shooting.firing_rate;

		let now = Date.now();
		let dt_last_time = now - node.shooting_vars.last_update

		let running_time = node.shooting_vars.residual_cooldown == null ? firing_rate : Math.min(node.shooting_vars.residual_cooldown + dt_last_time, firing_rate);
		
		// console.log("Running time", running_time);

		let bullets_fired = node.shooting_vars.bullets_fired;

		let dt = input.dt;
		if(running_time + dt >= firing_rate) {
			weapon_fn(this.node_factory, node, bullets_fired, this.textures)
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

var ShootingSink = (function() {
	var manditory = ['shooting'];
	var optional = [];
	var handles = ['shooting'];

	function ShootingSink(node_factory) {
		this.node_factory = node_factory;
	}

	ShootingSink.prototype.process = function() {
		var nodes = this.node_factory.create_node_list(manditory, optional);
		for(let i = 0; i < nodes.length; i++) {
			let node = nodes[i];
			this.cleanup(node);
		}

	};

	ShootingSink.prototype.cleanup = function(node) {
		for(let i = 0; i < handles.length; i++) {
			var comp = handles[i];
			node.delete_component(comp);
		}
	}

	return ShootingSink; 
})();