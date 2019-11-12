
var CollisionMovementSystem = (function() {
	var manditory = ["colliding", "position", "force", "rotation", "mass", "velocity"];
	var optional = ["inventory_mass"];
	var handles = ["colliding"];

	function CollisionMovementSystem(node_factory) {
		this.node_factory = node_factory;
	}

	CollisionMovementSystem.prototype.process = function() {
		var nodes = this.node_factory.create_node_list(manditory, optional);
		for(let i = 0; i < nodes.length; i++) {
			let node = nodes[i];
			this.handle(node);
			this.cleanup(node);
		}

	};

	CollisionMovementSystem.prototype.cleanup = function(node) {
		for(let i = 0; i < handles.length; i++) {
			var comp = handles[i];
			node.delete_component(comp);
		}
	}

	CollisionMovementSystem.prototype.handle = function(node) {
		for(let i = 0; i < node.colliding.collisions; i++){
			let collision = node.colliding.collisions[i];
			let c_node = this.node_factory.create_node(collision["collider"], ["force", "rotation"], ["position"]);

			if(!c_node.has("position")){
				continue
			}

			let x = (node.position.x - c_node.position.x) / collision["dist"];
			let y = (node.position.y - c_node.position.y) / collision["dist"];

			node.position.x = node.position.x + x * collision["delta"];
			node.position.y = node.position.y + y * collision["delta"];

			let inv_mass = node.has("inventory_mass") ? node.inventory_mass.inventory_mass : 0;

			mom1_x = node.velocity.x**2 * (node.mass.mass + inv_mass);
			mom1_y = node.velocity.y**2 * (node.mass.mass + inv_mass);

			node.velocity.x = 0
			node.velocity.y = 0

			if(c_node.entity_has("mass") and c_node.entity_has("velocity")) {
				c_node.add_or_attach("mass", {});
				c_node.add_or_attach("inventory_mass", {});
				c_node.add_or_attach("velocity", {});

				let inv_mass = c_node.inventory_mass.inventory_mass;

				mom2_x = c_node.velocity.x**2 * (node.mass.mass + inv_mass);
				mom2_y = c_node.velocity.y**2 * (node.mass.mass + inv_mass);

				c_node.velocity.x = 0
				c_node.velocity.y = 0

				node.force.x += (mom1_x + mom_2.x) / 2
				node.force.y += (mom1_y + mom_2.y) / 2

				c_node.force.x -= (mom1_x + mom_2.x) / 2
				c_node.force.y -= (mom1_y + mom_2.y) / 2

			} else {

				node.force.x -= mom1_x;
				node.force.y -= mom1_y;

			}

			c_node.delete_component("colliding")

		}
	}

	return CollisionMovementSystem; 
})();