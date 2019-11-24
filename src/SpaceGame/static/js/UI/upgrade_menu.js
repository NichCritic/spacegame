

var UpgradeMenu = (function() {

	 var guiObj = {
        id:'upgradeWindow',
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
		id: 'invList',
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


	function UpgradeMenu() {
		this.visible = false;
		this.upgrade_list = false;
	}

	UpgradeMenu.prototype.load = function() {
        guiContainer = EZGUI.create(guiObj, 'kenney');
	}

	UpgradeMenu.prototype.show = function(stage) {
		if(!this.visible) {
			this.loadData()
			stage.addChild(guiContainer);
		}
		this.visible = true;

	}

	UpgradeMenu.prototype.hide = function(stage) {
		if(this.visible) {
			stage.removeChild(guiContainer);
		}
		this.visible = false;
	}

	UpgradeMenu.prototype.toggle = function(stage) {
		if(this.visible === false) {

            this.show(stage); 
        } else {
            this.hide(stage);
        }
	}

	UpgradeMenu.prototype.loadData = function() {
		let self = this;
		$.getJSON("/upgrade", function success(data){
            var menu_state = {};
            menu_state.upgrades = data.upgrades;

            if(this.upgrade_list) {
            	EZGUI.components.upgradeWindow.removeChild(this.upgrade_list);
            }
            let uls = JSON.parse(JSON.stringify(invList));
            this.upgrade_list = EZGUI.create(uls, "kenney");
            EZGUI.components.upgradeWindow.addChild(this.upgrade_list)

            for(var i = 0; i < menu_state.upgrades.length; i++) {
            	let item = menu_state.upgrades[i];
            	if(EZGUI.components['it_uqty_'+i]) {
						EZGUI.components['it_uqty_'+i].erase();
				}
				let li = JSON.parse(JSON.stringify(listItem));
				li.children = [
					{id:'it_uname_'+i, component:"Window", text:item.name, width:'33%', height:'100%', position:'left'},
					{id:'it_uqty_'+i, component:"Window", text:item.qty, width:'33%', height:'100%', position:'right'},
					{id:'btn_upgrade_'+i, component:"Button", text:"apply", width:'33%', height:'100%', position:'right', userData:{'id':item.id}}
				];
				let child = EZGUI.create(li, 'kenney');
				// EZGUI.components['it_uqty_'+i].rebuild(); 
				// child.rebuild();
				

				EZGUI.components.invList.addChild(child);
				EZGUI.components["btn_upgrade_"+i].on('click', function(event, me){
					$.postJSON("/upgrade", {msg: "upgrade", "item_id":me.userData.id}, 
                	function(){
                    	self.loadData();
                	},
                	function(err){
                    	console.warn(err);
                	})
				})
			}

			

        }, function failure(err){

        });
        

		

	}



	return UpgradeMenu;
})();