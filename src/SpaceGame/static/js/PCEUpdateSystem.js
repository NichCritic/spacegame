
var PCEUpdateSystem = (function() {
	var manditory = ["server_update", "player_created"];
	var optional = [];
	var handles = ["server_update"];


	function PCEUpdateSystem(node_factory) {
		this.node_factory = node_factory;
	}

	PCEUpdateSystem.prototype.process = function() {
		var nodes = this.node_factory.create_node_list(manditory, optional);
		for(let i = 0; i < nodes.length; i++) {
			let node = nodes[i];
			this.handle(node);
			this.cleanup(node);
		}

	};

	PCEUpdateSystem.prototype.cleanup = function(node) {
		for(let i = 0; i < handles.length; i++) {
			var comp = handles[i];
			node.delete_component(comp);
		}
	}



	PCEUpdateSystem.prototype.handle = function(node) {
		let pnode = this.node_factory.create_node_list(["player", "inputs"], [])[0];
		let inputs = pnode.inputs.inputs;
		
		node.add_or_update("position", node.server_update.data.position);
		node.add_or_update("velocity", node.server_update.data.velocity);
		node.add_or_update("acceleration", node.server_update.data.acceleration);
		node.add_or_update("force", node.server_update.data.force);
		node.add_or_update("thrust", node.server_update.data.thrust);
		node.add_or_update("rotation", node.server_update.data.rotation);
		node.add_or_update("mass", node.server_update.data.mass);

		for(let i = 0; i < inputs.list.length-1; i++) {
			let control = {};
			control.dt = inputs.list[i].dt
			control.brake = true;
			do_physics(node, control, control.dt);
		}
		
	}

	return PCEUpdateSystem; 
})();