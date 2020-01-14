
var PositionLerpSystem = (function() {
	var manditory = ["target_position"];
	var optional = ["position"];
	var handles = [];

	function PositionLerpSystem(node_factory) {
		this.node_factory = node_factory;
	}

	PositionLerpSystem.prototype.process = function() {
		var nodes = this.node_factory.create_node_list(manditory, optional);
		for(let i = 0; i < nodes.length; i++) {
			let node = nodes[i];
			this.handle(node);
			this.cleanup(node);
		}

	};

	PositionLerpSystem.prototype.cleanup = function(node) {
		for(let i = 0; i < handles.length; i++) {
			var comp = handles[i];
			node.delete_component(comp);
		}
	}



	PositionLerpSystem.prototype.handle = function(node) {
		if(node.has("position")) {
			node.position.x = node.position.x * 0.5 + node.target_position.x * 0.5
			node.position.y = node.position.y * 0.5 + node.target_position.y * 0.5
		}
		else{
			node.add_or_attach("position", {"x":node.target_position.x, "y":node.target_position.y})
		}

		// if(node.type.type === "bolt") {
		// 	let dt = Date.now() - node.server_update.data.time;

		// 	node.position.x = node.position.x + node.velocity.x * dt;
		// 	node.position.y = node.position.y + node.velocity.y * dt;
		// }
	}

	return PositionLerpSystem; 
})();