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
        for(let ii in renderables) {
            for(let ij in renderables[ii]){
                menu.removeChild(renderables[ii][ij]);
            }
        }
        renderables= {};

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