var invMenu = (function() {

    var menu_state = {
        items: [
            // {id: "0001", pos:0, text:"Rockets", cost:10000, img:""},
            // {id: "0002", pos:1, text:"Shields", cost:1000, img:""},
            // {id: "0003", pos:2, text:"Engines", cost:20000, img:""}


        ],
        selector_index:0
    };

    var renderables = {};

    var menu_text_style = {
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
    }

    function render_static_elems(menu){
        var bg = new PIXI.Graphics();
            bg.beginFill(0xD2E7D2);
            bg.drawRect(0, 0, 700, 500);
            bg.endFill();
            bg.x = 50;
            bg.y = 50;

        var selector = new PIXI.Graphics();
            selector.lineStyle(4, 0x33AAAA, 1);
            selector.drawRect(0, 0, 694, 50);
            selector.x = 53;
            selector.y = 53;
            selector.zOrder=-1;

        var elems = {};
        elems.bg = bg;
        elems.selector = selector;

        menu.addChild(elems.bg);
        menu.addChild(elems.selector);

        return elems;
    }

    function render_item(menu, item) {
        var bg = new PIXI.Graphics();
        var renderable = {};
        bg.beginFill(0xB2C7B2);
        bg.drawRect(0, 0, 700-10, 50);
        bg.endFill();
        bg.x = 50+5;
        bg.y = 50*item.pos+50+5+(item.pos > 0 ? 5:0);
        menu.addChild(bg);

        let style = new PIXI.TextStyle(menu_text_style);

        let item_text = new PIXI.Text(item.name, style);
        item_text.position.set(50+5, 50*item.pos+50+5+(item.pos > 0 ? 5:0));

        let qty_text = new PIXI.Text(""+item.qty, style);
        qty_text.position.set(700-100, 50*item.pos+50+5+(item.pos > 0 ? 5:0));

        menu.addChild(item_text);
        menu.addChild(qty_text);

        renderable.item_text = item_text;
        renderable.qty_text = qty_text;
        renderable.bg = bg;
        renderable.item = item;

        renderables[item.id] = renderable;

        menu.updateLayersOrder();

    }

    var menu_keys = (function(){
        var keys = {};
        var menu_state;

        keys.up = keyboard(38);

        keys.up.press = function(){
            if(menu_state.selector_index > 0) {
                menu_state.selector_index--;
            }
        };

        keys.down = keyboard(40);
        keys.down.press = function(){
            if(menu_state.selector_index < menu_state.items.length-1) {
                menu_state.selector_index++;
            }
        };

        return {
            keys:keys,
            set_menu_state:function(state){
                menu_state = state
            }
        }
    })();

    function get_server_data(unlock_fn) {
        $.getJSON("/inv", function success(data){
            menu_state.items = data.inventory;
            unlock_fn();
        }, function failure(err){
            console.warn(err);
            menu_state = {items:[]}
            unlock_fn();
        });
        return menu_state;
    }

    throttled_get_server_data = locked(get_server_data);

    return {
        menu_text_style:menu_text_style,
        render_static_elems:render_static_elems,
        render_item:render_item,
        menu_keys:menu_keys,
        get_server_data:throttled_get_server_data,
        menu_state:menu_state,
        renderables:renderables
    }

})();

var shopMenu = (function() {

    var menu_state = {
        items: [
            // {id: "0001", pos:0, text:"Rockets", cost:10000, img:""},
            // {id: "0002", pos:1, text:"Shields", cost:1000, img:""},
            // {id: "0003", pos:2, text:"Engines", cost:20000, img:""}


        ],
        selector_index:0
    };

    var renderables = {};

    var menu_text_style = {
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
    }

    function render_static_elems(menu){
        var bg = new PIXI.Graphics();
            bg.beginFill(0xD2E7D2);
            bg.drawRect(0, 0, 700, 500);
            bg.endFill();
            bg.x = 50;
            bg.y = 50;

        var selector = new PIXI.Graphics();
            selector.lineStyle(4, 0x33AAAA, 1);
            selector.drawRect(0, 0, 694, 50);
            selector.x = 53;
            selector.y = 53;
            selector.zOrder=-1;

        var elems = {};
        elems.bg = bg;
        elems.selector = selector;

        menu.addChild(elems.bg);
        menu.addChild(elems.selector);

        return elems;
    }

    function render_item(menu, item) {
        var bg = new PIXI.Graphics();
        var renderable = {};
        bg.beginFill(0xB2C7B2);
        bg.drawRect(0, 0, 700-10, 50);
        bg.endFill();
        bg.x = 50+5;
        bg.y = 50*item.pos+50+5+(item.pos > 0 ? 5:0);
        menu.addChild(bg);

        let style = new PIXI.TextStyle(menu_text_style);

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

    var menu_keys = (function(){
        var keys = {};
        var menu_state;

        keys.up = keyboard(38);

        keys.up.press = function(){
            if(menu_state.selector_index > 0) {
                menu_state.selector_index--;
            }
        };

        keys.down = keyboard(40);
        keys.down.press = function(){
            if(menu_state.selector_index < menu_state.items.length-1) {
                menu_state.selector_index++;
            }
        };

        keys.enter = keyboard(13);

        keys.enter.press = function() {
            $.postJSON("/shop", {msg: "purchase", "item_index":menu_state.selector_index}, 
            function(){
                
            },
            function(err){
                console.warn(err);
            })
        };


        return {
            keys:keys,
            set_menu_state:function(state){
                menu_state = state
            }
        }
    })();

    function get_server_data(unlock_fn) {
        $.getJSON("/shop", function success(data){
            menu_state.items = data.items;
            unlock_fn();
        }, function failure(err){
            console.warn(err);
            menu_state = {items:[]}
            unlock_fn();
        });
        return menu_state;
    }

    throttled_get_server_data = locked(get_server_data);

    return {
        menu_text_style:menu_text_style,
        render_static_elems:render_static_elems,
        render_item:render_item,
        menu_keys:menu_keys,
        get_server_data:throttled_get_server_data,
        menu_state:menu_state,
        renderables:renderables
    }

})();


var MenuState = (function(menuData) {
    var menu; menu = new PIXI.Container();

    var keys = {};

    var sprites = {};

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

    var render_item = menuData.render_item.bind(null, menu);


    function setup_menu() {
        var s_elems = menuData.render_static_elems(menu);

        sprites.selector = s_elems.selector;

        menu_keys = menuData.menu_keys
        menu_keys.set_menu_state(menuData.menu_state);
        keys = menu_keys.keys;
        
    }

    function update(state) {
        sprites.selector.y = 53 + menuData.menu_state.selector_index * 55;

        return state;
    }

    function get_state() {
        var menu_state = menuData.get_server_data();
        return menu_state;
    }

    function render_menu(renderer, state, menu) {
        renderer.render(menu);
        new_renderables = {}

        for(let i in menuData.renderables) {
            let r = menuData.renderables[i];
            if(!(i in state.items)) {
                for(let elem in r) {
                    menu.removeChild(r[elem]);
                }
            } else {
                new_renderables[i] = r;
            }
        }

        menuData.renderables = new_renderables;

        let cnt = 0;
        for(let i in state.items) {
            let item = state.items[i];
            if(!(item.id in menuData.renderables)) {
                if(!item.pos) {
                    item.pos = cnt;
                }
                render_item(item);
            }
            cnt++;
        }
    }

    return menu_mode;
});