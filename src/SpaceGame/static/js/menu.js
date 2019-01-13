var MenuState = (function() {
    var menu; menu = new PIXI.Container();

    var keys = {};

    var menu_state = {
        items: [
            {id: "0001", pos:0, text:"Rockets", cost:10000, img:""}
        ]
    };

    var renderables = {};

    var menu_mode = {
        init: setup_menu,
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

        keys.up = keyboard(38);
        keys.down = keyboard(40);

    }

    function get_state() {
        return menu_state
    }

    function render_item(item) {
        var bg = new PIXI.graphics();
        bg.beginFill(0xB2C7B2);
        bg.drawRect(0, 0, 700-5, 50);
        bg.endFill();
        bg.x = 50+5;
        bg.y = 50*item.pos+5;
        menu.addChild(bg);

        let style = new TextStyle({
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

        let item_text = new Text(item.text, style);
        item_text.position.set()

    }

    function render_menu(renderer, state, menu) {
        renderer.render(menu);
        for(i in state.items) {
            let item = state.items[i];
            if(!item.id in renderables) {
                render_item(item);
            }
        }
    }

    return menu_mode;
});