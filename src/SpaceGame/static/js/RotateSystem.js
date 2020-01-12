
var RotateSystem = (function() {
	var manditory = ["rotation", "rotate"];
	var optional = [];
	var handles = [];

	function RotateSystem(node_factory) {
		this.node_factory = node_factory;
		this.position_cache = {};
	}

	RotateSystem.prototype.process = function(dt) {
		var nodes = this.node_factory.create_node_list(manditory, optional);
		
		
		for(let i = 0; i < nodes.length; i++) {
			let node = nodes[i];
			this.handle(node, dt);
			this.cleanup(node);
		}
	};

	RotateSystem.prototype.cleanup = function(node) {
		for(let i = 0; i < handles.length; i++) {
			var comp = handles[i];
			node.delete_component(comp);
		}
	}

	RotateSystem.prototype.handle = function(node, dt) {
		let amt = node.rotate.amt;
		node.rotation.rotation += amt * (dt / 1000)
	}

	return RotateSystem; 
})();

