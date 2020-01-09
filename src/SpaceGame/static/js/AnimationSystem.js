
var AnimationSystem = (function() {
	var manditory = ["animated", "animation_state", "renderable"];
	var optional = [];
	var handles = [];

	function AnimationSystem(node_factory) {
		this.node_factory = node_factory;
	}

	AnimationSystem.prototype.process = function(dt) {
		var nodes = this.node_factory.create_node_list(manditory, optional);
		for(let i = 0; i < nodes.length; i++) {
			let node = nodes[i];
			this.handle(node, dt);
			this.cleanup(node);
		}

	};

	AnimationSystem.prototype.cleanup = function(node) {
		for(let i = 0; i < handles.length; i++) {
			var comp = handles[i];
			node.delete_component(comp);
		}
	}

	AnimationSystem.prototype.handle = function(node, dt) {
		//TODO: only handles idle state
		
		
		let spritesheet = node.renderable.spritesheet.idle;

		if(node.renderable.spritesheet[node.animation_state.state] != null) {
			spritesheet = node.renderable.spritesheet[node.animation_state.state];
		}



		node.animated.residual_cooldown += dt;

		if(node.animated.residual_cooldown >= node.animated.update_rate) {
			let frames = Math.floor(node.animated.residual_cooldown/node.animated.update_rate);
			node.animated.frame = (node.animated.frame + frames) % spritesheet.length;
			node.animated.residual_cooldown -= node.animated.update_rate * frames
			// console.log(node.animated.frame);
		}

		node.renderable.image = spritesheet[Math.floor(node.animated.frame)];


	}

	return AnimationSystem; 
})();