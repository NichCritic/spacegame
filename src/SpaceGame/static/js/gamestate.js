function Entity() {
	this.position = {
		x:0, y:0
	};
	this.mass = 1;
	this.radius = 1;
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
	this.physics_packets = []
	this.rotation = 0;
	this.last_update = 0;
	this.type = 'bolt';
}

function clone_entity(entity) {
	var new_entity = new Entity();
	new_entity.position.x = entity.position.x;
	new_entity.position.y = entity.position.y;
	new_entity.mass = entity.mass;
	new_entity.radius = entity.radius;
	new_entity.velocity.x = entity.velocity.x;
	new_entity.velocity.y = entity.velocity.y;
	new_entity.acceleration.x = entity.acceleration.x;
	new_entity.acceleration.y = entity.acceleration.y;
	new_entity.force.x = entity.force.x;
	new_entity.force.y = entity.force.y;
	new_entity.state = entity.state;
	new_entity.physics_packets = entity.physics_packets;
	new_entity.rotation = entity.rotation;
	new_entity.last_update = entity.last_update;
	new_entity.type = entity.type;
	return new_entity;
}

function Gamestate(time) {
	this.player_id = "player";
	this.client_entities = []
	this.entities = {};
	this.time = time;
	this.camera = {};
}

function packet_physics(entity, packet){
	let dt = packet.dt

	var new_entity = new Entity();
	new_entity.mass = entity.mass; 
	new_entity.rotation = packet.rotation;
	
	new_entity.force.x = packet.force.x;
	new_entity.force.y = packet.force.y;

	new_entity.acceleration.x = new_entity.force.x/new_entity.mass
    new_entity.acceleration.y = new_entity.force.y/new_entity.mass

    new_entity.velocity.x = entity.velocity.x + new_entity.acceleration.x * dt;
    new_entity.velocity.y = entity.velocity.y + new_entity.acceleration.y * dt;

    if(!packet.brake){
    	new_entity.velocity.x *= Math.pow(0.99, dt);
    	new_entity.velocity.y *= Math.pow(0.99, dt);
    }

    new_entity.position.x = entity.position.x + new_entity.velocity.x * dt;
    new_entity.position.y = entity.position.y + new_entity.velocity.y * dt;

    new_entity.type = entity.type;

    new_entity.last_update = entity.last_update + dt;

    return new_entity;
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

function interpolate(p1, p2, proportion) {

}

var EnemyState = (function(){
	function EState(){
		this.previous_state = null;
		this.render_state = null;
		this.server_state = null; 
		this.t = 0;
	}	

	EState.prototype = {
		tick: _tick,
		update: _update
	}

	function _tick(dt) {
		if(!this.previous_state){
			return;
		}
		if(this.render_state.time >= this.server_state.time){
			//Up to date
			return;
		}
		this.t += dt;

		let update_time = this.server_state.time - this.previous_state.time;
		let update_proportion = this.t / update_time;
		if(update_proportion > 1){
			update_proportion = 1;
		}

		for(let e in this.render_state.entities) {
			if(e === this.server_state.player_id){
				continue;
			}
			if(!(e in this.server_state) || !(e in this.previous_state)) {
				continue
			}
			let prv = this.previous_state.entities[e];
			let srv = this.server_state.entities[e];
			let px = prv.position.x;
			let py = prv.position.y;
			let sx = srv.position.x;
			let sy = srv.position.y;
			let new_x = px + ((sx-px)*update_proportion);
			let new_y = py + ((sy-py)*update_proportion);
			this.render_state.entities[e].position.x = new_x;
			this.render_state.entities[e].position.y = new_y;

		}
		
		if(update_proportion >= 1){
			//Set the render state to the server state if we're caught up
			this.update(this.server_state);
		}
	}

	function _update(new_server_state){
		this.previous_state = this.server_state;
		this.render_state = this.server_state;
		this.server_state = new_server_state;
		this.t = 0
	}




	return EState;
})();

var replay_state = new EnemyState();


function update_player(gamestate, unprocessed, dt) {
	let new_gamestate = new Gamestate(0);
	let player = gamestate.entities[gamestate.player_id];
	let time = 0

	for(let e in gamestate.entities){
		if(e !== gamestate.player_id){
			new_gamestate.entities[e] = gamestate.entities[e];
		}
	}

	for(let i = 0; i < unprocessed.length; i++){
		let cont = unprocessed[i];
		player = physics(player, cont, cont.dt);
		new_gamestate.entities[gamestate.player_id] = player;
		time += cont.dt;	
	}

	new_gamestate.player_id = gamestate.player_id;
	new_gamestate.time = gamestate.time + time;

	return new_gamestate
}

function update_enemies(gamestate, dt) {
	if(!replay_state.server_state){
		replay_state.update(gamestate);
	}
	if(gamestate.time > replay_state.server_state.time){
		replay_state.update(gamestate);
	}
	replay_state.tick(dt);
}

/*
	TODO: Doesn't handle two objects in motion very well
*/
function detect_and_resolve_collisions(gamestate) {
	var new_entities = {};
	for(var e1_id in gamestate.entities) {
		var e1 = clone_entity(gamestate.entities[e1_id]);
		if(e1.velocity.x == 0 && e1.velocity.y == 0) {
			new_entities[e1_id] = e1;
			continue;
		}

		for(var e2_id in gamestate.entities) {
			if(e1_id != e2_id) {
				var e2 = clone_entity(gamestate.entities[e2_id]);
				var dist = Math.sqrt((e1.position.x-e2.position.x)*(e1.position.x-e2.position.x)+(e1.position.y-e2.position.y)*(e1.position.y-e2.position.y));
				if(dist < e1.radius+e2.radius){
					let delta = e1.radius + e2.radius - dist;
					let norm_vec = {
						x: (e1.position.x - e2.position.x) / dist,
						y: (e1.position.y - e2.position.y) / dist
					}
					e1.position.x = e1.position.x + norm_vec.x * delta;
					e1.position.y = e1.position.y + norm_vec.y * delta;

					mom1 = {
						x: e1.velocity.x * e1.mass,
						y: e1.velocity.y * e1.mass
					}

					e1.force.x = -(e1.force.x+mom1.x);
					e1.force.y = -(e1.force.y+mom1.y);
				}
			}

		}
		new_entities[e1_id] = e1; 
	}
	gamestate.entities = new_entities;
	return gamestate;
}


