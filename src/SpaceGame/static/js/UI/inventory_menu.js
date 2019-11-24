

var InventoryMenu = (function() {

	 var guiObj = {
        id:'inventoryWindow',
        component:'Window',
        padding:4,
        position:{x:10, y:10},
        width:500, 
        height:500,
        layout:[1, 1],
        children: [
		]

    }

    var invList = {        		
		id: 'invList2',
		component: 'List',
		dragX:false,
		padding: 3,
		position: {x:0, y:0},
		width: 500,
		height: 450,
		layout: [1, 8]
    }

    var listItem = {
    	component: 'Window',
    	position: 'left',
    	width: 500,
    	height: 50, 
    	layout: [3, 1]
    }

	var guiContainer;


	function InventoryMenu() {
		this.visible = false;
		this.list = null;

	}

	InventoryMenu.prototype.load = function() {
        guiContainer = EZGUI.create(guiObj, 'kenney');
	}

	InventoryMenu.prototype.show = function(stage) {
		if(!this.visible) {
			this.loadData()
			stage.addChild(guiContainer);
		}
		this.visible = true;

	}

	InventoryMenu.prototype.hide = function(stage) {
		if(this.visible) {
			stage.removeChild(guiContainer);
		}
		this.visible = false;
	}

	InventoryMenu.prototype.toggle = function(stage) {
		if(this.visible === false) {

            this.show(stage); 
        } else {
            this.hide(stage);
        }
	}

	InventoryMenu.prototype.loadData = function() {
		$.getJSON("/inv", function success(data){
            var menu_state = {};
            menu_state.inv = data.inventory;

            if(this.list) {
            	EZGUI.components.inventoryWindow.removeChild(list)
            	this.list = null;
            }
            let listSpec = JSON.parse(JSON.stringify(invList))
            this.list = EZGUI.create(listSpec, 'kenney');
            EZGUI.components.inventoryWindow.addChild(this.list);

            for(var i = 0; i < menu_state.inv.length; i++) {
            	let item = menu_state.inv[i];
				let li = JSON.parse(JSON.stringify(listItem));
				li.children = [
					{id:'it_iname_'+i, component:"Window", text:item.name, width:'33%', height:'100%', position:'left'},
					{id:'it_iqty_'+i, component:"Window", text:item.qty, width:'33%', height:'100%', position:'right'}
				];
				let child = EZGUI.create(li, 'kenney');
				EZGUI.components['it_iqty_'+i].rebuild();
				EZGUI.components.invList2.addChild(child);
				
			}

			

        }, function failure(err){

        });
        

		

	}



	return InventoryMenu;
})();