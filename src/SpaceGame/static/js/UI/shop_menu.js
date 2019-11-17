var ShopMenu = (function() {

	 var guiObj = {
        id:'myWindow',
        component:'Window',
        padding:4,
        position:{x:10, y:10},
        width:500, 
        height:500,
        layout:[1, 1],
        children: [
		{
			id: 'itemList',
			component: 'List',
			dragX:false,
			padding: 3,
			position: {x:0, y:0},
			width: 590,
			height: 450,
			layout: [1, 6]
		}]

    }

    var listItem = {
    	component: 'Window',
    	position: 'center',
    	width: 120,
    	height: 50
    }

	var guiContainer;


	function ShopMenu() {
		this.visible = false;

	}

	ShopMenu.prototype.load = function(cb) {
		EZGUI.Theme.load(["static/assets/kenney-theme/kenney-theme.json"], function(){
            guiContainer = EZGUI.create(guiObj, 'kenney');
            //stage.addChild(guiContainer);
            cb();
        });
	}

	ShopMenu.prototype.show = function(stage) {
		if(!this.visible) {
			this.loadData()
			stage.addChild(guiContainer);
		}
		this.visible = true;

	}

	ShopMenu.prototype.hide = function(stage) {
		if(this.visible) {
			stage.removeChild(guiContainer);
		}
		this.visible = false;
	}

	ShopMenu.prototype.toggle = function(stage) {
		if(this.visible === false) {

            this.show(stage); 
        } else {
            this.hide(stage);
        }
	}

	ShopMenu.prototype.loadData = function() {
		for(var i = 0; i < 10; i++) {
			let li = JSON.parse(JSON.stringify(listItem));
			li.text = "List Item " + i;
			let child = EZGUI.create(li, 'kenney'); 
			EZGUI.components.itemList.addChild(child);
		}

	}



	return new ShopMenu;
});