

var MapMenu = (function() {

    function MapMenu() {
        var map_menu = $("#map_menu").dialog({autoOpen:false, open:this.loadData.bind(null, this)});
        // var inv_list = $("#inv_list").menu();
    } 
   
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
            
            ctx.fillStyle = 'red'
            for(var i in data.positions) {
                let x = data.positions[i].x
                let y = data.positions[i].y
                item = {};

                item.x = 125+ (x-p.x) / 50;
                item.y = 125+ (y-p.y) / 50;
                ctx.fillRect(item.x-2.5, item.y-2.5, 5, 5)
            }

            setTimeout(menu.loadData.bind(null, menu), 250);
        });
    }

    return MapMenu;
})();