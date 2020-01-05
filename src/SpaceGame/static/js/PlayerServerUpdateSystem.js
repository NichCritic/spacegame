
var PlayerServerUpdateSystem = (function() {
	var manditory = ["server_update", "player", "inputs"];
	var optional = [];
	var handles = ["server_update"];

	function PlayerServerUpdateSystem(node_factory) {
		this.node_factory = node_factory;
	}

	PlayerServerUpdateSystem.prototype.process = function() {
		var nodes = this.node_factory.create_node_list(manditory, optional);
		for(let i = 0; i < nodes.length; i++) {
			let node = nodes[i];
			this.handle(node);
			this.cleanup(node);
		}

	};

	PlayerServerUpdateSystem.prototype.cleanup = function(node) {
		for(let i = 0; i < handles.length; i++) {
			var comp = handles[i];
			node.delete_component(comp);
		}
	}



	PlayerServerUpdateSystem.prototype.handle = function(node) {
		let control = node.control;
		let inputs = node.inputs.inputs;
		
		node.add_or_update("position", node.server_update.data.position);
		node.add_or_update("velocity", node.server_update.data.velocity);
		node.add_or_update("acceleration", node.server_update.data.acceleration);
		node.add_or_update("force", node.server_update.data.force);
		node.add_or_update("thrust", node.server_update.data.thrust);
		node.add_or_update("rotation", node.server_update.data.rotation);
		node.add_or_update("rotational_velocity", node.server_update.data.rotational_velocity)
		node.add_or_update("mass", node.server_update.data.mass);

		for(let i = 0; i < inputs.list.length-1; i++) {
			let control = inputs.list[i];
			do_physics(node, control, control.dt);
		}
		
	}

	return PlayerServerUpdateSystem; 
})();