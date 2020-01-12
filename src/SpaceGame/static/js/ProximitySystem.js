
var ProximitySystem = (function() {
	var manditory = ["position"];
	var optional = [];
	var handles = [];

	function ProximitySystem(node_factory) {
		this.node_factory = node_factory;
	}

	ProximitySystem.prototype.process = function() {
		var nodes = this.node_factory.create_node_list(manditory, optional);
		var p_nodes = this.node_factory.create_node_list(["position", "moved"]);
		for(let j = 0; j < p_nodes.length; j++) {
			let p_node = p_nodes[j];
			for(let i = 0; i < nodes.length; i++) {
				let node = nodes[i];
				if(node.id == p_node.id){
					continue;
				}
				this.handle(p_node, node);
				this.cleanup(node);
			}
		}

	};

	ProximitySystem.prototype.cleanup = function(node) {
		for(let i = 0; i < handles.length; i++) {
			var comp = handles[i];
			node.delete_component(comp);
		}
	}

	ProximitySystem.prototype.handle = function(p_node, node) {
		p_node.add_or_attach("proximity", {"proximity_map":{}});
		if(node.id in p_node.proximity.proximity_map) {
			return;
		}

		let x = p_node.position.x;
		let y = p_node.position.y;
		let x2 = node.position.x;
		let y2 = node.position.y;

		dist = Math.sqrt((x-x2)**2 + (y-y2)**2);

		
		p_node.proximity.proximity_map[node.id] = dist;
		node.add_or_attach("proximity", {"proximity_map":{}});
		node.proximity.proximity_map[p_node.id] = dist;
		


	}

	return ProximitySystem; 
})();

var ProximitySink = (function() {
	var manditory = ["proximity"]
	var optional = [];
	var handles = ["proximity"];

	function ProximitySink(node_factory) {
		this.node_factory = node_factory
	}

	ProximitySink.prototype.process = function() {
		var nodes = this.node_factory.create_node_list(manditory, optional);
		
		for(let i = 0; i < nodes.length; i++) {
			let node = nodes[i];
			this.cleanup(node);
		}
	};

	ProximitySink.prototype.cleanup = function(node) {
		for(let i = 0; i < handles.length; i++) {
			var comp = handles[i];
			node.delete_component(comp);
		}
	}

	return ProximitySink;
})();