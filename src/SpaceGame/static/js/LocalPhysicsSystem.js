


var LocalPhysicsSystem = (function() {
	var manditory = ["position", "velocity", "rotation", "mass", "acceleration", "force", "thrust", "ship_control"];
	var optional = [];
	var handles = ["ship_control"];

	function LocalPhysicsSystem(node_factory) {
		this.node_factory = node_factory;
	}

	function do_rotation(node, control, dt) {
		let rotation = node.rotation.rotation;
		node.rotation.rotation = control.left ? (rotation - 1/200 * dt) : (control.right ? (rotation + 1/200 * dt) : rotation);
	}

	function do_force(node, control, dt) {
		let rotation = node.rotation.rotation
		let thrust = node.thrust.thrust;

		node.force.x = control.thrust ? dt * thrust * Math.sin(rotation) + (-0.03*node.velocity.x*dt): 0;
		node.force.y = control.thrust ? -dt * thrust * Math.cos(rotation) + (-0.03*node.velocity.y*dt) : 0;
	}

	function do_acceleration(node, dt) {
		let mass = node.mass.mass;
		node.acceleration.x = node.force.x/mass;
	    node.acceleration.y = node.force.y/mass;
	}

	function do_velocity(node, dt) {
		node.velocity.x = node.velocity.x + node.acceleration.x * dt;
	    node.velocity.y = node.velocity.y + node.acceleration.y * dt;
	}

	function do_brake(node, control, dt) {
		if(!control.brake){
	    	node.velocity.x *= Math.pow(0.99, dt);
	    	node.velocity.y *= Math.pow(0.99, dt);
	    }
	}

	function do_position(node, dt) {
		node.position.x = node.position.x + node.velocity.x * dt;
	    node.position.y = node.position.y + node.velocity.y * dt;
	}

	LocalPhysicsSystem.prototype.process = function() {
		var nodes = this.node_factory.create_node_list(["ship_control", "rotation"]);
		let control = nodes[0].ship_control;
		let dt = nodes[0].ship_control.dt;


		for(let i = 0; i < nodes.length; i++) {
			let node = nodes[i];
			let control = node.ship_control;
			let dt = node.ship_control.dt;
			do_rotation(node, control, dt)
		}

		nodes = this.node_factory.create_node_list(["ship_control", "rotation", "thrust", "velocity"]);

		for(let i = 0; i < nodes.length; i++) {
			let node = nodes[i];
			node.add_or_attach("force", {})
			do_force(node, control, dt)
		}

		nodes = this.node_factory.create_node_list(["force", "mass"]);

		for(let i = 0; i < nodes.length; i++) {
			let node = nodes[i];
			node.add_or_attach("acceleration", {})
			do_acceleration(node, dt)
		}

		nodes = this.node_factory.create_node_list(["acceleration"]);

		for(let i = 0; i < nodes.length; i++) {
			let node = nodes[i];
			node.add_or_attach("velocity", {})
			do_velocity(node, dt)
		}

		nodes = this.node_factory.create_node_list(["velocity", "ship_control"]);
		for(let i = 0; i < nodes.length; i++) {
			let node = nodes[i];
			do_brake(node, control, dt)
		}

		nodes = this.node_factory.create_node_list(["position", "velocity"])

		for(let i = 0; i < nodes.length; i++) {
			let node = nodes[i];
			do_position(node, dt)
		}

	};


	return LocalPhysicsSystem; 
})();