

var ShopMenu = (function() {


	function ShopMenu() {
		var shop_menu = $("#shop_menu").dialog({autoOpen:false, open:loadShopData});
        var shop_tabs = $("#shop_tabs").tabs();
        
        var buy_menu = $("#shop_buy_list");
        var sell_menu = $("#shop_sell_list");

        buy_menu.menu({select: sell_item});
        sell_menu.menu({select: buy_item});
	}

    function buy_item(event, ui) {
        $.postJSON("/shop", {msg: "buy", "item_id":ui.item.data('item_id')}, 
            function(){
                setTimeout(loadShopData, 100);
            },
            function(err){
                console.warn(err);
            });
    }

    function sell_item(event, ui) {
        $.postJSON("/shop", {msg: "sell", "item_id":ui.item.data('item_id')}, 
            function(){
                setTimeout(loadShopData, 100);
            },
            function(err){
                console.warn(err);
            });
    }

    function loadShopData(event, ui) {
        $.getJSON("/shop", function success(data){
            var menu_state = {};
            var buy_menu = $("#shop_buy_list");
            var sell_menu = $("#shop_sell_list");
            buy_menu.empty();
            sell_menu.empty();
            menu_state.shop_name = data.name;
            menu_state.items = data.sale_items;
            menu_state.buy_items = data.buy_items;
            menu_state.shop_inv = data.inventory;
            menu_state.player_inv = data.player_inventory;
 
            for(var i = 0; i < menu_state.buy_items.length; i++) {
                let item = menu_state.buy_items[i];
                let qty = item.id in menu_state.player_inv ? menu_state.player_inv[item.id].qty : 0;
                $("<li><div>"+item.name +":"+qty+". Sell for "+item.cost+"</div></li>").appendTo(buy_menu).data("item_id", item.id);   

            }

            for(var i = 0; i < menu_state.items.length; i++) {
                let item = menu_state.items[i];
                let qty = item.id in menu_state.player_inv ? menu_state.player_inv[item.id].qty : 0;
                $("<li><div>"+item.name +":"+qty+". Buy for "+item.cost+"</div></li>").appendTo(sell_menu).data("item_id", item.id);
            }


            buy_menu.menu("refresh");
            sell_menu.menu("refresh");

        }, function failure(err){

        });

        $.getJSON("/money", function success(data){
            $("#money").html("Money:"+ data.money);

        }, function failure(err) {});

    
	}




	return ShopMenu;
})();