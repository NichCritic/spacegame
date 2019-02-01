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
    var elems = {};

    var money_text;

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

        
        elems.bg = bg;
        elems.selector = selector;

        let style = new PIXI.TextStyle(menu_text_style);

        elems.money = new PIXI.Text(menu_state.money, style);
        elems.money.position.set(600, 490);

        menu.addChild(elems.bg);
        menu.addChild(elems.selector);
        menu.addChild(elems.money);

        money_text = elems.money;

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

    function get_all_server_data(){
        throttled_get_inventory_data()
        throttled_get_money_data()

        return menu_state
    }

    function get_inventory_data(unlock_fn) {
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

    function get_money_data(unlock_fn) {
        $.getJSON("/money", function success(data){
            menu_state.money = data.money;
            money_text.text = data.money;
            unlock_fn();
        }, function failure(err){
            console.warn(err);
            menu_state = {items:[]}
            unlock_fn();
        });
        return menu_state;
    }

    function renderItems(menu){
        let cnt = 0;
        for(let i in menu_state.items) {
            let item = menu_state.items[i];
            if(!(item.id in renderables)) {
                if(!item.pos) {
                    item.pos = cnt;
                }
                render_item(menu, item);
            }
            cnt++;
        }
    }

    function update_selector(){
        elems.selector.y = 53 + menu_state.selector_index * 55;
    }

    let throttled_get_inventory_data = locked(get_inventory_data);
    let throttled_get_money_data = locked(get_money_data);

    return {
        menu_text_style:menu_text_style,
        render_static_elems:render_static_elems,
        render_item:render_item,
        menu_keys:menu_keys,
        get_server_data:get_all_server_data,
        menu_state:menu_state,
        renderItems:renderItems,
        renderables:renderables,
        update_selector:update_selector
    }

})();

