'''
Created on 2013-11-17

@author: Nich
'''
 
from PyMud.objects.baseobject import Entity
from PyMud.objects.node_factory import NodeFactoryDB
from PyMud.room.room import RoomFactory
from PyMud.objects.component_manager import ComponentManager
from PyMud.objects.components import components
from PyMud.room.room_components import db_components as db_room_components



def create_test_room(comp_manager, node_factory):
    #|0|   ____
    #|||  / 0  \
    #|||_// | \ \   N
    #|0-_0 -0- 0| W   E
    #||| \\ | / /   S
    #|||  \_0__/
    #|0| 
    
    all_components = {}
    all_components.update(components)
    all_components.update(db_room_components)
    
    
    
    room_factory = RoomFactory(comp_manager)
    
    
    hallway = room_factory.create_room()
    hall_node = node_factory.create_node(hallway.id, ["locations",])
    
    
   
    
   
   
    
    
    gryffindore_common_room = room_factory.create_room()
    gcr_node = node_factory.create_node(gryffindore_common_room.id, ["locations"])
   
    
    
    
    
    
    
    
   
    
    
    
    
    return gryffindore_common_room, node_factory