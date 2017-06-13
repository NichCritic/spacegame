'''
Created on 2013-11-15

@author: Nich
'''

class RoomFactory():
    
    def __init__(self, component_manager):
        self.component_manager = component_manager
        
    def create_room(self, name, width, length, height, container_id):
        room = self.component_manager.create_entity({}).id
        self.component_manager.add_component_to_object("names", room, data={"name":name})
        self.component_manager.add_component_to_object("space", room, data={"width":width, "length":length, "height":height})
        self.component_manager.add_component_to_object("container", room, data={"parent_id":container_id})
        self.component_manager.add_component_to_object("type", room, data={"type":"room"})
        self.component_manager.add_component_to_object("room", room)
        
        return room
        
        
        
       

        
        

   
    
    