
var MovementSystem = (function() {
	var manditory = ["position"];
	var optional = ["to_be_removed"];
	var handles = [];

	function MovementSystem(node_factory) {
		this.node_factory = node_factory;
		this.position_cache = {};
	}

	MovementSystem.prototype.process = function() {
		var nodes = this.node_factory.create_node_list(manditory, optional);
		
		
		for(let i = 0; i < nodes.length; i++) {
			let node = nodes[i];
			this.handle(node);
			this.cleanup(node);
		}
	};

	MovementSystem.prototype.cleanup = function(node) {
		for(let i = 0; i < handles.length; i++) {
			var comp = handles[i];
			node.delete_component(comp);
		}
	}

	MovementSystem.prototype.handle = function(node) {
		if(node.has("to_be_removed")) {
			delete this.position_cache[node.id];
			return
		}

		if(node.id in this.position_cache) {
			let x = Math.floor(node.position.x);
			let y = Math.floor(node.position.y);
			if(x != this.position_cache[node.id].x || y != this.position_cache[node.id].y) {
				node.add_or_attach("moved", {})
				this.position_cache[node.id] = {
					x: Math.floor(node.position.x),
					y: Math.floor(node.position.y)
				}
			} else {
				node.delete_component("moved");
			}
		} else {
			node.add_or_attach("moved", {});
			this.position_cache[node.id] = {
				x: Math.floor(node.position.x),
				y: Math.floor(node.position.y)
			}
		}
		

	}

	return MovementSystem; 
})();

