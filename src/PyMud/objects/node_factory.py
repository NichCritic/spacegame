'''
Created on 2013-11-23

@author: Nich
'''


from contextlib import contextmanager

class NodeFactoryDB(object):
    
    def __init__(self, component_manager):
        
        self.component_manager = component_manager
    

    def create_new_node(self, entity_spec):
        components_list = entity_spec.keys()
        entity = self.component_manager.create_entity(entity_spec)
        return self.create_node(entity.id, components_list)   

    def create_node_list(self, component_list, optional=None):
        '''
            Create a list of all entities matching the given components. 
            Return a list of Node objects, which contain references to the given components
        '''
        if optional == None:
            optional = []
        
        entities = self.component_manager.get_entities_with_components(component_list)
        
        
        #feels strange to do this again
        components = {}
        
        for comp_name in component_list+optional:
            comps = self.component_manager.get_components_for_entities(entities, comp_name)
            
            for c in comps:
                if not c.entity_id in components:
                    components[c.entity_id] = {}
                components[c.entity_id][comp_name] = c
        
        
        
                
        
            
        results = NodeList([Node(e, components[e], self.component_manager) for e in entities])
        
        return results
        
    '''
    @contextmanager   
    def create_node_list_session(self, component_list):
        
        session = self.Session()
        
        try:
            yield session, self.create_node_list(component_list, session)
        except:
            raise
        
        finally:
            session.commit()
            session.close()
            
    '''
            
    def create_node(self, entity_id, component_list):
        components = {}
            
        for comp_name in component_list:
            c= self.component_manager.get_components_for_entities([entity_id], comp_name)
            if len(c) > 0:
                components[comp_name] = c[0]
            else:
                raise AttributeError("No nodes found with comp_name "+comp_name+" and entity_id "+entity_id)
        
            
        result = Node(entity_id, components, self.component_manager)
        return result
    '''    
    @contextmanager
    def create_node_session(self, entity_id, component_list):
        #feels strange to do this again
        session = self.Session()
        try:
            yield session, self.create_node(entity_id, component_list, session)
        except:
            raise
        finally:
            session.commit()
            session.close()  
        
    '''                 



        
            
            
            
class Node(object):
    def __init__(self, entity_id, components, component_manager):
        self.id = entity_id
        self.components = components
        self.component_manager = component_manager
        
        
    def __getattr__(self, arg):
        if arg == "components":
            raise AttributeError(arg)
        if arg in self.components:
            return self.components[arg]
        else:
            raise AttributeError(arg)
        
    def has(self, component_name):
        return component_name in self.components
    
    def add_or_attach_component(self, component_name, data):
        if self.component_manager.entity_has_component(self.id, component_name):
            self.components[component_name] = self.component_manager.get_component(self.id, component_name)
        else:
            self.add_component(component_name, data)
        
        
    
    def add_component(self, component_name, data):
        self.component_manager.add_component_to_object(component_name, self.id, data)
        self.components[component_name] = self.component_manager.get_component(self.id, component_name)
        
    def remove_component(self, component_name):
        self.component_manager.remove_component(component_name, self.id)
    
    
        
    
class NodeList(list):
    def subset(self, component_list):
        return NodeList([n for n in self if all([n.has(c) for c in component_list])])   
        
        
        
        

