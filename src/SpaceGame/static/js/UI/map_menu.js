

var MapMenu = (function() {

    function MapMenu() {
        var map_menu = $("#map_menu").dialog({
            autoOpen:false, 
            open:this.loadData.bind(null, this),
            close: this.cancelTimer.bind(null, this),
            position: { my: "right bottom", at: "right bottom", of: window }
        });
        this.timeout = null;
    } 

    MapMenu.prototype.cancelTimer = function(menu) {
        clearTimeout(menu.timeout);
        menu.timeout = null
    };
   
    MapMenu.prototype.loadData = function (menu, event, ui) {
        $.getJSON("/minimap", function success(data){
            let canvas = $("#map_canvas")[0];
            let ctx = canvas.getContext('2d')


            ctx.fillStyle = 'black'
            ctx.fillRect(0, 0, 250, 250)

            let x = data.player.x;
            let y = data.player.y;
            let p = {};
            p.x = x;
            p.y = y;
            ctx.fillStyle = 'green'
            ctx.fillRect(125, 125, 5, 5);

            
            for(var i in data.positions) {

                let x = data.positions[i].x
                let y = data.positions[i].y
                if (data.positions[i].id == data.player.id) {
                    continue;
                }

                let item = {};
                let size = Math.max(data.positions[i].radius/50, 2);

                item.x = 125+ (x-p.x) / 50;
                item.y = 125+ (y-p.y) / 50;
                ctx.fillStyle = 'yellow';
                if(data.positions[i].type === "boss" || data.positions[i].type === 'ship') {
                    ctx.fillStyle = 'red';
                }
                ctx.fillRect(item.x-2.5, item.y-2.5, size, size)
            }
            if(!menu.timeout) {
                menu.timeout = setInterval(menu.loadData.bind(null, menu), 1000);
            }
        });
    }

    return MapMenu;
})();