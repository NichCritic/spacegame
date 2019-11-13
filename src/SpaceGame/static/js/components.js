var components = (function(){ 
	var Position = function(entity_id, data) {
		this.entity_id = entity_id
		this.x = data.x
		this.y = data.y
	};
	var Velocity = function(entity_id, data) {
		this.entity_id = entity_id
		this.x = data.x
		this.y = data.y
	};
	var Acceleration = function(entity_id, data) {
		this.entity_id = entity_id,
		this.x = data.x,
		this.y = data.y
	};
	var Force = function(entity_id, data) {
		this.entity_id = entity_id
		this.x = data.x
		this.y = data.y
	};
	var Thrust = function(entity_id, data) {
		this.entity_id = entity_id;
		this.thrust = data.thrust;
	};
	var Mass = function(entity_id, data) {
		this.entity_id = entity_id;
		this.mass = data.mass;
	};

	var Rotation = function(entity_id, data) {
		this.entity_id = entity_id;
		this.rotation = data.rotation;
	};

	var Renderable = function(entity_id, data) {
		this.entity_id = entity_id;
		this.spritesheet = data.spritesheet;
		this.image = data.image;
		this.width = data.width;
		this.height = data.height;
		//this.transform = data.transform
	};
	var State = function(entity_id, data) {
		this.entity_id = entity_id;
		this.state = data.state;
	};
	var Camera = function(entity_id) {
		this.entity_id = entity_id;
	};

	var ShipControl = function(entity_id, data) {
		this.entity_id = entity_id;
		this.left = data.left;
		this.right = data.right;
		this.thrust = data.thrust;
		this.brake = data.brake;
		this.dt = data.dt;
	}

	var Control = function(entity_id, data) {
		this.entity_id = entity_id;
		this.left = data.left;
		this.right = data.right;
		this.thrust = data.thrust;
		this.brake = data.brake;
		this.shoot = data.shoot;
		this.dt = data.dt;
		this.time = data.time;
	};
	var PlayerControlled = function(entity_id) {
		this.entity_id = entity_id;
	}

	var ServerControlled = function(entity_id) {
		this.entity_id = entity_id;
	}

	var ServerUpdate= function(entity_id, data) {
		this.entity_id = entity_id;
		this.data = data.data;
	}
	
	var Inputs = function(entity_id, data) {
		this.entity_id = entity_id;
		this.inputs = data.inputs;
	}

	var Area = function(entity_id, data) {
		this.entity_id = entity_id;
		this.radius = data.radius;
	}

	var Animated = function(entity_id, data) {
		this.entity_id = entity_id;
		this.update_rate = data.update_rate;
		this.frame = data.frame ? data.frame:0;
		this.residual_cooldown = 0
	}

	var ToBeRemoved = function(entity_id) {
		this.entity_id = entity_id;
	}

	var Health = function(entity_id, data) {
		this.entity_id = entity_id;
		this.health = data.health;
		this.max_health = data.max_health;
	}

	var Type = function(entity_id, data) {
		this.entity_id = entity_id;
		this.type = data.type;
	}

	var Shooting = function(entity_id, data) {
		this.entity_id = entity_id;
		this.input = data.input;
		this.firing_rate = data.firing_rate;
	
	}

	var ShootingVars = function(entity_id, data) {
		this.entity_id = entity_id;
		this.last_update = Date.now();
		this.bullets_fired = 0;
		this.residual_cooldown = null; //Make null so it can be init to variable firing rate
	}

	var Expires = function(entity_id, data) {
		this.entity_id = entity_id
		this.expiry_time_ms = data.expiry_time_ms;
		this.creation_time = data.creation_time;
	}

	var ServerSync = function(entity_id, data) {
		this.entity_id = entity_id
		this.sync_key = data.sync_key
	}

	var ClientSync = function(entity_id, data) {
		this.entity_id = entity_id
		this.sync_key = data.sync_key
	}

	var PlayerCreated = function(entity_id, data) {
		this.entity_id = entity_id
	}

	var Colliding = function(entity_id, data) {
		this.entity_id = entity_id
		this.collisions = []
	}

	var Collidable = function(entity_id, data) {
		this.entity_id = entity_id
	}

	var Mining = function(entity_id, data) {
		this.entity_id = entity_id;
	}

	var Minable = function(entity_id, data) {
		this.entity_id = entity_id;
	}

	var components = {
		"position":Position,
		"velocity":Velocity,
		"acceleration":Acceleration,
		"force":Force,
		"thrust":Thrust,
		"mass": Mass,
		"rotation": Rotation,
		"renderable": Renderable,
		"camera": Camera,
		"control": Control, 
		"player": PlayerControlled,
		"server_controlled": ServerControlled,
		"server_update": ServerUpdate,
		"inputs":Inputs,
		"area": Area,
		"animated":Animated,
		"to_be_removed": ToBeRemoved,
		"health": Health,
		"type": Type,
		"ship_control": ShipControl,
		"shooting": Shooting,
		"shooting_vars": ShootingVars,
		"expires": Expires,
		"server_sync": ServerSync,
		"client_sync": ClientSync,
		"player_created": PlayerCreated,
		"collidable": Collidable,
		"colliding": Colliding,
		"minable": Minable,
		"mining": Mining
	};

	return components
})();

