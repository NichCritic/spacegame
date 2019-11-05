
var ServerSyncSystem = (function() {
	var manditory = ["server_sync"];
	var optional = [];
	var handles = [];

	function ServerSyncSystem(node_factory) {
		this.node_factory = node_factory;
	}

	ServerSyncSystem.prototype.process = function() {
		var nodes = this.node_factory.create_node_list(manditory, optional);
		var server_nodes = this.node_factory.create_node_list(['client_sync'], [])
		server_node_hash = {}
		for(var i = 0; i < server_nodes.length; i++){ 
			server_node_hash[server_nodes[i].client_sync.sync_key] = server_nodes[i];
		}


		for(var i = 0; i < nodes.length; i++) {
			let node = nodes[i];
			if(node.server_sync.sync_key in server_node_hash) {
				//There's a match. Copy (what?) Data from the original and delete the duplicate
				//Maybe just merge the entities. If they share components use the server's copy 
				//otherwise use the client's
				//Make sure client_sync and server_sync are gone though
				//console.log("Turns out this works")
				let key = node.server_sync.sync_key;
				let snode = server_node_hash[key];
				node.add_or_attach("expires")
				snode.add_or_attach("expires", node.expires);
				node.add_or_attach("to_be_removed");
				snode.add_or_attach("player_created");
				snode.delete_component("client_sync")
				node.delete_component("server_sync")
				continue
			}
			//Otherwise just ignore it, might turn up later?
			//If this becomes an issue shove a timer on it, and delete them if the server fails 
			//to create after X seconds. But in absence of a problem we'll ignore for now
			var now = Date.now();
			node.add_or_update("expires", {
				creation_time:now,
				expiry_time_ms: 1000
			})
		}
	};

	return ServerSyncSystem; 
})();