var shopMenu = (function() {

    var menu_state = {
        items: [
            // {id: "0001", pos:0, text:"Rockets", cost:10000, img:""},
            // {id: "0002", pos:1, text:"Shields", cost:1000, img:""},
            // {id: "0003", pos:2, text:"Engines", cost:20000, img:""}


        ],
        sell_items:[

        ],
        selector_index:0,
        selector_menu:'buy'
    };

    var renderables = {};
    var s_renderables = {};
    var elems = {};
    var money_text;

    var menu_style = {
        x:50, y:50, width:350, height:500,
        selector_width: 346, selector_height:50, selector_margin_left:3, selector_margin_top:3,
        item_top_margin:5, item_bottom_margin:5, item_right_margin:5, item_left_margin:5, item_height:50,
        money_bottom_margin:20
    }

    var sell_menu_style = {
        x:menu_style.x+menu_style.width+10, y:50, width:350, height:500,
        selector_width: 346, selector_height:50, selector_margin_left:3, selector_margin_top:3,
        money_right_margin:100, money_bottom_margin:10,
        item_top_margin:5, item_bottom_margin:5, item_right_margin:5, item_left_margin:5, item_height:50,
        money_bottom_margin:20
    }


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
            bg.drawRect(0, 0, menu_style.width, menu_style.height);
            bg.endFill();
            bg.x = menu_style.x;
            bg.y = menu_style.y;

        var sell_bg = new PIXI.Graphics();
            sell_bg.beginFill(0xD2E7D2);
            sell_bg.drawRect(0, 0, sell_menu_style.width, sell_menu_style.height);
            sell_bg.endFill();
            sell_bg.x = sell_menu_style.x;
            sell_bg.y = sell_menu_style.y;

        var selector = new PIXI.Graphics();
            selector.lineStyle(4, 0x33AAAA, 1);
            selector.drawRect(0, 0, menu_style.selector_width, menu_style.selector_height);
            selector.x = menu_style.x + menu_style.selector_margin_left;
            selector.y = menu_style.y + menu_style.selector_margin_top;
            selector.zOrder=-1;

        
        elems.bg = bg;
        elems.sell_bg = sell_bg;
        elems.selector = selector;

        let style = new PIXI.TextStyle(menu_text_style);

        elems.money = new PIXI.Text(menu_state.money, style);
        elems.money.position.set(sell_menu_style.x + sell_menu_style.width - sell_menu_style.money_right_margin, sell_menu_style.height - sell_menu_style.money_bottom_margin);

        menu.addChild(elems.bg);
        menu.addChild(elems.sell_bg);
        menu.addChild(elems.selector);
        menu.addChild(elems.money);

        money_text = elems.money

        return elems;
    }

    function render_item(menu, item) {
        var bg = new PIXI.Graphics();
        var renderable = {};
        bg.beginFill(0xB2C7B2);
        bg.drawRect(0, 0, menu_style.width - menu_style.item_left_margin - menu_style.item_left_margin, menu_style.item_height);
        bg.endFill();

        let x_pos = menu_style.x+menu_style.item_left_margin; 
        let y_pos = menu_style.item_height*item.pos+menu_style.y+menu_style.item_bottom_margin+(item.pos > 0 ? menu_style.item_top_margin:0);

        bg.x = x_pos
        bg.y = y_pos
        menu.addChild(bg);

        let style = new PIXI.TextStyle(menu_text_style);

        let item_text = new PIXI.Text(item.text, style);
        item_text.position.set(x_pos, y_pos);

        let price_text = new PIXI.Text(""+item.cost, style);
        price_text.position.set(menu_style.width-100, y_pos);

        menu.addChild(item_text);
        menu.addChild(price_text);

        renderable.item_text = item_text;
        renderable.price_text = price_text;
        renderable.bg = bg;
        renderable.item = item;

        renderables[item.id] = renderable;

        menu.updateLayersOrder();
    }

    function render_sell_item(menu, item) {
        var bg = new PIXI.Graphics();
        var renderable = {};
        bg.beginFill(0xB2C7B2);
        bg.drawRect(0, 0, sell_menu_style.width - sell_menu_style.item_left_margin - sell_menu_style.item_left_margin, sell_menu_style.item_height);
        bg.endFill();

        let x_pos = sell_menu_style.x+sell_menu_style.item_left_margin; 
        let y_pos = sell_menu_style.item_height*item.pos+sell_menu_style.y+menu_style.item_bottom_margin+(item.pos > 0 ? sell_menu_style.item_top_margin:0);

        bg.x = x_pos
        bg.y = y_pos
        menu.addChild(bg);

        let style = new PIXI.TextStyle(menu_text_style);

        let item_text = new PIXI.Text(item.name, style);
        item_text.position.set(x_pos, y_pos);

        let qty_text = new PIXI.Text(""+item.qty, style);
        qty_text.position.set(sell_menu_style.x+sell_menu_style.width-100, y_pos);

        menu.addChild(item_text);
        menu.addChild(qty_text);

        renderable.item_text = item_text;
        renderable.qty_text = qty_text;
        renderable.bg = bg;
        renderable.item = item;

        s_renderables[item.id] = renderable;

        menu.updateLayersOrder();
    }

    function update_sell_item(r_item, item) {
        r_item.qty_text.text = item.qty;
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

        keys.left = keyboard(37);
        keys.left.press = function(){
            if(menu_state.selector_menu == 'sell') {
                menu_state.selector_menu = 'buy'
                menu_state.selector_index = Math.min(menu_state.items.length-1, menu_state.selector_index);
            }
        };

        keys.right = keyboard(39);
        keys.right.press = function(){
            if(menu_state.selector_menu == 'buy') {
                menu_state.selector_menu = 'sell'
                menu_state.selector_index = Math.min(menu_state.sell_items.length-1, menu_state.selector_index);
            }
        };

        keys.enter = keyboard(13);

        keys.enter.press = function() {
            if(menu_state.selector_menu === 'buy') {
                $.postJSON("/shop", {msg: "purchase", "item_index":menu_state.selector_index}, 
                function(){
                    
                },
                function(err){
                    console.warn(err);
                })
            } else if (menu_state.selector_menu === 'sell') {
                $.postJSON("/shop", {msg: "sell", "item_index":menu_state.selector_index}, 
                function(){
                    
                },
                function(err){
                    console.warn(err);
                })
            }
        };


        return {
            keys:keys,
            set_menu_state:function(state){
                menu_state = state
            }
        }
    })();

    function get_all_data() {
        throttled_get_money_data();
        throttled_get_shop_data();
        throttled_get_inv_data();
        return menu_state
    }

    function get_inv_data(unlock_fn) {
        $.getJSON("/inv", function success(data){
            menu_state.sell_items = data.inventory;
            unlock_fn();
        }, function failure(err){
            console.warn(err);
            unlock_fn();
        });
        return menu_state;
    }

    function get_shop_data(unlock_fn) {
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

    function get_money_data(unlock_fn) {
        $.getJSON("/money", function success(data){
            menu_state.money = data.money;
            money_text.text = data.money;
            unlock_fn();
        }, function failure(err){
            console.warn(err);
            menu_state = {items:[]}
            unlock_fn();
        });
        return menu_state;
    }

    function renderItems(menu){
        let cnt = 0;
        for(let i in menu_state.items) {
            let item = menu_state.items[i];
            if(!(item.id in renderables)) {
                if(!item.pos) {
                    item.pos = cnt;
                }
                render_item(menu, item);
            }
            cnt++;
        }

        cnt = 0;
        for(let i in menu_state.sell_items) {
            let item = menu_state.sell_items[i];
            if(!(item.id in s_renderables)) {
                if(!item.pos) {
                    item.pos = cnt;
                }
                render_sell_item(menu, item);
            }
            else{
                update_sell_item(s_renderables[item.id], item);
            }
            cnt++;
        }
    }

    function update_selector() {
        elems.selector.x = menu_state.selector_menu === 'buy' ? menu_style.x + menu_style.selector_margin_left : sell_menu_style.x + sell_menu_style.selector_margin_left; 
        elems.selector.y = 53 + menu_state.selector_index * 55;
    }

    let throttled_get_money_data = locked(get_money_data);
    let throttled_get_shop_data = locked(get_shop_data);
    let throttled_get_inv_data = locked(get_inv_data);

    return {
        menu_text_style:menu_text_style,
        render_static_elems:render_static_elems,
        render_item:render_item,
        menu_keys:menu_keys,
        get_server_data:get_all_data,
        menu_state:menu_state,
        renderables:renderables,
        renderItems:renderItems,
        update_selector:update_selector
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
        menuData.update_selector();
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

        menuData.renderItems(menu);
    }

    return menu_mode;
});