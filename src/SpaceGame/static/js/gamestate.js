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
		thrust:false,
		brake:false,
		shoot:false
	}
	this.rotation = 0;
	this.last_update = 0;
	this.type = 'bolt';
}

function Gamestate(time) {
	this.player_id = "player";
	this.entities = {};
	this.time = time;
}

function physics(entity, control, time) {
	let dt = time;

	if (!dt) {
	 	return entity;
	}

	if(!control){
		control = {
			left: false,
            right: false,
            thrust: false,
            brake: false,
            shoot: false,
            time: 0,
            dt: 100,
            was_processed: false,
            was_sent: false	
		}
	}

	var new_entity = new Entity();
	new_entity.mass = entity.mass;

	let rot_left = (entity.rotation - 1/new_entity.mass * dt);
	let rot_right = (entity.rotation + 1/new_entity.mass * dt);

	new_entity.rotation = control.left ? rot_left : (control.right ? rot_right : entity.rotation);
	
	new_entity.force.x = control.thrust ? dt * 0.1* Math.sin(new_entity.rotation) : 0;
	new_entity.force.y = control.thrust ? -dt * 0.1 * Math.cos(new_entity.rotation) : 0;

	new_entity.acceleration.x = new_entity.force.x/new_entity.mass
    new_entity.acceleration.y = new_entity.force.y/new_entity.mass

    new_entity.velocity.x = entity.velocity.x + new_entity.acceleration.x * dt;
    new_entity.velocity.y = entity.velocity.y + new_entity.acceleration.y * dt;

    if(!control.brake){
    	new_entity.velocity.x *= Math.pow(0.99, dt);
    	new_entity.velocity.y *= Math.pow(0.99, dt);
    }

    new_entity.position.x = entity.position.x + new_entity.velocity.x * dt;
    new_entity.position.y = entity.position.y + new_entity.velocity.y * dt;

    new_entity.control = control;

    new_entity.state = control.thrust ? 'accelerating' : 'idle';

    new_entity.type = entity.type;

    new_entity.last_update = entity.last_update + time;


    return new_entity;
}

function update_gamestate(gamestate, unprocessed) {
	new_gamestate = new Gamestate(0);

	let player = gamestate.entities[gamestate.player_id];
	let time = 0

	for(let i = 0; i < unprocessed.length; i++){
		let cont = unprocessed[i];
		player = physics(player, cont, cont.dt);
		new_gamestate.entities[gamestate.player_id] = player;
		time += cont.dt;	
	}

	for(var i in gamestate.entities) {
		if(i !== gamestate.player_id){
			let e =  gamestate.entities[i];
			let cont = e.control
			let n_e = physics(e, cont, cont.dt);
			new_gamestate.entities[i] = n_e;
		}
	}

	new_gamestate.player_id = gamestate.player_id;
	new_gamestate.time = gamestate.time + time;

	return new_gamestate
}

function consolidate_states(server_state, gamestate_buffer) {
	var gamestate = gamestate_buffer.top();

	if(!gamestate) {
		return server_state;
	}

	var similar_state = gamestate_buffer.find(function(item) {
	return item.time <= server_state.time; 
	});

	server_player = server_state.entities[server_state.player_id];

	if(!similar_state) {
		let new_gamestate = update_gamestate(server_state, server_player.control, gamestate.time);
		return new_gamestate
	}

	similar_state = update_gamestate(similar_state, server_player.control, server_state.time);

	local_player = similar_state.entities[similar_state.player_id];
	

	delta_pos = {};
	delta_pos.x = Math.abs(local_player.position.x - server_player.position.x);
	delta_pos.y = Math.abs(local_player.position.y - server_player.position.y);

	delta_rot = Math.abs(local_player.rotation - server_player.rotation);

	if(delta_pos.x > 10 || delta_pos.y > 10 || delta_rot > 10) {
		let new_gamestate = update_gamestate(server_state, server_player.control, gamestate.time);
		return new_gamestate
	}

	return gamestate;

}

