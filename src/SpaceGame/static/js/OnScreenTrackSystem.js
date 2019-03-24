
var OnScreenTrackSystem = (function() {
	var manditory = ["server_controlled", "renderable"];
	var optional = [];
	var handles = [];

	function OnScreenTrackSystem(node_factory) {
		this.node_factory = node_factory;
	}

	OnScreenTrackSystem.prototype.process = function() {
		var nodes = this.node_factory.create_node_list(manditory, optional);
		for(let i = 0; i < nodes.length; i++) {
			let node = nodes[i];
			this.handle(node);
			this.cleanup(node);
		}

	};

	OnScreenTrackSystem.prototype.cleanup = function(node) {
		for(let i = 0; i < handles.length; i++) {
			var comp = handles[i];
			node.delete_component(comp);
		}
	}

	OnScreenTrackSystem.prototype.handle = function(node) {
		if(!node.entity_has("on_screen")) {
			node.add_or_attach("remove_sprite");
			return;
		}
		node.delete_component("on_screen");
	}

	return OnScreenTrackSystem; 
})();