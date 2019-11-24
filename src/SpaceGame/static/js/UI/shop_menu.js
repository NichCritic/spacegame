

var ShopMenu = (function() {

	 var guiObj = {
        id:'myWindow',
        component:'Window',
        padding:4,
        position:{x:10, y:10},
        width:500, 
        height:500,
        layout:[1, 1],
        children: [{
        		id: 'tabsObj',
        		component:'Tabs',
        		tabHeight:40,
        		padding:1,
        		position:{x:0, y:0},
        		width:500,
        		height:450,
        		children: [
        			{ id: 'buy_tab', text: 'buy', title: 'buy', userData: 'buy_tab', component: 'Button', position: 'center', width: "100%", height: "100%", skin: 'levelBtn', active:true, children:[]},
        			{ id: 'sell_tab', text: 'sell', title: 'sell', userData: 'sell_tab', component: 'Button', position: 'center', width: "100%", height: "100%", skin: 'levelBtn', children:[]}

        		]
        	}
		]

    }

    var buyItemList = {
		id: 'buyItemList',
		component: 'List',
		dragX:false,
		padding: 3,
		position: {x:0, y:0},
		width: 500,
		height: 450,
		layout: [1, 8]
	};

	var sellItemList = {
		id: 'sellItemList',
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


	function ShopMenu() {
		this.visible = false;
		this.buy_item_list = null;
		this.sell_item_list = null;

	}

	ShopMenu.prototype.load = function(cb) {
        guiContainer = EZGUI.create(guiObj, 'kenney');
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
		let self = this;
		$.getJSON("/shop", function success(data){
            var menu_state = {};
            menu_state.shop_name = data.name;
            menu_state.items = data.sale_items;
            menu_state.buy_items = data.buy_items;
            menu_state.shop_inv = data.inventory;
            menu_state.player_inv = data.player_inventory;
 
           	if(this.buy_item_list) {
           		EZGUI.components.buy_tab.removeChild(this.buy_item_list);
           	}
           	if(this.sell_item_list) {
           		EZGUI.components.sell_tab.removeChild(this.sell_item_list);
           	}
           	let buy_items_spec = JSON.parse(JSON.stringify(buyItemList)); 
           	this.buy_item_list = EZGUI.create(buy_items_spec, 'kenney');
           	EZGUI.components.buy_tab.addChild(this.buy_item_list)

           	let sell_items_spec = JSON.parse(JSON.stringify(sellItemList)); 
           	this.sell_item_list = EZGUI.create(sell_items_spec, 'kenney');
           	EZGUI.components.sell_tab.addChild(this.sell_item_list)

            for(var i = 0; i < menu_state.buy_items.length; i++) {
            	let item = menu_state.buy_items[i];
            	let qty = item.id in menu_state.player_inv ? menu_state.player_inv[item.id].qty : 0;
				let li = JSON.parse(JSON.stringify(listItem));
				li.children = [
					{id:'it_bname_'+i, component:"Window", text:item.name, width:'33%', height:'100%', position:'left'},
					{id:'it_bqty_'+i, component:"Window", text:qty, width:'33%', height:'100%', position:'right'},
					{id:'btn_sell_'+i, component:"Button", text:"sell for " +item.cost, width:'33%', height:'100%', position:'right', userData:{'id':item.id}}
				];
				let child = EZGUI.create(li, 'kenney'); 
				EZGUI.components.sellItemList.addChild(child);
				EZGUI.components["btn_sell_"+i].on('click', function(event, me){
					$.postJSON("/shop", {msg: "sell", "item_id":me.userData.id}, 
                	function(){
                    	self.loadData();
                	},
                	function(err){
                    	console.warn(err);
                	})
				})
			}

			for(var i = 0; i < menu_state.items.length; i++) {
            	let item = menu_state.items[i];
				let li = JSON.parse(JSON.stringify(listItem));
				li.children = [
					{id:'it_sname_'+i, component:"Window", text:item.name, width:'33%', height:'100%', position:'left'},
					{id:'it_sqty_'+i, component:"Window", text:item.qty, width:'33%', height:'100%', position:'right'},
					{id:'btn_buy_'+i, component:"Button", text:"buy for "+item.cost, width:'33%', height:'100%', position:'right', userData:{'id':item.id}}
				];
				let child = EZGUI.create(li, 'kenney'); 
				EZGUI.components.buyItemList.addChild(child);
				EZGUI.components["btn_buy_"+i].on('click', function(event, me){
					$.postJSON("/shop", {msg: "purchase", "item_id":me.userData.id}, 
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



	return ShopMenu;
})();