

var UpgradeMenu = (function() {

	 var guiObj = {
        id:'upgradeWindow',
        component:'Window',
        padding:4,
        position:{x:10, y:10},
        width:500, 
        height:500,
        layout:[1, 1],
        children: [{
        		
							id: 'invList',
							component: 'List',
							dragX:false,
							padding: 3,
							position: {x:0, y:0},
							width: 500,
							height: 450,
							layout: [1, 8]

        	}
		]

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
		$.getJSON("/upgrade", function success(data){
            var menu_state = {};
            menu_state.upgrades = data.upgrades;

            for(var i = 0; i < menu_state.upgrades.length; i++) {
            	let item = menu_state.upgrades[i];
				let li = JSON.parse(JSON.stringify(listItem));
				li.children = [
					{id:'it_uname_'+i, component:"Window", text:item.name, width:'33%', height:'100%', position:'left'},
					{id:'it_uqty_'+i, component:"Window", text:item.qty, width:'33%', height:'100%', position:'right'},
					{id:'btn_upgrade_'+i, component:"Button", text:"apply", width:'33%', height:'100%', position:'right', userData:{'id':item.id}}
				];
				let child = EZGUI.create(li, 'kenney'); 
				EZGUI.components.invList.addChild(child);
				EZGUI.components["btn_upgrade_"+i].on('click', function(event, me){
					$.postJSON("/upgrade", {msg: "upgrade", "item_id":me.userData.id}, 
                	function(){
                    
                	},
                	function(err){
                    	console.warn(err);
                	})
				})
			}

			

        }, function failure(err){

        });
        

		

	}



	return new UpgradeMenu;
});