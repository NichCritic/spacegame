
var ExpirySystem = (function() {
	var manditory = ['expires'];
	var optional = [];
	var handles = [];

	function ExpirySystem(node_factory, textures) {
		this.node_factory = node_factory;
		this.textures = textures;
	}

	ExpirySystem.prototype.process = function() {
		var nodes = this.node_factory.create_node_list(manditory, optional);
		for(let i = 0; i < nodes.length; i++) {
			let node = nodes[i];
			this.handle(node);
			this.cleanup(node);
		}

	};

	ExpirySystem.prototype.cleanup = function(node) {
		return;
	}

	ExpirySystem.prototype.handle = function(node) {
		var now = Date.now();

		if(node.expires.expiry_time_ms < now - node.expires.creation_time) {
			node.add_or_attach("to_be_removed")
		}
	}

	return ExpirySystem; 
})();