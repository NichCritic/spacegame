
var MapState = (function(mapData) {
    var map; map = new PIXI.Container();

    var sprites = {};

    var map_data = {};

    var map_mode = {
        init: setup_map,
        stage:map,
        get_input: function(){},
        get_state: function(){},
        update: function(){},
        render: render_map,
        update_server:function(){},
        poll:get_data
    }

    function get_data() {
        $.getJSON("/minimap", function success(data){
            map_data = data;
            map.removeChildren();
            var p = new PIXI.Graphics();
            p.beginFill(0x00FF00);
            p.drawRect(0, 0, 5, 5);
            p.endFill();

            //Center is 600, 300
            let x = map_data.player.x;
            let y = map_data.player.y;
            p.x = 600+ (x / 7500)*250;
            p.y = 300+ (y / 7500)*250;
            map.addChild(p);
            
            for(var i in map_data.positions) {
                let x = map_data.positions[i].x
                let y = map_data.positions[i].y
                var item = new PIXI.Graphics();
                item.beginFill(0xFF0000);
                item.drawRect(0, 0, 5, 5);
                item.endFill();

                //Center is 600, 300
                item.x = 600+ (x / 7500)*250;
                item.y = 300+ (y / 7500)*250;
                map.addChild(item);
            }

        }, function failure(err){
            console.warn(err);
        });
    }


    function setup_map() {
        get_data();
    }

    

    function render_map(renderer, state, mapp) {
        renderer.render(map);
    }

    return map_mode;
});