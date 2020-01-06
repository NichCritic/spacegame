var BeamRenderSystem = (function() {
	var manditory = ["beam", "position", "rotation"];
	var optional = ["charged", "charging", "shooting"];
	var handles = [];
	function BeamRenderSystem(node_factory, canvas) {
		this.node_factory = node_factory
		this.canvas = canvas

		this.entering = [];
		this.onScreen = [];
		this.leaving = [];

		this.displayObjects = {};
	}

	


	BeamRenderSystem.prototype.process = function() {
		let nodes = this.node_factory.create_node_list(manditory, optional);

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
		let entering = !this.displayObjects[node.id] && node.has('shooting');
		let leaving = this.displayObjects[node.id] && !node.has('shooting');
		let onScreen = this.displayObjects[node.id] && node.has('shooting');

		let addChild = false;

		if(leaving) {
			this.canvas.removeChild(this.displayObjects[node.id]);
			delete this.displayObjects[node.id];

			return;
		}



		let x_pos = node.position.x - camera.position.x;
		let y_pos = node.position.y - camera.position.y;

		if(entering) {
			this.displayObjects[node.id] = new PIXI.Graphics();
            this.canvas.addChild(this.displayObjects[node.id]);
            onScreen = true;
		}


		if(onScreen) {
			let v_x = Math.sin(node.rotation.rotation)
			let v_y = -Math.cos(node.rotation.rotation)

			let end_x = x_pos + v_x * node.beam.length;
			let end_y = y_pos + v_y * node.beam.length;

			let beam_width = node.has('charged') ? 10 * (1-node.charged.charge_time / 200) : node.beam.width
			let beam_alpha = node.has('charged') ? 1 : 0.5

	    	this.displayObjects[node.id].clear();
	        this.displayObjects[node.id].lineStyle(beam_width, 0xDDDDFF, beam_alpha);
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