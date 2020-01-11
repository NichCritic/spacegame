
var BossAnnounceSystem = (function() {
	var manditory = ["boss", "proximity"];
	var optional = [];
	var handles = [];

	function BossAnnounceSystem(node_factory) {
		this.node_factory = node_factory;
	}

	BossAnnounceSystem.prototype.process = function() {
		var nodes = this.node_factory.create_node_list(manditory, optional);
		
		
		for(let i = 0; i < nodes.length; i++) {
			let node = nodes[i];
			var p_nodes = this.node_factory.create_node_list(["player"], [], Object.keys(node.proximity.proximity_map));
			for(let j = 0; j < p_nodes.length; j++) {
				let p_node = p_nodes[j];
				if(node.id == p_node.id){
					continue;
				}
				this.handle(p_node, node);
				this.cleanup(node);
			}
		}
		

	};

	BossAnnounceSystem.prototype.cleanup = function(node) {
		for(let i = 0; i < handles.length; i++) {
			var comp = handles[i];
			node.delete_component(comp);
		}
	}

	BossAnnounceSystem.prototype.handle = function(p_node, node) {
		
		dist = node.proximity.proximity_map[p_node.id];

		if(dist < 1000) {
			//Code to set boss name, description
			//Going to access jquery globally here, kinda gross
			$(".encounter-inner").css("animation", "boss 2s")
		}

	}

	return BossAnnounceSystem; 
})();