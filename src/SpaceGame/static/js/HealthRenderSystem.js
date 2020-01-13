var HealthRenderSystem = (function() {
	var manditory = ["renderable", "position", "health", "display_health"];
	var optional = [];
	var handles = [];
	function HealthRenderSystem(node_factory, canvas) {
		this.node_factory = node_factory
		this.canvas = canvas

		this.entering = [];
		this.onScreen = [];
		this.leaving = [];

		this.displayObjects = {};
	}

	HealthRenderSystem.prototype.categorize = function(nodes) {
		let ids = [];
		let newEntering = [];
		let newOnScreen = [];
		let newLeaving = [];

		for(let i = 0; i < nodes.length; i++) {
			let n_id = nodes[i].id;
			ids.push(n_id);
			let entering = this.onScreen.indexOf(n_id) == -1;
			if(entering) {
				newEntering.push(n_id);
			}

			if(nodes[i].entity_has("to_be_removed")) {
				newLeaving.push(n_id);
			}

		}

		

		for(let i = 0; i < this.onScreen.length; i++) {
			let e_id = this.onScreen[i];
			let on_screen = ids.indexOf(e_id) !== -1;
			let leaving = !on_screen;

			if (on_screen) {
				newOnScreen.push(e_id);
			}			
		}

		this.entering = newEntering;
		this.onScreen = newOnScreen;
		this.leaving = newLeaving;

	}


	HealthRenderSystem.prototype.process = function() {
		let nodes = this.node_factory.create_node_list(manditory, optional);

		this.categorize(nodes);
		let camera = this.node_factory.create_node_list(["camera", "position"])[0];

		for(let i = 0; i < nodes.length; i++) {
			let node = nodes[i];
			this.handle(node, camera);
			this.cleanup(node);
		}

	};

	HealthRenderSystem.prototype.cleanup = function(node) {
		for(let i = 0; i < handles.length; i++) {
			var comp = handles[i];
			node.delete_component(comp);
		}
	}

	HealthRenderSystem.prototype.handle = function(node, camera) { 
		let entering = this.entering.indexOf(node.id) !== -1;
		let leaving = this.leaving.indexOf(node.id) !== -1;
		let onScreen = this.onScreen.indexOf(node.id) !== -1;

		if(leaving) {
			this.canvas.removeChild(this.displayObjects[node.id]);
			delete this.displayObjects[node.id];
			return;
		}

		let x_pos = node.position.x - camera.position.x - node.renderable.width/2;
		let y_pos = node.position.y - camera.position.y - node.renderable.height/2 - 10;

		if(entering) {
			this.displayObjects[node.id] = new PIXI.Graphics(node.renderable.image);
            this.displayObjects[node.id].beginFill(0x33FF55);
            this.displayObjects[node.id].drawRect(0, 0, node.renderable.width, 2);
            this.displayObjects[node.id].endFill();

            this.canvas.addChild(this.displayObjects[node.id]);
            this.onScreen.push(node.id);
		}

		if(this.displayObjects[node.id]) {
			this.displayObjects[node.id].x = x_pos;
			this.displayObjects[node.id].y = y_pos;
			if(node.health.health >= node.health.max_health) {
				this.displayObjects[node.id.width] = 0
			} else {
				this.displayObjects[node.id].width = node.renderable.width * node.health.health / node.health.max_health;
			}
		}

	}

	return HealthRenderSystem;
})();