var EntityManager = (function(){
	function EntityManager() {

		return this;
	}

	EntityManager.prototype.init = function() {
		this.last_id = 0;
	}

	EntityManager.prototype.new_entity = function() {
		return ++this.last_id;
	}
 
	return EntityManager;
})();

var NodeFactory = (function(entity_manager, component_manager) {
	function NodeFactory(entity_manager, component_manager) {
		this.entity_manager = entity_manager
		this.component_manager = component_manager;
	}

	NodeFactory.prototype.init = function() {

	}

	NodeFactory.prototype.create_node = function(components, entity_id) {
		let n = Node(this.component_manager);

		e_id = entity_id ? entity_id : this.entity_manager.new_entity();

		n.init(e_id, []);

		let component_ids = Object.keys(components);
		for(let c in component_ids) {
			let comp = component_ids[c];
			n.add_or_attach(comp, components[comp]);
		}
		return n;
	}

	NodeFactory.prototype.create_node_list = function(mandatory, optional, entity_ids) {
		optional = optional ? optional : [];

		let nodes = [];
		entities = this.component_manager.get_entities_with_components(mandatory);

		let all_components = []
		all_components = all_components.concat(mandatory);
		all_components = all_components.concat(optional);

		for(let i = 0; i < entities.length; i++) {
			var n = Node(this.component_manager);
			let entity_id = entities[i];
			n.init(entity_id, []);
			for(let j = 0; j < all_components.length; j++) {
				let comp = all_components[j];
				if(this.component_manager.entity_has_component(entity_id, comp)) {
					n.add_or_attach(comp, {});
				}
			}
			nodes.push(n);

		}
		return nodes;

	}
	var Node = (function(component_manager) {

		function Node(component_manager) {
			this.component_manager = component_manager;
			return this;
		}

		Node.prototype.init = function(entity_id, components) {
			this.id = entity_id
			this.component_list = Object.keys(components)
			for(let i in this.component_list){
				c = this.component_list[i];
				this[c] = components[c];
			}
		}

		Node.prototype.has = function(compo) {
			return this.component_list.indexOf(compo) > -1;
		};

		Node.prototype.entity_has = function(comp) {
			return this.component_manager.entity_has_component(this.id, comp);
		}

		Node.prototype.add_or_attach = function(comp, comp_data) {
			if(this.has(comp)){
				return;
			}
			if(!this.component_manager.entity_has_component(this.id, comp)) {
				this.component_manager.add_component_to_entity(this.id, comp, comp_data)
			}
			this.component_list.push(comp);
			this[comp] = this.component_manager.get_component_data_for_entity(this.id, comp);

		};

		Node.prototype.add_or_update = function(comp, comp_data) {
			this.component_manager.update_component_for_entity(this.id, comp, comp_data);
			this.component_list.push(comp);
			this[comp] = this.component_manager.get_component_data_for_entity(this.id, comp);
		};

		Node.prototype.remove_component = function(comp) {
			delete this[comp];
			this.component_list = this.component_list.filter(function(i){i !== comp});
		};

		Node.prototype.delete_component = function(comp) {
			this.remove_component(comp);
			this.component_manager.remove_component_from_entity(this.id, comp);
		}

		Node.prototype.delete_all_components = function(comp) {
			for(let i = 0; i < this.component_list.length; i++) {
				this.remove_component(this.component_list[i]);
			}
			this.component_manager.remove_all_components_from_entity(this.id);
		}	

		return new Node(component_manager);
	});

	return new NodeFactory(entity_manager, component_manager);
});




