var gamestate_buffer = new circularArrayBuffer(10);
 //Create a container object called the `stage`
var stage; stage = new PIXI.Container();

var game_state = {
    stage:stage,
    get_input: get_input_gamestate,
    get_state: get_state_gamestate,
    update: update_gamestate,
    render: render_game,
    update_server:update_server
}

function update_gamestate(state, sim_time, unprocessed_input) {
    if(state) {
        update_enemies(state, sim_time);
        state = update_player(state, unprocessed_input, sim_time);
        state.camera = camera_track(camera, state.entities[state.player_id]);
    }
    return state;
}

function get_input_gamestate(my_inputs, keys, time, sim_time) {
    var unprocessed_input;
    var controls = {
        left: keys.left.isDown,
        right: keys.right.isDown,
        thrust: keys.up.isDown,
        brake: keys.d.isDown,
        shoot: keys.f.isDown,
        time: time,
        dt: sim_time,
        was_processed: false,
        was_sent: false
    };
        // Package up and send movement command using simulation time
        
    inputs = my_inputs
    inputs.push(new Input(controls));
    unprocessed_input = inputs.getUnprocessedInput();
    return unprocessed_input;
} 

function get_state_gamestate() {
    return gamestate_buffer.top();
}

function update_server() {
    throttledGetServerData(
        {
            gamestate_buffer:gamestate_buffer,
            inputs:inputs.list
        }
    );
    throttledSendServerData({
        inputs:inputs.list
    });
}

function render_game(renderer, textures, sprites, gamestate, stage){
    var camera = {
        x:  0,
        y:  0,
        width: 1,
        height: 1
    }
    if(gamestate) {
        //for(var e in gamestate.entities){
            camera = gamestate.camera;
            let entity = gamestate.entities[gamestate.player_id];
            if(!(gamestate.player_id in sprites)){
                sprites[gamestate.player_id] = new PIXI.Sprite(textures[entity.type].idle[0]);
                sprites[gamestate.player_id].x = stage.width/2 - sprites[gamestate.player_id].width/2;
                sprites[gamestate.player_id].y = stage.height/2 - sprites[gamestate.player_id].height/2;
                sprites[gamestate.player_id].anchor.x = 0.5;
                sprites[gamestate.player_id].anchor.y = 0.5;
                sprites[gamestate.player_id].frame = 0;

                stage.addChild(sprites[gamestate.player_id])
            }   
            let sprite = sprites[gamestate.player_id];

            sprite.x = entity.position.x - camera.x;
            sprite.y = entity.position.y - camera.y;
            sprite.rotation = entity.rotation;
            entity.state = entity.force.x != 0 || entity.force.y != 0 ? 'accelerating' : 'idle';
            let texture = textures[entity.type][entity.state]
            sprite.texture = texture[Math.floor(sprite.frame)%texture.length];
            sprite.frame += 0.5;
        //}
    }

    if(replay_state && replay_state.render_state){
        
        for(var e in replay_state.render_state.entities){
            if(e === replay_state.render_state.player_id) {
                continue;
            }
            let entity = replay_state.render_state.entities[e];
            if(!(e in sprites)){
                sprites[e] = new PIXI.Sprite(textures[entity.type].idle[0]);
                sprites[e].x = stage.width/2 - sprites[e].width/2;
                sprites[e].y = stage.height/2 - sprites[e].height/2;
                sprites[e].anchor.x = 0.5;
                sprites[e].anchor.y = 0.5;
                sprites[e].frame = 0;

                stage.addChild(sprites[e])    
            }   
            let sprite = sprites[e];

            sprite.x = entity.position.x - camera.x;
            sprite.y = entity.position.y - camera.y;
            sprite.rotation = entity.rotation;
            entity.state = entity.force.x != 0 || entity.force.y != 0 ? 'accelerating' : 'idle';
            let texture = textures[entity.type][entity.state]
            sprite.texture = texture[Math.floor(sprite.frame)%texture.length];
            sprite.frame += 0.5;
        }

    }
    textures.stars.tilePosition.x = -camera.x;
    textures.stars.tilePosition.y = -camera.y;
    
    renderer.render(stage);

    
}