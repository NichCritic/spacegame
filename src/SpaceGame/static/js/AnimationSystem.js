
var AnimationSystem = (function() {
	var manditory = ["animated", "renderable"];
	var optional = [];
	var handles = [];

	function AnimationSystem(node_factory) {
		this.node_factory = node_factory;
		this.last_update = Date.now();
	}

	AnimationSystem.prototype.process = function() {
		var nodes = this.node_factory.create_node_list(manditory, optional);
		for(let i = 0; i < nodes.length; i++) {
			let node = nodes[i];
			this.handle(node);
			this.cleanup(node);
		}

	};

	AnimationSystem.prototype.cleanup = function(node) {
		for(let i = 0; i < handles.length; i++) {
			var comp = handles[i];
			node.delete_component(comp);
		}
	}

	AnimationSystem.prototype.handle = function(node) {
		//TODO: only handles idle state
		let spritesheet = node.renderable.spritesheet.idle;

		let now = Date.now();
		let dt = now - this.last_update;

		node.animated.residual_cooldown += dt;

		if(node.animated.residual_cooldown >= node.animated.update_rate) {
			let frames = Math.floor(node.animated.residual_cooldown/node.animated.update_rate);
			node.animated.frame = (node.animated.frame + frames) % spritesheet.length;
			node.animated.residual_cooldown -= node.animated.update_rate * frames
			console.log(node.animated.frame);
		}

		node.renderable.image = spritesheet[Math.floor(node.animated.frame)];

		this.last_update = now;

	}

	return AnimationSystem; 
})();