var TouchController = (function(){

	function TouchController() {
		this.touches = [];
		

		this.listeners = {
			"touchmove":[],
			"touchdown":[],
			"touchend":[]
		};
		
		

        window.ontouchstart = function(event) {
        	if(!document.fullscreenElement) {
        		 document.getElementById("gamestuff").requestFullscreen()
        	}
			self.mousedown = true;
			//event.preventDefault();
        }

        window.ontouchmove = function(event) {
        	self.mouse_x = event.touches[0].clientX;
        	self.mouse_y = event.touches[0].clientY;
        	//event.preventDefault();
        }
 
        window.ontouchend = function(event) {
        	self.mousedown = false;
        	//event.preventDefault();
        }	
	}

	TouchController.prototype.add_listener = function(event, listener) {
		
	};


	return TouchController;
})();