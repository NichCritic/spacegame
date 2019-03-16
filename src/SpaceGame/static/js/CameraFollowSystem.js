var CameraFollowSystem = (function() {
	var manditory = ["player", "position"];
	var optional = [];
	var handles = [];
	function CameraFollowSystem(node_factory, textures) {
		this.node_factory = node_factory;
		this.textures = textures;
	}

	CameraFollowSystem.prototype.process = function() {
		let node = this.node_factory.create_node_list(manditory, optional)[0];
		let camera = this.node_factory.create_node_list(["camera", "position"])[0];
		if(node && camera) {
			this.handle(node, camera);
		}
	};

	CameraFollowSystem.prototype.handle = function(node, camera) { 
		camera.position.x = node.position.x - 600;
		camera.position.y = node.position.y - 300;

		this.textures.stars.tilePosition.x = -camera.position.x;
        this.textures.stars.tilePosition.y = -camera.position.y;
	}

	return CameraFollowSystem;
})();

