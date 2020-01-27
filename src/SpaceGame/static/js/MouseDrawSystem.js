
var MouseDrawSystem = (function() {

	function MouseDrawSystem(node_factory, textures) {
		var self = this;
		this.node_factory = node_factory;
		this.mousedown = null;
		this.mouse_x = 0;
		this.mouse_y = 0;
		this.textures = textures;
		this.touches = [];


		window.onmousedown = function(event) {      
			self.mousedown = true;
        }

        window.onmousemove = function(event) {
        	self.mouse_x = event.clientX;
        	self.mouse_y = event.clientY;
        }

        window.onmouseup = function(event) {
        	self.mousedown = false;
        }

        window.ontouchstart = function(event) {
        	if(!document.fullscreenElement) {
        		 document.getElementById("gamestuff").requestFullscreen()
        	}
			self.mousedown = true;
			self.touches = event.touches;
			//event.preventDefault();
        }

        window.ontouchmove = function(event) {
        	self.mouse_x = event.touches[0].clientX;
        	self.mouse_y = event.touches[0].clientY;
        	self.touches = event.touches;
        	//event.preventDefault();
        }

        
        window.ontouchend = function(event) {
        	self.mousedown = false;
        	self.touches = event.touches;
        	//event.preventDefault();
        }


	}

	MouseDrawSystem.prototype.process = function(dt) {
		if(this.mousedown) {
			let player = this.node_factory.create_node_list(["player"])[0];
			if(!player) {
				return;
			}
            let camera = this.node_factory.create_node_list(["camera", "position"])[0];

            let m_x = 1200/window.innerWidth * this.mouse_x;
            let m_y = 600/window.innerHeight * this.mouse_y;

            let w_x = m_x + camera.position.x;
            let w_y = m_y + camera.position.y;

            player.add_or_attach("waypoints", {});

            player.waypoints.waypoints[0] = {x: w_x, y:w_y};

            if(this.touches.length > 1) {
        		player.add_or_attach("shooting", {firing_rate:200});
				player.shooting.input = {shoot: true, dt: dt};
            }

            // let wp = this.node_factory.create_node([]);
            // wp.add_or_attach('waypoint', {});
            // wp.add_or_attach('position', {x: w_x, y:w_y});
            // wp.add_or_update("renderable", {spritesheet: this.textures["target"],
            //        image:this.textures["target"].idle[0],
            //        width: 300,
            //        height: 300});
		} else {
			// waypoints = this.node_factory.create_node_list(['waypoint']);
			// for(let i = 0; i < waypoints.length; i++) {
			// 	waypoints[i].add_or_attach("to_be_removed");
			// }

			let player = this.node_factory.create_node_list(["player", "waypoints"])[0];
			if(player) {
				player.delete_component('waypoints');
			}
		}
	};

	return MouseDrawSystem; 
})();