var ComponentManager = (function(){
	function ComponentManager() {
		return this
	}

	ComponentManager.prototype.init = function(component_objects, components) {
		this.component_objects = component_objects;
		this.components = components;
	};

	ComponentManager.prototype.add_component_to_entity = function(entity_id, component_id, component_data){
		if(!this.component_objects[component_id]){
			this.component_objects[component_id] = {};
		}

		if(this.component_objects[component_id][entity_id]) {
			throw "Component with entity_id "+entity_id+" already has component_id " + component_id;
		}

		this.component_objects[component_id][entity_id] = new this.components[component_id](entity_id, component_data);
	}

	ComponentManager.prototype.update_component_for_entity = function(entity_id, component_id, component_data){
		if(!this.component_objects[component_id]){
			this.component_objects[component_id] = {}
		}
		if(!this.component_objects[component_id][entity_id]){
			this.add_component_to_entity(entity_id, component_id, component_data);
			return
		}

		this.component_objects[component_id][entity_id] = new this.components[component_id](entity_id, component_data);
	}

	ComponentManager.prototype.remove_component_from_entity = function(entity_id, component_id) {
		if(!this.component_objects[component_id]){
			return;
		}
		delete this.component_objects[component_id][entity_id];
	}

	ComponentManager.prototype.remove_all_components_from_entity = function(entity_id) {
		let all_components = Object.keys(components);
		for(let j in all_components) {
			let comp = all_components[j];
			if(this.component_objects[comp] && this.component_objects[comp][entity_id]) {
				delete this.component_objects[comp][entity_id];
			}
		}
	}

	ComponentManager.prototype.entity_has_component = function(entity_id, component_id) {
		if(!this.component_objects[component_id]){
			return false
		}
		return !!this.component_objects[component_id][entity_id];
	}

	ComponentManager.prototype.get_entities_with_component = function(component_id) {
		if(this.component_objects[component_id]) {
			return Object.keys(this.component_objects[component_id]);
		}
		return [];
	}

	ComponentManager.prototype.get_entities_with_components = function(components_list, entity_ids) {
		let intersection = [];

		var entities0 = entity_ids ? entity_ids : this.get_entities_with_component(components_list[0]);

		var start = entity_ids ? 0 : 1;

		for(let i = start; i < components_list.length; i++) {
			let entities = this.get_entities_with_component(components_list[i]);
			for(let j = 0; j < entities.length; j++) {
				let entity = entities[j];
				if (entities0.indexOf(entity) > -1) {
					intersection.push(entity);
				} 
			}
			entities0 = intersection;
			intersection = [];
		}
		intersection = entities0;
		return intersection;
	}

	ComponentManager.prototype.get_component_data_for_entity = function(entity_id, component_id) {
		if(!this.component_objects[component_id]) {
			return null;
		}
		return this.component_objects[component_id][entity_id];
	}

	return new ComponentManager();
})();
