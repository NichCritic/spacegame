

var InventoryMenu = (function() {

	function InventoryMenu() {
		var inv_menu = $("#inv_menu").dialog({autoOpen:false, open:this.loadData});
        var inv_list = $("#inv_list").menu();
	} 
   
   	InventoryMenu.prototype.loadData = function (event, ui) {
        $.getJSON("/inv", function success(data){
            var menu = $("#inv_list");
            menu.empty();
            var menu_state = {};
            menu_state.inv = data.inventory;
            for(var i = 0; i < menu_state.inv.length; i++) {
                let item = menu_state.inv[i];
                $("<li><div>"+item.name +":"+item.qty+"</div></li>").appendTo(menu);
            }
            menu.menu("refresh");
        });
    }

	return InventoryMenu;
})();