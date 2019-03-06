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
		this.entity_id = entity_id
		this.x = data.x
		this.y = data.y	
	};
	var Mass = function(entity_id, data) {
		this.entity_id = entity_id;
		this.mass = data.mass;
	};

	var Rotation = function(entity_id, data) {
		this.entity_id = entity_id;
		this.rotation = data.rotation;
	}

	var Renderable = function(entity_id, data) {
		this.entity_id = entity_id
		this.spritesheet = data.spritesheet
		//this.transform = data.transform
	},
	var State = function(entity_id, data) {
		this.entity_id = entity_id;
		this.state = data.state;
	}

	var components = {
		"position":Position,
		"velocity":Velocity,
		"acceleration":Acceleration,
		"force":Force,
		"thrust":Thrust,
		"mass": Mass,
		"rotation": Rotation,
		"renderable": Renderable
	}

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
});

var NodeFactory = (function(entity_manager, component_manager) {
	function NodeFactory(entity_manager, component_manager) {
		this.entity_manager = entity_manager
		this.component_manager = component_manager;
	}

	NodeFactory.prototype.init = function() {

	}

	NodeFactory.prototype.create_node = function(components) {
		let n = Node();
		n.init(this.entity_manager.new_entity(), []);

		let components = Object.keys(components);
		for(let c in components) {
			n.add_or_attach_component(c, components[c]);
		}

	}

	NodeFactory.prototype.create_node_list = function(mandatory, optional, entity_ids) {
		let optional = optional ? optional : [];

		let nodes = [];
		entities = this.component_manager.get_entities_with_components(mandatory);

		let all_components = []
		all_components.concat(mandatory);
		all_components.concat(optional);

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
			nodes.append(n);

		}


	}
	var Node = (function(component_manager) {

		function Node(component_manager) {
			this.component_manager = component_manager;
			return this;
		}

		Node.prototype.init = function(entity_id, components) {
			this.id = entity_id
			this.component_list = Object.keys(components)
			for(let i in component_list){
				c = component_list[i];
				this[c] = components[c];
			}
		}

		Node.prototype.has = function(compo) {
			return this.component_list.indexOf(compo) > -1;
		};

		Node.prototype.add_or_attach = function(comp, comp_data) {
			if(this.has(comp)){
				return;
			}
			if(!this.component_manager.entity_has_component(this.id, comp)) {
				this.component_manager.add_component_to_entity(this.id, comp, comp_data)
			}
			component_list.push(comp);
			this[c] = this.component_manager.get_component_data_for_entity(this.id, comp);

		};

		Node.prototype.add_or_update = function(comp, comp_data) {
			this.component_manager.update_component_for_entity(this.id, comp, comp_data);
			component_list.push(comp);
			this[c] = this.component_manager.get_component_data_for_entity(this.id, comp);
		};

		Node.prototype.remove_component = function(comp) {
			delete this[comp];
			this.components = this.components.filter(function(i){i !== comp});
		};

		Node.prototype.delete_component = function(comp) {
			this.remove_component(comp);
			this.component_manager.remove_component_from_entity(this.id, comp);
		}

		Node.prototype.delete_all_components = function(comp) {
			for(let i = 0; i < this.components.length; i++) {
				this.remove_component(this.components[i]);
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
		return Object.keys(this.component_objects[component_id]);
	}

	ComponentManager.prototype.get_entities_with_components = function(components_list, entity_ids) {
		let intersection = [];

		var entities0 = entity_ids ? entity_ids : [];
		for(let i = 0; i < components_list.length; i++) {
			let entities = this.get_entities_with_component(components_list[0]);
			for(let j = 0; j < entities.length; j++) {
				let entity = entities[j];
				if (entities0.indexOf(entity) > -1) {
					intersection.add(entity);
				} 
			}
		}
		return intersection;
	}

	ComponentManager.prototype.get_component_data_for_entity = function(entity_id, component_id) {
		if(!this.component_objects[component_id]) {
			return null;
		}
		return this.component_objects[component_id][entity_id];
	}

	return new ComponentManager();
});
