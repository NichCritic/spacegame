function Entity() {
	this.position = {
		x:0, y:0
	};
	this.mass = 1;
	this.velocity = {
		x:0, y:0
	};
	this.acceleration = {
		x:0, y:0
	};
	this.force = {
		x:0, y:0
	}
	this.state = "idle"
	this.control = {
		left:false,
		right:false,
		thrust:false
	}
	this.rotation = 0;
	this.time_stamp = 0;
}

function Gamestate(time) {
	this.entities = {};
	this.time = time;
}

function physics(entity, control, time) {
	let dt = time - entity.time_stamp;

	if (dt <= 0) {
		return entity;
	}

	var new_entity = new Entity();
	new_entity.mass = entity.mass;

	let rot_left = (entity.rotation - 1/new_entity.mass * dt);
	let rot_right = (entity.rotation + 1/new_entity.mass * dt);

	new_entity.rotation = control.left ? rot_left : (control.right ? rot_right : entity.rotation);
	
	new_entity.force.x = control.thrust ? 1 * Math.sin(new_entity.rotation) : 0;
	new_entity.force.y = control.thrust ? -1 * Math.cos(new_entity.rotation) : 0;

	new_entity.acceleration.x = new_entity.force.x/new_entity.mass
    new_entity.acceleration.y = new_entity.force.y/new_entity.mass

    new_entity.velocity.x = entity.velocity.x + new_entity.acceleration.x * dt;
    new_entity.velocity.y = entity.velocity.y + new_entity.acceleration.y * dt;

    if(!control.brake){
    	new_entity.velocity.x *= 0.95;
    	new_entity.velocity.y *= 0.95;
    }

    new_entity.position.x = entity.position.x + new_entity.velocity.x * dt;
    new_entity.position.y = entity.position.y + new_entity.velocity.y * dt;

    new_entity.control = control;

    new_entity.state = control.thrust ? 'accelerating' : 'idle';

    new_entity.time_stamp = time;

    return new_entity;
}

function update_gamestate(gamestate, control, time) {
	new_gamestate = new Gamestate(time);

	for(var i in gamestate.entities){
		let e =  gamestate.entities[i];
		let n_e = physics(e, control, time);
		new_gamestate.entities[i] = n_e;
	}

	return new_gamestate
}


