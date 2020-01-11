var CameraFollowSystem = (function() {
	var manditory = ["player", "position", "velocity", "ship_control"];
	var optional = [];
	var handles = [];
	function CameraFollowSystem(node_factory, textures, width, height) {
		this.node_factory = node_factory;
		this.textures = textures;
		this.width = width;
		this.height = height;
		this.offset_x = 0;
		this.offset_y = 0;
	}

	CameraFollowSystem.prototype.process = function() {
		let node = this.node_factory.create_node_list(manditory, optional)[0];
		let camera = this.node_factory.create_node_list(["camera", "position"])[0];
		if(node && camera) {
			this.handle(node, camera);
		}
	};

	CameraFollowSystem.prototype.handle = function(node, camera) { 
		let brake = !node.ship_control.brake;
		let camera_offset_x = brake ? 0 : node.velocity.x * 250;
		let camera_offset_y = brake ? 0 : node.velocity.y * 500;

		x_return_speed = 3
		y_return_speed = 6

		if(brake) {
			if(this.offset_x > x_return_speed) {
				camera_offset_x = Math.max(camera_offset_x, this.offset_x - x_return_speed);
			} else if (this.offset_x < -x_return_speed) {
				camera_offset_x = Math.min(camera_offset_x, this.offset_x + x_return_speed);
			}

			if(this.offset_y > y_return_speed) {
				camera_offset_y = Math.max(camera_offset_y, this.offset_y - y_return_speed);
			} else if (this.offset_y < -y_return_speed){
				camera_offset_y = Math.min(camera_offset_y, this.offset_y + y_return_speed);
			}
		}

		camera.position.x = node.position.x - this.width/2 + camera_offset_x;
		camera.position.y = node.position.y - this.height/2 + camera_offset_y;

		this.textures.stars.tilePosition.x = -camera.position.x;
        this.textures.stars.tilePosition.y = -camera.position.y;

        this.offset_x = camera_offset_x;
        this.offset_y = camera_offset_y;
	}

	return CameraFollowSystem;
})();

