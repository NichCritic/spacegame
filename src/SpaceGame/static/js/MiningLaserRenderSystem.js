var MiningLaserRenderSystem = (function() {
	var manditory = ["renderable", "position"];
	var optional = ["mining"];
	var handles = [];
	function MiningLaserRenderSystem(node_factory, canvas) {
		this.node_factory = node_factory
		this.canvas = canvas

		this.entering = [];
		this.onScreen = [];
		this.leaving = [];

		this.displayObjects = {};
	}

	MiningLaserRenderSystem.prototype.categorize = function(nodes) {
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


	MiningLaserRenderSystem.prototype.process = function() {
		let nodes = this.node_factory.create_node_list(manditory, optional);

		this.categorize(nodes);
		let camera = this.node_factory.create_node_list(["camera", "position"])[0];

		for(let i = 0; i < nodes.length; i++) {
			let node = nodes[i];
			this.handle(node, camera);
			this.cleanup(node);
		}

	};

	MiningLaserRenderSystem.prototype.cleanup = function(node) {
		for(let i = 0; i < handles.length; i++) {
			var comp = handles[i];
			node.delete_component(comp);
		}
	}

	MiningLaserRenderSystem.prototype.get_closest_minable = function(node) {
		let nodes = this.node_factory.create_node_list(['minable', 'position', 'area']);
		let smallest = 251; //Max laser range + 1
		let current = nodes[0];

		for(let i = 0; i < nodes.length; i++) {
			let n = nodes[i];
			let dist = Math.sqrt((node.position.x - n.position.x)**2 + (node.position.y - n.position.y)**2);

			if(dist < smallest) {
				smallest = dist;
				current = n;
			}
		}

		return {
			dist:smallest,
			closest:current
		}

	}

	MiningLaserRenderSystem.prototype.handle = function(node, camera) { 
		let entering = this.entering.indexOf(node.id) !== -1 && node.has('mining');
		let leaving = this.leaving.indexOf(node.id) !== -1 || !node.has('mining');
		let onScreen = this.onScreen.indexOf(node.id) !== -1 && node.has('mining');

		let o = this.get_closest_minable(node);

		let dist = o.dist;
		let closest = o.closest;

		if(dist === 251) {
			//Nothing to mine in range
			return
		}

		if(leaving) {
			this.canvas.removeChild(this.displayObjects[node.id]);
			delete this.displayObjects[node.id];
			return;
		}

		let x_pos = node.position.x - camera.position.x - node.renderable.width/2;
		let y_pos = node.position.y - camera.position.y - node.renderable.height/2;

		if(entering) {
			this.displayObjects[node.id] = new PIXI.Graphics(node.renderable.image);
            this.canvas.addChild(this.displayObjects[node.id]);
            this.onScreen.push(node.id);
		}

		let v_x = node.position.x - closest.position.x;
		let v_y = node.position.y - closest.position.y;

		let n_x = v_x / dist;
		let n_y = v_y / dist;

		let start_x = closest.position.x + n_x * closest.area.radius
    	let start_y = closest.position.y + n_y * closest.area.radius

    	let line_end_x = start_x - camera.position.x - node.renderable.width/2;
    	let line_end_y = start_y - camera.position.y - node.renderable.width/2;

    	this.displayObjects[node.id].clear();
        this.displayObjects[node.id].lineStyle(3, 0xFF0000);
        this.displayObjects[node.id].moveTo(x_pos, y_pos);
        this.displayObjects[node.id].lineTo(line_end_x, line_end_y);

	}

	return MiningLaserRenderSystem;
})();

