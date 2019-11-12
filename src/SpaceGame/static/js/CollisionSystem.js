
var CollisionSystem = (function() {
	var manditory = ["position", "area", "collidable"];
	var optional = [];
	var handles = [];

	function CollisionSystem(node_factory) {
		this.node_factory = node_factory;
	}

	CollisionSystem.prototype.process = function() {
		var nodes = this.node_factory.create_node_list(manditory, optional);
		var p_node = this.node_factory.create_node_list(["player", "position", "area"])[0];
		for(let i = 0; i < nodes.length; i++) {
			let node = nodes[i];
			if(node.id == p_node.id){
				continue;
			}
			this.handle(p_node, node);
			this.cleanup(node);
		}

	};

	CollisionSystem.prototype.cleanup = function(node) {
		for(let i = 0; i < handles.length; i++) {
			var comp = handles[i];
			node.delete_component(comp);
		}
	}

	CollisionSystem.prototype.handle = function(p_node, node) {
		let x = p_node.position.x;
		let y = p_node.position.y;
		let x2 = node.position.x;
		let y2 = node.position.y;

		dist = Math.sqrt((x-x2)**2 + (y-y2)**2);

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
		}


	}

	return CollisionSystem; 
})();