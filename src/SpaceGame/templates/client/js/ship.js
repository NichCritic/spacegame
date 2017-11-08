(function(){
	function ShipPhysics() {
		this.x = 0;
		this.y = 0;
		this.vel = {};
		this.vel.x = 0;
		this.vel.y = 0;
		this.accel = {};
		this.accel.x = 0;
		this.accel.y = 0;
		this.force = {};
		this.force.x = 0;
		this.force.y = 0;
		this.mass = 20;
		this.rotation = 0;
	}

	ShipPhysics.prototype = {
		update: function(ship, dt) {

			ship.accel.x = ship.force.x / ship.mass;
			ship.accel.y = ship.force.y / ship.mass;

			ship.vel.x += ship.accel.x * dt;
			ship.vel.y += ship.accel.y * dt;

			ship.x += ship.vel.x * dt;
			ship.y += ship vel.y * dt;
		}
	}

	return Ship;
})()