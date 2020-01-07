

var UpgradeMenu = (function() {


	function UpgradeMenu() {
		var upgr_menu = $("#upgrade_menu").dialog({autoOpen:false, open:loadData,
                position: { my: "right top", at: "right top", of: window }
        });
        var upgr_list = $("#upgr_list").menu({select:applyUpgrade});
	}

	function loadData(event, ui) {
        $.getJSON("/upgrade", function success(data){
            var menu = $("#upgr_list");
            menu.empty();
            var menu_state = {};
            menu_state.upgr = data.upgrades;
            for(var i = 0; i < menu_state.upgr.length; i++) {
                let item = menu_state.upgr[i];
                $("<li><div>"+item.name +":"+item.qty+"-------Click to apply</div></li>").appendTo(menu).data("item_id", item.id);
            }
            menu.menu("refresh");
        });
    }

    function applyUpgrade(event, ui) {
        $.postJSON("/upgrade", {"item_id":ui.item.data('item_id')}, 
            function(){
                setTimeout(loadData, 100);
            },
            function(err){
                console.warn(err);
            });
    }

	return UpgradeMenu;
})();