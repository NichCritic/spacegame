
var CollisionSystem = (function() {
	var manditory = ["area", "collidable"];
	var optional = [];
	var handles = [];

	function CollisionSystem(node_factory) {
		this.node_factory = node_factory;
	}

	CollisionSystem.prototype.process = function() {
		var nodes = this.node_factory.create_node_list(manditory, optional);
		var p_nodes = this.node_factory.create_node_list(["check_collision", "area", "proximity"]);
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

	CollisionSystem.prototype.cleanup = function(node) {
		for(let i = 0; i < handles.length; i++) {
			var comp = handles[i];
			node.delete_component(comp);
		}
	}

	CollisionSystem.prototype.handle = function(p_node, node) {
		
		dist = p_node.proximity.proximity_map[node.id];

		if(dist == 0) {
			dist = 1;
		}

		rad = p_node.area.radius;
		rad2 = node.area.radius;

		if(rad + rad2 > dist) {
			p_node.add_or_attach("colliding", {})
			p_node.colliding.collisions.push({
				collider:node,
				dist: dist,
				delta: rad + rad2 - dist
			})

			//Hack, this should be in its own system
			if(p_node.entity_has("remove_on_collide")) {
				p_node.add_or_attach("to_be_removed")
			}
			if(node.entity_has("remove_on_collide")) {
				node.add_or_attach("to_be_removed")
			}
		}


	}

	return CollisionSystem; 
})();