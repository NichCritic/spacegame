var GameLoop = (function() {
    var gamestate_buffer = new circularArrayBuffer(10);
     //Create a container object called the `stage`
    var stage; stage = new PIXI.Container();
    var lasers; lasers = new PIXI.Container();
    var entities; entities = new PIXI.Container();

    var textures, sprites;

    sprites = [];

    var game_state = {
        init: setup,
        stage:stage,
        get_input: get_input_gamestate,
        get_state: get_state_gamestate,
        update: update_gamestate,
        render: render_game,
        update_server:update_server
    }

    function getTexturesFromSpritesheet(mySpriteSheetImage, count, rows, imgW, imgH){
        var textures = [];
        var countPerRow = Math.floor(count/rows);

        for(var i = 0; i < count; i++) {
            let x = (i % countPerRow) * imgW;
            let y = Math.floor(i/countPerRow) * imgH;
            let frame = new PIXI.Rectangle(x, y, imgW, imgH);
            let texture = new PIXI.Texture(mySpriteSheetImage, frame);
            textures.push(texture);
        }
        return textures
    }

    function setup() {
        bg = new PIXI.Sprite(
            PIXI.loader.resources["static/assets/parallax-space-background2.png"].texture
        );

        bg.width = 1200; 

        stars = new PIXI.extras.TilingSprite(
            PIXI.loader.resources["static/assets/parallax-space-stars2.png"].texture
        , 1200, 600);
        

        var ship_accel  = PIXI.BaseTexture.fromImage("static/assets/ship.png");
        var ship_idle = PIXI.BaseTexture.fromImage("static/assets/ship_idle.png");

        var bolt = PIXI.BaseTexture.fromImage("static/assets/laser-bolt.png")
        // var spacestation1 = PIXI.BaseTexture.fromImage("static/assets/spacestation1.png")

        textures = {}
        textures.ship = {}
        textures.ship.accelerating = getTexturesFromSpritesheet(ship_accel, 10, 2, 16, 24);
        textures.ship.idle = getTexturesFromSpritesheet(ship_idle, 10, 2, 16, 24);

        textures.bolt = {};
        textures.bolt.idle = getTexturesFromSpritesheet(bolt, 2, 1, 7, 13)
        textures.bolt.accelerating = getTexturesFromSpritesheet(bolt, 2, 1, 7, 13)

        
        textures.spacestation1 = {};
        textures.spacestation1.idle = [PIXI.loader.resources["static/assets/spacestation1.png"].texture];
        textures.spacestation1.accelerating = [PIXI.loader.resources["static/assets/spacestation1.png"].texture];

        textures.bolfenn = {};
        textures.bolfenn.idle = [PIXI.loader.resources["static/assets/bolfenn.png"].texture];
        textures.bolfenn.accelerating = [PIXI.loader.resources["static/assets/bolfenn.png"].texture];

        textures.asteroid = {};
        textures.asteroid.idle = [PIXI.loader.resources["static/assets/asteroid.png"].texture];
        textures.asteroid.accelerating = [PIXI.loader.resources["static/assets/asteroid.png"].texture];

        textures.asteroid = {};
        textures.asteroid.idle = [PIXI.loader.resources["static/assets/asteroid.png"].texture];
        textures.asteroid.accelerating = [PIXI.loader.resources["static/assets/asteroid.png"].texture];

        textures.planet2 = {};
        textures.planet2.idle = [PIXI.loader.resources["static/assets/planet2.png"].texture];
        textures.planet2.accelerating = [PIXI.loader.resources["static/assets/planet2.png"].texture];

        textures.planet3 = {};
        textures.planet3.idle = [PIXI.loader.resources["static/assets/planet3.png"].texture];
        textures.planet3.accelerating = [PIXI.loader.resources["static/assets/planet3.png"].texture];

        textures.planet4 = {};
        textures.planet4.idle = [PIXI.loader.resources["static/assets/planet4.png"].texture];
        textures.planet4.accelerating = [PIXI.loader.resources["static/assets/planet4.png"].texture];

        textures.planet5 = {};
        textures.planet5.idle = [PIXI.loader.resources["static/assets/planet5.png"].texture];
        textures.planet5.accelerating = [PIXI.loader.resources["static/assets/planet5.png"].texture];

        textures.target = {};
        textures.target.idle = [PIXI.loader.resources["static/assets/target.png"].texture];
        textures.target.accelerating = [PIXI.loader.resources["static/assets/target.png"].texture];

        textures.iron_ore_pickup = {};
        textures.iron_ore_pickup.idle = [PIXI.loader.resources["static/assets/iron_ore_pickup.png"].texture];
        textures.iron_ore_pickup.accelerating = [PIXI.loader.resources["static/assets/iron_ore_pickup.png"].texture];

        textures.silver_ore_pickup = {};
        textures.silver_ore_pickup.idle = [PIXI.loader.resources["static/assets/silver_ore_pickup.png"].texture];
        textures.silver_ore_pickup.accelerating = [PIXI.loader.resources["static/assets/silver_ore_pickup.png"].texture];

        textures.gold_ore_pickup = {};
        textures.gold_ore_pickup.idle = [PIXI.loader.resources["static/assets/gold_ore_pickup.png"].texture];
        textures.gold_ore_pickup.accelerating = [PIXI.loader.resources["static/assets/gold_ore_pickup.png"].texture];
        textures.stars = stars;
        textures.bg = bg;

        stage.addChild(textures.bg);
        stage.addChild(textures.stars);
        stage.addChild(lasers);
        stage.addChild(entities);
    }

    function update_gamestate(state, sim_time, unprocessed_input) {
        if(state) {
            update_enemies(state, sim_time);
            state = update_player(state, unprocessed_input, sim_time);
            detect_and_resolve_collisions(state);
            handle_mining(state)

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
            brake: !keys.d.isDown,
            shoot: keys.f.isDown,
            mining: keys.space.isDown,
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

    
    

    function render_game(renderer, gamestate, stage){
        var camera = {
            x:  0,
            y:  0,
            width: 1,
            height: 1
        }
        entities.removeChildren();
        if(gamestate) {
            camera = gamestate.camera;
            let entity = gamestate.entities[gamestate.player_id];
            // if(!(gamestate.player_id in sprites)){
            sprites[gamestate.player_id] = new PIXI.Sprite(textures[entity.type].idle[0]);
            sprites[gamestate.player_id].x = stage.width/2 - sprites[gamestate.player_id].width/2;
            sprites[gamestate.player_id].y = stage.height/2 - sprites[gamestate.player_id].height/2;
            sprites[gamestate.player_id].anchor.x = 0.5;
            sprites[gamestate.player_id].anchor.y = 0.5;
            sprites[gamestate.player_id].frame = 0;

            entities.addChild(sprites[gamestate.player_id])
            // }   
            let sprite = sprites[gamestate.player_id];

            sprite.x = entity.position.x - camera.x;
            sprite.y = entity.position.y - camera.y;
            sprite.rotation = entity.rotation;
            entity.state = entity.force.x != 0 || entity.force.y != 0 ? 'accelerating' : 'idle';
            let texture = textures[entity.type][entity.state]
            sprite.texture = texture[Math.floor(sprite.frame)%texture.length];
            sprite.frame += 0.5;
        }

        if(gamestate && gamestate.mining_entities) {
            lasers.removeChildren();
            camera = gamestate.camera;
            for(var min_id in gamestate.mining_entities) {
                let miner = gamestate.mining_entities[min_id];
                let p_from_x = miner["from"].position.x - camera.x;
                let p_from_y = miner["from"].position.y - camera.y;
                let p_to_x = miner["to"].position.x - camera.x;
                let p_to_y = miner["to"].position.y - camera.y;

                let myGraph = new PIXI.Graphics();
                lasers.addChild(myGraph);

                // Move it to the beginning of the line
                //myGraph.position.set(p_from_x, p_from_y);

                // Draw the line (endPoint should be relative to myGraph's position)
                myGraph.lineStyle(4, 0xff0000)
                       .moveTo(p_from_x, p_from_y)
                       .lineTo(p_to_x, p_to_y)
                       .lineStyle(2, 0x770022)
                       .moveTo(p_from_x+4, p_from_y+4)
                       .lineTo(p_to_x+4, p_to_y+4)
                       .moveTo(p_from_x-4, p_from_y-4)
                       .lineTo(p_to_x-4, p_to_y-4);
            }

        }

        if(replay_state && replay_state.render_state){
            
            for(var e in replay_state.render_state.entities){
                if(e === replay_state.render_state.player_id) {
                    continue;
                }
                let entity = replay_state.render_state.entities[e];
                sprites[e] = new PIXI.Sprite(textures[entity.type].idle[0]);

                if (entity.radius) {
                    sprites[e].width = 2*entity.radius;
                    sprites[e].height = 2*entity.radius;
                }

                sprites[e].x = stage.width/2 - sprites[e].width/2;
                sprites[e].y = stage.height/2 - sprites[e].height/2;
                sprites[e].anchor.x = 0.5;
                sprites[e].anchor.y = 0.5;
                sprites[e].frame = 0;

                entities.addChild(sprites[e])    
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

    return game_state
});