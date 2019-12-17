
var InputSystem = (function() {
	var manditory = ["control"];
	var optional = [];
	var handles = ["control"];

	function InputSystem(node_factory) {
		this.node_factory = node_factory;
	}

	InputSystem.prototype.process = function() {
		var nodes = this.node_factory.create_node_list(manditory, optional);
		for(let i = 0; i < nodes.length; i++) {
			let node = nodes[i];
			this.handle(node);
			this.cleanup(node);
		}

	};

	InputSystem.prototype.cleanup = function(node) {
		for(let i = 0; i < handles.length; i++) {
			var comp = handles[i];
			node.delete_component(comp);
		}
	}

	InputSystem.prototype.handle = function(node) {
		node.add_or_attach("ship_control", {})
		node.ship_control.thrust = node.control.thrust
		node.ship_control.left = node.control.left
		node.ship_control.right = node.control.right
		node.ship_control.brake = node.control.brake
		node.ship_control.dt = node.control.dt

		if(node.control.shoot) {
			node.add_or_attach("shooting", {firing_rate:200});
			node.shooting.input = {shoot: node.control.shoot, dt: node.control.dt};
		}
		if(node.control.mining) {
			node.add_or_attach("mining", {}) 
		} else {
			node.delete_component("mining")
		}

	}

	return InputSystem; 
})();