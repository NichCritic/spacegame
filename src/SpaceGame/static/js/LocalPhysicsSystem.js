
var LocalPhysicsSystem = (function() {
	var manditory = ["position", "velocity", "acceleration", "force", "thrust", "control"]
	var optional = []
	var handles = ["control"]

	function LocalPhysicsSystem(node_factory) {
		this.node_factory = node_factory;
	}

	LocalPhysicsSystem.prototype.process = function() {
		let nodes = this.node_factory.create_node_list(manditory, optional);
		for(let i = 0; i < nodes.length; i++) {
			let node = nodes[i];
			this.handle(node);
			this.cleanup(node);
		}

	};

	LocalPhysicsSystem.prototype.cleanup = function(node) {
		for(let i = 0; i < handles.length; i++) {
			var comp = handles[i];
			node.delete_component(comp);
		}
	}

	LocalPhysicsSystem.prototype.handle = function(node) {
		let control = node.control;
		let dt = control.dt;

		let mass = node.mass.mass;
		let rotation = node.rotation.rotation;

		let rot_left = (rotation - 1/200 * dt);
		let rot_right = (rotation + 1/200 * dt);

		node.rotation.rotation = control.left ? rot_left : (control.right ? rot_right : rotation);
		
		let thrust_x = node.thrust.x;
		let thrust_y=  node.thrust.y;

		node.force.x = control.thrust ? dt * thrust_x * Math.sin(new_entity.rotation) + (-0.03*entity.velocity.x*dt): 0;
		node.force.y = control.thrust ? -dt * thrust.y * Math.cos(new_entity.rotation) + (-0.03*entity.velocity.y*dt) : 0;

		node.acceleration.x = node.force.x/mass;
	    node.acceleration.y = node.force.y/mass;

	    node.velocity.x = node.velocity.x + node.acceleration.x * dt;
	    node.velocity.y = node.velocity.y + node.acceleration.y * dt;

	    if(!control.brake){
	    	node.velocity.x *= Math.pow(0.99, dt);
	    	node.velocity.y *= Math.pow(0.99, dt);
	    }

	    node.position.x = node.position.x + node.velocity.x * dt;
	    node.position.y = node.position.y + node.velocity.y * dt;
	}

	return LocalPhysicsSystem; 
});