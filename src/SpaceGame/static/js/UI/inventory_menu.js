

var InventoryMenu = (function() {

	function InventoryMenu() {
		var inv_menu = $("#inv_menu").dialog({
            autoOpen:false, 
            open:this.loadData.bind(null, this),
            close: this.cancelTimer.bind(null, this),
            position: { my: "right top", at: "right top", of: window }
        });
        var inv_list = $("#inv_list").menu();
        this.timeout = null;
	}

    InventoryMenu.prototype.cancelTimer = function(menu) {
        clearTimeout(menu.timeout);
        menu.timeout = null
    }; 
   
   	InventoryMenu.prototype.loadData = function (self, event, ui) {
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
            if(!self.timeout) {
                self.timeout = setInterval(self.loadData.bind(null, self), 250);
            }
        });
    }

	return InventoryMenu;
})();