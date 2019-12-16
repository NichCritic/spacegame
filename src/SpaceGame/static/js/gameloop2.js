var GameLoop = (function() {
    var gamestate_buffer = new circularArrayBuffer(10);
     //Create a container object called the `stage`
    var stage; stage = new PIXI.Container();
    var lasers; lasers = new PIXI.Container();
    var entities; entities = new PIXI.Container();
    var health_bars; health_bars = new PIXI.Container();
    var mining_lasers; mining_lasers = new PIXI.Container();

    var textures, sprites;

    var entity_manager;
    var entity_components;
    var component_manager;
    var node_factory;
    var physics_system;
    var render_system;
    var player_server_update_system;
    var server_update_system;
    var animation_system;

    var camera_track_system;
    var systems;
    var camera;
    var ship;

    var last_seen_entities = [];

    sprites = [];

    var ws;
    
    var dialog_menu;

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

    function setup(dialog) {
        dialog_menu = dialog

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

        
        textures.spacestation1 = {};
        textures.spacestation1.idle = [PIXI.loader.resources["static/assets/spacestation1.png"].texture];

        textures.bolfenn = {};
        textures.bolfenn.idle = [PIXI.loader.resources["static/assets/bolfenn.png"].texture];

        textures.asteroid = {};
        textures.asteroid.idle = [PIXI.loader.resources["static/assets/asteroid.png"].texture];

        textures.asteroid = {};
        textures.asteroid.idle = [PIXI.loader.resources["static/assets/asteroid.png"].texture];

        textures.planet2 = {};
        textures.planet2.idle = [PIXI.loader.resources["static/assets/planet2.png"].texture];

        textures.planet3 = {};
        textures.planet3.idle = [PIXI.loader.resources["static/assets/planet3.png"].texture];

        textures.planet4 = {};
        textures.planet4.idle = [PIXI.loader.resources["static/assets/planet4.png"].texture];

        textures.planet5 = {};
        textures.planet5.idle = [PIXI.loader.resources["static/assets/planet5.png"].texture];

        textures.target = {};
        textures.target.idle = [PIXI.loader.resources["static/assets/target.png"].texture];

        textures.iron_ore_pickup = {};
        textures.iron_ore_pickup.idle = [PIXI.loader.resources["static/assets/iron_ore_pickup.png"].texture];

        textures.silver_ore_pickup = {};
        textures.silver_ore_pickup.idle = [PIXI.loader.resources["static/assets/silver_ore_pickup.png"].texture];

        let explosion_idle = PIXI.BaseTexture.fromImage("static/assets/explosion.png")
        textures.explosion = {}
        textures.explosion.idle = getTexturesFromSpritesheet(explosion_idle, 5, 1, 16, 16);

        textures.gold_ore_pickup = {};
        textures.gold_ore_pickup.idle = [PIXI.loader.resources["static/assets/gold_ore_pickup.png"].texture];
        textures.stars = stars;
        textures.bg = bg;

        stage.addChild(textures.bg);
        stage.addChild(textures.stars);
        stage.addChild(lasers);
        stage.addChild(entities);
        stage.addChild(health_bars);
        stage.addChild(mining_lasers);

        entity_manager = new EntityManager();
        entity_manager.init();
        var entity_components = {};
        var component_manager = ComponentManager;
        component_manager.init(entity_components, components);

        node_factory = NodeFactory(entity_manager, component_manager);
        input_system = new InputSystem(node_factory);
        physics_system = new LocalPhysicsSystem(node_factory);

        player_server_update_system = new PlayerServerUpdateSystem(node_factory);
        PCE_update_system = new PCEUpdateSystem(node_factory);
        server_update_system = new ServerUpdateSystem(node_factory);
        shooting_system = new ShootingSystem(node_factory, textures, weapons);
        mining_system = new MiningSystem(node_factory, textures);

        camera_track_system = new CameraFollowSystem(node_factory, textures);
        
        animation_system = new AnimationSystem(node_factory);

        health_render_system = new HealthRenderSystem(node_factory, health_bars);
        mining_laser_render = new MiningLaserRenderSystem(node_factory, mining_lasers);
        render_system = new RenderSystem(node_factory, entities);

        expiry_system = new ExpirySystem(node_factory);

        server_sync_system = new ServerSyncSystem(node_factory);
        collision_system = new CollisionSystem(node_factory);
        collision_move_system = new CollisionMovementSystem(node_factory);

        systems = [/*server_sync_system,*/ player_server_update_system, PCE_update_system, server_update_system, expiry_system, input_system, shooting_system, mining_system, physics_system, collision_system, collision_move_system, camera_track_system, animation_system, /*mining_laser_render,*/ health_render_system, render_system];

        camera = node_factory.create_node({
            position:{x:-100, y:-100},
            camera: {}
        });

        ws = new WebSocket("ws://naelick.com:8888/a/message/updates")
        ws.onmessage = function(evt){
            update_from_server(
                {
                gamestate_buffer:gamestate_buffer,
                inputs:inputs
            }, JSON.parse(evt.data));
        }

        ws.onclose = function(evt){    
            // window.location.replace("/auth/login");
            debugger;
        }
        ws.onerror = function(evt){    
            // window.location.replace("/auth/login");
            debugger;
        }

    }

    function update_gamestate(state, dt, unprocessed_input) {
        let player = node_factory.create_node_list(["player"])[0];
        if(player) {
            player.add_or_attach("control", unprocessed_input[unprocessed_input.length-1]);
        }
        for(let i = 0; i < systems.length; i++) {
            systems[i].process();
        }
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

    // var throttledGetServerData =  locked(getServerData);
    var throttledSendServerData = locked(sendServerData);

    function update_from_server(args, result) {
        let serverState = result.messages[result.messages.length-1];

        inputs.update(serverState.time);
        let entities = Object.keys(serverState.entities);
        for(let i = 0; i < entities.length; i++) {
            let entity = serverState.entities[entities[i]];

            // if(entity.type && entity.type=== 'bolt') {
            //     //Temporarily don't sync bullets
            //     continue    
            // } 

            let n = node_factory.create_node([], entity.id);

            n.add_or_update("server_update", {data: {
                'acceleration': {x:0, y:0},
                'force': {x:0, y:0},
                'mass': {mass:entity.mass},
                'position': entity.position,
                'rotation': {rotation: entity.rotation},
                'velocity': {x:0, y:0},
                'thrust': {thrust:0.00},
                'time': serverState.time
            }});




            n.add_or_update("area", {"radius":entity.radius});
            n.add_or_update("renderable", {spritesheet: textures[entity.type],
                                           image:textures[entity.type].idle[0],
                                           width: n.area.radius*2,
                                           height: n.area.radius*2});



            n.add_or_update("type", {"type":entity.type})

            if(entity.animated) {
                //TODO This could cause a bug where the animation rate isn't updated between
                //two entity states
                n.add_or_attach('animated', {update_rate: entity.animated.update_rate});
            }


            if(entity.health) {
                n.add_or_update('health', entity.health);
            }

            if(entity.collidable) {
                n.add_or_update('collidable', {});
            }
            if(entity.minable) {
                n.add_or_update('minable', {});
            }
            if(entity.mining) {
                n.add_or_update('mining', {});
            }
            else{
                n.delete_component('mining')
            }
            
            if(entity.expires) {
                n.add_or_update('expires', entity.expires);
            }
            if(entity.pickup) {
                n.add_or_update('pickup', {});
            }

            if(entity.client_sync) {
                n.add_or_update('client_sync', entity.client_sync)
            }

            if(entities[i] === serverState.player_id){
                n.add_or_update('player');
                n.add_or_update('inputs', {inputs:inputs});

                if(entity.weapon) {
                    n.add_or_update('weapon', entity.weapon)
                }
                //TODO: We know that the player can be animated but this should really be based on server data
                
                n.add_or_update("server_update", {data: {
                    'acceleration': entity.acceleration,
                    'force': entity.force,
                    'mass': {mass:entity.mass},
                    'position': entity.position,
                    'rotation': {rotation: entity.rotation},
                    'velocity': entity.velocity,
                    'thrust': {thrust:0.015},
                    'time': serverState.time
                }}); 
                
                if(entity.quest_status_updated) {
                    //TODO: Hook this into some event system to show actual quest info
                    let quest = entity.quest_status_updated.quest;
                    let stage = entity.quest_status_updated.stage;
                    if(quest === 'intro') {
                        if(stage === 2) {
                            dialog_menu.open(quests.intro.script.stage2)
                        } else if (stage === 3) {
                            dialog_menu.open(quests.intro.script.stage3)
                        } else if (stage === 4) {
                            dialog_menu.open(quests.intro.script.stage4)
                        }

                    } else {
                        dialog_menu.open([quest, stage])
                    }
                }

            } else {
                n.add_or_update('server_controlled');
            }
            // acceleration: {x: 0, y: 0}
            // control: [null]
            // force: {x: 0, y: 0}
            // id: "48294adf-4768-46a5-b546-cbd1d59e344f"
            // last_update: 1552269914160.3145
            // mass: 200
            // minable: true
            // mining: false
            // position: {x: 1500, y: 0}
            // radius: 100
            // rotation: 10
            // state_history: (10) [{…}, {…}, {…}, {…}, {…}, {…}, {…}, {…}, {…}, {…}]
            // type: "asteroid"
            // velocity: {x: 0, y: 0}


        }

        // for(let i = 0; i < last_seen_entities.length; i++) {
        //     if(entities.indexOf(last_seen_entities[i]) === -1) {
        //         let n = node_factory.create_node([], last_seen_entities[i]);
        //         n.add_or_update("to_be_removed");
        //     }
        // } 

        // last_seen_entities = entities;

        //Hack, accessing global
        replay_state.time = serverState.time
    }

    function getServerData(unlock_fn, args){
        let inputs = args.inputs;
        let gamestate_buffer = args.gamestate_buffer;
        $.postJSON('./a/message/updates', {}, function success(result){
             
            unlock_fn();
        }, function error(result){
            unlock_fn();
            window.location.replace("/auth/login");
        });
        
    }

    function sendServerData(args){
        let inputs = args.inputs.list;
        let to_send = []
        for(let i = 0; i < inputs.length; i++){
            let inp = inputs[i];
            if(!inp.was_sent){
                to_send.push(inp)
                inp.was_sent = true
            }
        }
        if(ws.readyState === 1) {
            ws.send(JSON.stringify({'inputs':to_send,
                                    'tracked_ids':args.tracked_ids}));
        }
    }

    function update_server() {
        // throttledGetServerData(
        //     {
        //         gamestate_buffer:gamestate_buffer,
        //         inputs:inputs
        //     }
        // );
        let tracking_nodes = node_factory.create_node_list(["renderable", "server_controlled"])
        let ids = []
        for(var i = 0; i < tracking_nodes.length; i++) {
            let n = tracking_nodes[i];
            ids.push(n.id);
        }


        sendServerData({
            inputs:inputs,
            tracked_ids: ids
        });
    }

    
    

    function render_game(renderer, gamestate, stage){
        renderer.render(stage);
    }

    

    return game_state
});