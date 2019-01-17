var MenuState = (function() {
    var menu; menu = new PIXI.Container();

    var keys = {};

    var menu_state = {
        items: [
            // {id: "0001", pos:0, text:"Rockets", cost:10000, img:""},
            // {id: "0002", pos:1, text:"Shields", cost:1000, img:""},
            // {id: "0003", pos:2, text:"Engines", cost:20000, img:""}


        ]
    };

    var sprites = {};

    var renderables = {};

    var selector_index = 0;

    menu.updateLayersOrder = function () {
        menu.children.sort(function(a,b) {
            a.zOrder = a.zOrder || 0;
            b.zOrder = b.zOrder || 0;
            return b.zOrder - a.zOrder
        });
    };

    var menu_mode = {
        init: setup_menu,
        stage:menu,
        get_input: function(){},
        get_state: get_state,
        update: update,
        render: render_menu,
        update_server:function(){}
    }


    function setup_menu() {
        var bg = new PIXI.Graphics();
        bg.beginFill(0xD2E7D2);
        bg.drawRect(0, 0, 700, 500);
        bg.endFill();
        bg.x = 50;
        bg.y = 50;
        menu.addChild(bg);

        var selector = new PIXI.Graphics();
        selector.lineStyle(4, 0x33AAAA, 1);
        selector.drawRect(0, 0, 694, 50);
        selector.x = 53;
        selector.y = 53;
        selector.zOrder=-1;

        sprites.selector = selector;

        menu.addChild(selector);

        keys.up = keyboard(38);

        keys.up.press = function(){
            if(selector_index > 0) {
                selector_index--;
            }
        };

        keys.down = keyboard(40);
        keys.down.press = function(){
            if(selector_index < menu_state.items.length-1) {
                selector_index++;
            }
        };



    }

    function update(state) {
        sprites.selector.y = 53 + selector_index * 55;

        return state;
    }

    jQuery.getJSON = function(url, callback, error) {
        // args._xsrf = getCookie("_xsrf");
        $.ajax({url: url, dataType: "json", type: "GET",
            success: callback, error: error});
    };

    function get_server_data(unlock_fn) {
        $.getJSON("/shop", function success(data){
            menu_state = data;
            unlock_fn();
        }, function failure(err){
            console.warn(err);
            menu_state = {items:[]}
            unlock_fn();
        });

    }

    throttled_get_server_data = locked(get_server_data);

    function get_state() {
        throttled_get_server_data();
        return menu_state;
    }

    function render_item(item) {
        var bg = new PIXI.Graphics();
        var renderable = {};
        bg.beginFill(0xB2C7B2);
        bg.drawRect(0, 0, 700-10, 50);
        bg.endFill();
        bg.x = 50+5;
        bg.y = 50*item.pos+50+5+(item.pos > 0 ? 5:0);
        menu.addChild(bg);

        let style = new PIXI.TextStyle({
          fontFamily: "Arial",
          fontSize: 36,
          fill: "white",
          stroke: '#000000',
          strokeThickness: 4,
          dropShadow: true,
          dropShadowColor: "#000000",
          dropShadowBlur: 4,
          dropShadowAngle: Math.PI / 6,
          dropShadowDistance: 6,
        });

        let item_text = new PIXI.Text(item.text, style);
        item_text.position.set(50+5, 50*item.pos+50+5+(item.pos > 0 ? 5:0));

        let price_text = new PIXI.Text(""+item.cost, style);
        price_text.position.set(700-100, 50*item.pos+50+5+(item.pos > 0 ? 5:0));

        menu.addChild(item_text);
        menu.addChild(price_text);

        renderable.item_text = item_text;
        renderable.price_text = price_text;
        renderable.bg = bg;
        renderable.item = item;

        renderables[item.id] = renderable;

        menu.updateLayersOrder();

    }

    function render_menu(renderer, state, menu) {
        renderer.render(menu);
        new_renderables = {}

        for(let i in renderables) {
            let r = renderables[i];
            if(!(i in state.items)) {
                menu.removeChild(r.item_text);
                menu.removeChild(r.price_text);
                menu.removeChild(r.bg);
            } else {
                new_renderables[i] = r;
            }
        }

        renderables = new_renderables;

        for(let i in state.items) {
            let item = state.items[i];
            if(!(item.id in renderables)) {
                render_item(item);
            }
        }
    }

    return menu_mode;
});