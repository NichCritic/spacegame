var BeamRenderSystem = (function() {
	var manditory = ["beam", "position", "rotation"];
	var optional = ["charged", "charging"];
	var handles = [];
	function BeamRenderSystem(node_factory, canvas) {
		this.node_factory = node_factory
		this.canvas = canvas

		this.entering = [];
		this.onScreen = [];
		this.leaving = [];

		this.displayObjects = {};
	}

	BeamRenderSystem.prototype.categorize = function(nodes) {
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
			let node = this.node_factory.create_node([], e_id);
			if(node.entity_has("to_be_removed")) {
				newLeaving.push(e_id);
				continue;
			}

			if (on_screen) {
				newOnScreen.push(e_id);
			}


		}

		this.entering = newEntering;
		this.onScreen = newOnScreen;
		this.leaving = newLeaving;

	}


	BeamRenderSystem.prototype.process = function() {
		let nodes = this.node_factory.create_node_list(manditory, optional);

		this.categorize(nodes);
		let camera = this.node_factory.create_node_list(["camera", "position"])[0];

		for(let i = 0; i < nodes.length; i++) {
			let node = nodes[i];
			this.handle(node, camera);
			this.cleanup(node);
		}

	};

	BeamRenderSystem.prototype.cleanup = function(node) {
		for(let i = 0; i < handles.length; i++) {
			var comp = handles[i];
			node.delete_component(comp);
		}
	}

	BeamRenderSystem.prototype.handle = function(node, camera) { 
		let entering = this.entering.indexOf(node.id) !== -1;
		let leaving = this.leaving.indexOf(node.id) !== -1;
		let onScreen = this.onScreen.indexOf(node.id) !== -1;

		let addChild = false;

		if(leaving) {
			this.canvas.removeChild(this.displayObjects[node.id]);
			delete this.displayObjects[node.id];
			if(node.entity_has("to_be_removed")) {
				node.delete_all_components();
			}
			if(onScreen) {
				delete this.onScreen[this.onScreen.indexOf(node.id)]
				onScreen = false;
			}

			return;
		}



		let x_pos = node.position.x - camera.position.x;
		let y_pos = node.position.y - camera.position.y;
		
		if(entering) {
			this.displayObjects[node.id] = new PIXI.Graphics();
            this.canvas.addChild(this.displayObjects[node.id]);
            this.onScreen.push(node.id);
            onScreen = true;
		}


		if(onScreen) {
			let v_x = Math.sin(node.rotation.rotation)
			let v_y = -Math.cos(node.rotation.rotation)

			let end_x = x_pos + v_x * node.beam.length;
			let end_y = y_pos + v_y * node.beam.length;

	    	this.displayObjects[node.id].clear();
	        this.displayObjects[node.id].lineStyle(node.beam.width, 0xDDDDFF);
	        this.displayObjects[node.id].moveTo(x_pos, y_pos);
	        this.displayObjects[node.id].lineTo(end_x, end_y);

			if(x_pos > 2500 || x_pos < -2500 || y_pos > 2500 || y_pos < -2500){
				node.add_or_attach("to_be_removed")
			}
		}

		if(addChild) {
			this.canvas.addChild(this.displayObjects[node.id]);
		}

	}

	return BeamRenderSystem;
})();