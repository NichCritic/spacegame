
var AnimationStateSystem = (function() {
	var manditory = ["animation_state", "acceleration"];
	var optional = [];
	var handles = [];

	function AnimationStateSystem(node_factory) {
		this.node_factory = node_factory;
		this.last_update = Date.now();
	}

	AnimationStateSystem.prototype.process = function() {
		var nodes = this.node_factory.create_node_list(manditory, optional);
		for(let i = 0; i < nodes.length; i++) {
			let node = nodes[i];
			this.handle(node);
			this.cleanup(node);
		}

	};

	AnimationStateSystem.prototype.cleanup = function(node) {
		for(let i = 0; i < handles.length; i++) {
			var comp = handles[i];
			node.delete_component(comp);
		}
	}

	AnimationStateSystem.prototype.handle = function(node) {
		if(node.acceleration.x !== 0 || node.acceleration.y !== 0) {
			node.animation_state.state = 'accelerating';
		}
		else{
			node.animation_state.state = 'idle';
		}
		

	}

	return AnimationStateSystem; 
})();