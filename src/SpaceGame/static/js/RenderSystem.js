var RenderSystem = (function() {
	var manditory = ["renderable", "position", "area"];
	var optional = ["rotation"];
	var handles = [];
	function RenderSystem(node_factory, canvas) {
		this.node_factory = node_factory
		this.canvas = canvas

		this.entering = [];
		this.onScreen = [];
		this.leaving = [];

		this.displayObjects = {};
	}

	RenderSystem.prototype.categorize = function(nodes) {
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

		}

		

		for(let i = 0; i < this.onScreen.length; i++) {
			let e_id = this.onScreen[i];
			let on_screen = ids.indexOf(e_id) !== -1;
			let leaving = !on_screen;

			if (on_screen) {
				newOnScreen.push(e_id);
			}
			if (leaving) {
				newLeaving.push(e_id)
			}
		}

		this.entering = newEntering;
		this.onScreen = newOnScreen;
		this.leaving = newLeaving;

	}


	RenderSystem.prototype.process = function() {
		let nodes = this.node_factory.create_node_list(manditory, optional);

		this.categorize(nodes);
		let camera = this.node_factory.create_node_list(["camera", "position"])[0];

		for(let i = 0; i < nodes.length; i++) {
			let node = nodes[i];
			this.handle(node, camera);
			this.cleanup(node);
		}

	};

	RenderSystem.prototype.cleanup = function(node) {
		for(let i = 0; i < handles.length; i++) {
			var comp = handles[i];
			node.delete_component(comp);
		}
	}

	RenderSystem.prototype.handle = function(node, camera) { 
		let entering = this.entering.indexOf(node.id) !== -1;
		let leaving = this.leaving.indexOf(node.id) !== -1;
		let onScreen = this.onScreen.indexOf(node.id) !== -1;

		if(leaving) {
			this.canvas.removeChild(this.displayObjects[node.id]);
			delete this.displayObjects[node.id];
			return;
		}

		if(entering) {
			this.displayObjects[node.id] = new PIXI.Sprite(node.renderable.spritesheet["default"][0]);
			this.displayObjects[node.id].anchor.x = 0.5;
            this.displayObjects[node.id].anchor.y = 0.5;
            this.canvas.addChild(this.displayObjects[node.id]);
            this.onScreen.push(node.id);
		}

		let x_pos = node.position.x - camera.position.x;
		let y_pos = node.position.y - camera.position.y;

		this.displayObjects[node.id].x = x_pos;
		this.displayObjects[node.id].y = y_pos;
		this.displayObjects[node.id].width = node.area.radius * 2;
		this.displayObjects[node.id].height = node.area.radius * 2;

		if(node.has("rotation")) {
			this.displayObjects[node.id].rotation = node.rotation.rotation;
		}

	}

	return RenderSystem;
})();

