var shopMenu = (function() {

    var menu_state = {
        items: [
            // {id: "0001", pos:0, text:"Rockets", cost:10000, img:""},
            // {id: "0002", pos:1, text:"Shields", cost:1000, img:""},
            // {id: "0003", pos:2, text:"Engines", cost:20000, img:""}


        ],
        sell_items:[

        ],
        shop_inv:{},
        selector_index:0,
        selector_menu:'buy'
    };

    var renderables = {};
    var s_renderables = {};
    var elems = {};
    var money_text;

    var menu_style = {
        title_x:50, title_y:15,
        buy_text_x:50, buy_text_y:50,
        x:50, y:150, width:350, height:500,
        selector_width: 346, selector_height:50, selector_margin_left:3, selector_margin_top:3,
        item_top_margin:5, item_bottom_margin:5, item_right_margin:5, item_left_margin:5, item_height:50,
        money_bottom_margin:20
    }

    var sell_menu_style = {
        sell_text_x:menu_style.x+menu_style.width+10, sell_text_y:50,
        x:menu_style.x+menu_style.width+10, y:menu_style.y, width:500, height:500,
        money_right_margin:100, money_bottom_margin:10,
        item_top_margin:5, item_bottom_margin:5, item_right_margin:5, item_left_margin:5, item_height:50,
        money_bottom_margin:20
    }


    var menu_text_title_style = {
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

    var menu_text_style = {
        fontFamily: "Arial",
        fontSize: 22,
        fill: "white",
        stroke: '#000000',
        strokeThickness: 2,
        dropShadow: true,
        dropShadowColor: "#000000",
        dropShadowBlur: 2,
        dropShadowAngle: Math.PI / 6,
        dropShadowDistance: 3,
    }

    function render_static_elems(menu){

        let title_style = new PIXI.TextStyle(menu_text_title_style);

        elems.title = new PIXI.Text("Shop", title_style);
        elems.title.position.set(menu_style.title_x, menu_style.title_y);

        elems.buy_text = new PIXI.Text("Buy from shop", title_style);
        elems.buy_text.position.set(menu_style.buy_text_x, menu_style.buy_text_y);

        elems.sell_text = new PIXI.Text("Sell from Inventory", title_style);
        elems.sell_text.position.set(sell_menu_style.sell_text_x, sell_menu_style.sell_text_y);

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

        let style = new PIXI.TextStyle(menu_text_style);
        elems.b_name = new PIXI.Text("item", style);
        elems.b_name.position.set(50, 125);
        elems.b_price = new PIXI.Text("price", style);
        elems.b_price.position.set(155, 125);
        elems.b_qty = new PIXI.Text("qty", style);
        elems.b_qty.position.set(300, 125);


        elems.s_name = new PIXI.Text("item", style);
        elems.s_name.position.set(410, 125);
        elems.s_price = new PIXI.Text("price", style);
        elems.s_price.position.set(660, 125);
        elems.s_qty = new PIXI.Text("qty", style);
        elems.s_qty.position.set(810, 125);
        

        
        elems.bg = bg;
        elems.sell_bg = sell_bg;
        elems.selector = selector;

        

        elems.money = new PIXI.Text(menu_state.money, style);
        elems.money.position.set(sell_menu_style.x + sell_menu_style.width - sell_menu_style.money_right_margin, sell_menu_style.height - sell_menu_style.money_bottom_margin);

        menu.addChild(elems.bg);
        menu.addChild(elems.sell_bg);
        menu.addChild(elems.selector);
        menu.addChild(elems.b_name);
        menu.addChild(elems.b_qty);
        menu.addChild(elems.b_price)    ;
        menu.addChild(elems.s_name);
        menu.addChild(elems.s_qty);
        menu.addChild(elems.s_price)    ;
        menu.addChild(elems.money);
        menu.addChild(elems.title);
        menu.addChild(elems.buy_text);
        menu.addChild(elems.sell_text);

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

        let item_text = new PIXI.Text(item.name, style);
        item_text.position.set(x_pos, y_pos);

        let qty_text = new PIXI.Text(""+item.qty, style);
        qty_text.position.set(x_pos+menu_style.width-100, y_pos);

        let price_text = new PIXI.Text(""+item.cost, style)
        price_text.position.set(x_pos+menu_style.width-250, y_pos);

        menu.addChild(item_text);
        menu.addChild(qty_text);
        menu.addChild(price_text);

        renderable.item_text = item_text;
        renderable.price_text = price_text;
        renderable.qty_text = qty_text;
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

        let price_text = new PIXI.Text(""+item.cost, style)
        price_text.position.set(sell_menu_style.x+sell_menu_style.width-250, y_pos);

        menu.addChild(item_text);
        menu.addChild(qty_text);
        menu.addChild(price_text);

        renderable.item_text = item_text;
        renderable.qty_text = qty_text;
        renderable.price_text = price_text;
        renderable.bg = bg;
        renderable.item = item;

        s_renderables[item.id] = renderable;

        menu.updateLayersOrder();
    }

    function update_buy_item(r_item, item) {
        r_item.item_text = item.name;
        r_item.price_text.text = item.cost;
        r_item.qty_text.text = item.qty
    }

    function update_sell_item(r_item, item) {
        r_item.item_text = item.name;
        r_item.qty_text.text = item.qty;
        r_item.price_text.text = item.cost;
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
            if(menu_state.selector_menu == 'buy') {
                if(menu_state.selector_index < menu_state.items.length-1) {
                    menu_state.selector_index++;
                }
            } else if (menu_state.selector_menu == 'sell') {
                if(menu_state.selector_index < menu_state.sell_items.length-1) {
                    menu_state.selector_index++;
                }
            }
        };

        keys.left = keyboard(37);
        keys.left.press = function(){
            if(menu_state.selector_menu == 'sell') {
                menu_state.selector_menu = 'buy'
                menu_state.selector_index = Math.min(menu_state.items.length-1, menu_state.selector_index);
                if(menu_state.selector_index < 0) {
                    menu_state.selector_index = 0;
                }
            }
        };

        keys.right = keyboard(39);
        keys.right.press = function(){
            if(menu_state.selector_menu == 'buy') {
                menu_state.selector_menu = 'sell'
                menu_state.selector_index = Math.min(menu_state.sell_items.length-1, menu_state.selector_index);
                if(menu_state.selector_index < 0) {
                    menu_state.selector_index = 0;
                }
            }
        };

        keys.enter = keyboard(13);

        keys.enter.press = function() {
            if(menu_state.selector_menu === 'buy') {
                $.postJSON("/shop", {msg: "purchase", "item_id":menu_state.items[menu_state.selector_index].id}, 
                function(){
                    
                },
                function(err){
                    console.warn(err);
                })
            } else if (menu_state.selector_menu === 'sell') {
                $.postJSON("/shop", {msg: "sell", "item_id":menu_state.sell_items[menu_state.selector_index].id}, 
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
            menu_state.sell_items = []
            for(let i in data.inventory){
                let item = data.inventory[i];
                for(let j in menu_state.buy_items){
                    if(item.id === menu_state.buy_items[j].id){
                        item.cost = menu_state.buy_items[j].cost;
                        menu_state.sell_items.push(item);
                    }
                }
            }

            
            data.inventory;
            unlock_fn();
        }, function failure(err){
            console.warn(err);
            unlock_fn();
        });
        return menu_state;
    }

    function get_shop_data(unlock_fn) {
        $.getJSON("/shop", function success(data){
            menu_state.shop_name = data.name;
            menu_state.items = data.sale_items;
            menu_state.buy_items = data.buy_items;
            menu_state.shop_inv = data.inventory;

            for(let i in menu_state.items) {
                let item = menu_state.items[i];
                if(item.id in menu_state.shop_inv) {
                    item.qty = menu_state.shop_inv[item.id].qty;
                } else {
                    item.qty = 0;
                }
            }

            menu_keys.set_menu_state(menu_state);

            unlock_fn();
        }, function failure(err){
            console.warn(err);
            menu_state = {
                items:[],
                selector_index:0,
                selector_menu:'buy'
            }
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
        for(let ii in renderables) {
            for(let ij in renderables[ii]){
                menu.removeChild(renderables[ii][ij]);
            }
        }
        for(let ii in s_renderables) {
            for(let ij in s_renderables[ii]){
                menu.removeChild(s_renderables[ii][ij]);
            }
        }
        renderables = {};
        s_renderables = {};

        for(let i in menu_state.items) {
            let item = menu_state.items[i];
            if(!(item.id in renderables)) {
                if(!item.pos) {
                    item.pos = cnt;
                }
                render_item(menu, item);
            }else{
                update_buy_item(renderables[item.id], item);
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
        elems.title.text = menu_state.shop_name;

        elems.selector.x = menu_state.selector_menu === 'buy' ? menu_style.x + menu_style.selector_margin_left : sell_menu_style.x + menu_style.selector_margin_left; 
        elems.selector.y = menu_style.item_height*menu_state.selector_index+menu_style.y+menu_style.item_bottom_margin;

        let sell_menu_width = sell_menu_style.width - sell_menu_style.item_left_margin - sell_menu_style.item_left_margin;
        let buy_menu_width = menu_style.width - menu_style.item_left_margin - menu_style.item_left_margin;
        elems.selector.width = menu_state.selector_menu === 'buy' ? buy_menu_width : sell_menu_width;
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