var EnemyReplay = (function(){
	function EnemyReplay(){
		this.entities = {};
		this.entity_packets = {};
		this.entity_time = {};
		this.time = Date.now();
	}
	EnemyReplay.prototype = {
		update:_update,
		tick:_tick,
	}

	

	function _tick(dt) {
		for(var i in this.entities){
			let e = this.entities[i];
			var new_e = e;
			packets = find_updates(this.entity_packets[i], this.time, this.time+dt);
			for(p in packets){
				let pack = packets[p];
				new_e = packet_physics(new_e, pack)
				this.entity_time[i] = pack.time + pack.dt
			}
			this.entities[i] = new_e;
		}
		

		this.time += dt
	}

	function _update(id, entity){
		let last = entity.state_history.length-1;
		let last_update = entity.state_history[last]
		//Hack, attach the type to the state for rendering, 
		//but really the data needed for rendering should be removed seperately
		last_update.type = entity.type;
		last_update.mass = entity.mass;
		if(!(id in this.entities)){

			this.entities[id] = last_update;
			this.entity_packets[id] = last_update.physics_packets;
			this.entity_time[id] = last_update.time;
			this.time = last_update.time;
			//return;
		}

		let new_packets = [];
		let latest_time = this.entity_time[id];
		for(let p in this.entity_packets[id]){
			let pack = this.entity_packets[id][p];
			if(pack.time > latest_time){
				new_packets.push(pack);
				latest_time = pack.time
			}
		}

		for(let p in last_update.physics_packets){
			let pack = last_update.physics_packets[p];
			if(pack.time > latest_time) {
				new_packets.push(pack);
				latest_time = pack.time
			}
		}
		this.entity_packets[id] = new_packets;
	}

	function find_updates(packets, start, end){
		var res = [];
		for(var i = 0; i < packets.length; i++){
			packet = packets[i];
			if(packet.time >= start && packet.time < end){
				res.push(packet)
			}
		}
		return res
	}


	return EnemyReplay;
})();

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
	this.physics_packets = []
	this.rotation = 0;
	this.last_update = 0;
	this.type = 'bolt';
}

function Gamestate(time) {
	this.player_id = "player";
	this.entities = {};
	this.time = time;
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

var replay_state = new EnemyReplay();

function update_gamestate(gamestate, unprocessed, dt) {
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
			let e = gamestate.entities[i];
			replay_state.update(i, e);
			replay_state.tick(dt);
			new_gamestate.entities[i] = e;
			new_gamestate.entities[i].position = replay_state.entities[i].position;
		}
	}

	new_gamestate.player_id = gamestate.player_id;
	new_gamestate.time = gamestate.time + time;

	return new_gamestate
}


