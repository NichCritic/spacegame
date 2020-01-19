
var WaypointSystem = (function() {
	var manditory = ["waypoint", "position", "rotation", "control"];
	var optional = [];
	var handles = [];

	function WaypointSystem(node_factory, inputs) {
		this.node_factory = node_factory;
		this.inputs = inputs;
	}

	WaypointSystem.prototype.process = function() {
		var nodes = this.node_factory.create_node_list(manditory, optional);
		var camera = this.node_factory.create_node_list(["camera", "position"])[0];
		for(let i = 0; i < nodes.length; i++) {
			let node = nodes[i];
			this.handle(node, camera);
			this.cleanup(node);
		}

	};

	WaypointSystem.prototype.cleanup = function(node) {
		for(let i = 0; i < handles.length; i++) {
			var comp = handles[i];
			node.delete_component(comp);
		}
	}

	

	WaypointSystem.prototype.handle = function(node, camera) {
		if(node.waypoint.waypoints.length == 0) {
			node.delete_component("waypoint");
			return;
		}
		let unprocessed_input =  this.inputs.getUnprocessedInput();
		let latest_input = unprocessed_input[unprocessed_input.length-1];
		//Handle the first waypoint
		let waypoint = node.waypoint.waypoints[0];
		let w_x = waypoint.x //- camera.position.x;
		let w_y = waypoint.y //- camera.position.y;

		let p_x = node.position.x //- camera.position.x;
		let p_y = node.position.y //- camera.position.y;

		let dist = Math.sqrt((w_x-p_x)**2 + (w_y - p_y) **2)
		if(dist < 150) {
			node.waypoint.waypoints.shift();
			return
		}

		let a = (Math.atan2(p_y - w_y, p_x - w_x) - Math.PI/2);



		let a1 = Math.atan2(w_y - camera.position.y, w_x - camera.position.x);
		let a2 = Math.atan2(p_y - camera.position.y, p_x - camera.position.x);

		let left = a1 < a2; 

		let angle = (node.rotation.rotation - a) % (Math.PI*2);
		let minus_angle = angle - Math.PI*2

		angle = Math.abs(angle) < Math.abs(minus_angle) ? angle : minus_angle;

		if(angle < 0.25 && angle > -0.25) {
			node.control.thrust = true;
			latest_input.thrust = true;
		} else {
			if (angle > Math.PI || angle < -Math.PI) {
				node.control.brake = false;
				latest_input.brake = false;
			}

			if(left) {
				node.control.left = true;
				latest_input.left = true;
				// node.control.brake = false;
				// latest_input.brake = false;
			} else {
				node.control.right = true;
				latest_input.right = true;
				// node.control.brake = false;
				// latest_input.brake = false;
			}			
		}

		// if(dist < 100) {
		// 	latest_input.brake = false;
		// 	node.control.brake = false;
		// }

		
	}

	return WaypointSystem; 
})();

