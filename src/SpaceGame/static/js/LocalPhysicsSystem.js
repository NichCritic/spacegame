
var LocalPhysicsSystem = (function() {
	var manditory = ["position", "velocity", "rotation", "mass", "acceleration", "force", "thrust", "control"];
	var optional = [];
	var handles = ["control"];

	function LocalPhysicsSystem(node_factory) {
		this.node_factory = node_factory;
	}

	LocalPhysicsSystem.prototype.process = function() {
		var nodes = this.node_factory.create_node_list(manditory, optional);
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

		do_physics(node, control, dt);
	}

	return LocalPhysicsSystem; 
})();