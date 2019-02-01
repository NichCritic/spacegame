
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