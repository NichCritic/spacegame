
var AnimationSystem = (function() {
	var manditory = ["animated", "renderable"];
	var optional = [];
	var handles = [];

	function AnimationSystem(node_factory) {
		this.node_factory = node_factory;
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

		node.animated.frame = (node.animated.frame + node.animated.update_rate) % spritesheet.length;

		node.renderable.image = spritesheet[Math.floor(node.animated.frame)];

	}

	return AnimationSystem; 
})();