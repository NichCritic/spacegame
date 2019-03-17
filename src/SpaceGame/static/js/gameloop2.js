var GameLoop = (function() {
    var gamestate_buffer = new circularArrayBuffer(10);
     //Create a container object called the `stage`
    var stage; stage = new PIXI.Container();
    var lasers; lasers = new PIXI.Container();
    var entities; entities = new PIXI.Container();

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

        textures.gold_ore_pickup = {};
        textures.gold_ore_pickup.idle = [PIXI.loader.resources["static/assets/gold_ore_pickup.png"].texture];
        textures.stars = stars;
        textures.bg = bg;

        stage.addChild(textures.bg);
        stage.addChild(textures.stars);
        stage.addChild(lasers);
        stage.addChild(entities);

        entity_manager = new EntityManager();
        entity_manager.init();
        var entity_components = {};
        var component_manager = ComponentManager;
        component_manager.init(entity_components, components);

        node_factory = NodeFactory(entity_manager, component_manager);

        physics_system = new LocalPhysicsSystem(node_factory);

        player_server_update_system = new PlayerServerUpdateSystem(node_factory);
        server_update_system = new ServerUpdateSystem(node_factory);

        camera_track_system = new CameraFollowSystem(node_factory, textures);
        
        animation_system = new AnimationSystem(node_factory);

        render_system = new RenderSystem(node_factory, entities);

        systems = [player_server_update_system, server_update_system, physics_system, camera_track_system, animation_system, render_system];

        camera = node_factory.create_node({
            position:{x:-100, y:-100},
            camera: {}
        });


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

    var throttledGetServerData =  locked(getServerData);
    var throttledSendServerData = locked(sendServerData);

    function getServerData(unlock_fn, args){
        let inputs = args.inputs;
        let gamestate_buffer = args.gamestate_buffer;
        $.postJSON('./a/message/updates', {}, function success(result){
            let serverState = result.messages[0];

            inputs.update(serverState.time);
            let entities = Object.keys(serverState.entities);
            for(let i = 0; i < entities.length; i++) {
                let entity = serverState.entities[entities[i]];

                let n = node_factory.create_node([], entity.id);

                n.add_or_update("server_update", {data: {'acceleration': entity.acceleration,
                'force': entity.force,
                'mass': {mass:entity.mass},
                'position': entity.position,
                'rotation': {rotation: entity.rotation},
                'velocity': entity.velocity,
                'thrust': {thrust:0.05}}});




                n.add_or_update("area", {"radius":entity.radius});
                n.add_or_update("renderable", {spritesheet: textures[entity.type],
                                               image:textures[entity.type].idle[0],
                                               width: n.area.radius*2,
                                               height: n.area.radius*2});

                if(entities[i] === serverState.player_id){
                    n.add_or_update('player');
                    n.add_or_update('inputs', {inputs:inputs});
                    //TODO: We know that the player can be animated but this should really be based on server data
                    n.add_or_update('animated', {update_rate: 0.5});
                    

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

            for(let i = 0; i < last_seen_entities.length; i++) {
                if(entities.indexOf(last_seen_entities[i]) === -1) {
                    let n = node_factory.create_node([], last_seen_entities[i]);
                    n.add_or_update("to_be_removed");
                }
            } 

            last_seen_entities = entities;

            //Hack, accessing global
            replay_state.time = serverState.time 
            unlock_fn();
        }, function error(result){
            unlock_fn();
            window.location.replace("/auth/login");
        });
        
    }

    function sendServerData(unlock_fn, args){
        let inputs = args.inputs.list;
        let to_send = []
        for(let i = 0; i < inputs.length; i++){
            let inp = inputs[i];
            if(!inp.was_sent){
                to_send.push(inp)
                inp.was_sent = true
            }
        }
        $.postJSON('./a/message/new', {'inputs':to_send}, function(result){
            unlock_fn();

        }, function error(result){
            unlock_fn();
        });    
    }

    function update_server() {
        throttledGetServerData(
            {
                gamestate_buffer:gamestate_buffer,
                inputs:inputs
            }
        );
        throttledSendServerData({
            inputs:inputs
        });
    }

    
    

    function render_game(renderer, gamestate, stage){
        renderer.render(stage);
    }

    

    return game_state
});