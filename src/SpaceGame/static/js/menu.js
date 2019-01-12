var menu; menu = new PIXI.Container();

var menu_state = {
    stage:menu,
    get_input: function(){},
    get_state: function(){},
    update: function(){},
    render: render_menu,
    update_server:function(){}
}


function setup_menu(keys) {
    var bg = new PIXI.Graphics();
    bg.beginFill(0xD2E7D2);
    bg.drawRect(0, 0, 700, 500);
    bg.endFill();
    bg.x = 50;
    bg.y = 50;
    menu.addChild(bg);

    keys.c = keyboard(67);
    keys.c.press = function() {
        if(mode == menu_state) {
            mode = game_state
        }
        else
        {
            mode = menu_state
        }
    }
}

function render_menu(renderer, textures, sprites, state, menu) {
    renderer.render(menu);
}