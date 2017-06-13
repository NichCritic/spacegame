'''
Created on 2013-03-13

@author: Nich
'''
from PyMud.graph.graphnodes import *
from PyMud.objects.baseobject import Entity
from PyMud.objects.component_manager import ComponentManager 
#import PyMud.data_cache as data_cache

from collections import defaultdict
#|0|   ____
#|||  / 0  \
#|||_// | \ \   N
#|0-_0 -0- 0| W   E
#||| \\ | / /   S
#|||  \_0__/
#|0| 

#This is just the display graph. The graph that allows from movement needs to be distinct. 
#In that case, do we need the links at all?

def create_common_room(data_cache):


    hallway = data_cache.add_room(Room("gryffindore_corridore"))
    hall_n = data_cache.add_location(hallway.add_location("north"))
    hall_m = data_cache.add_location(hallway.add_location("middle"))
    hall_s = data_cache.add_location(hallway.add_location("south"))
    
    Link(hall_n, hall_m)
    Link(hall_m, hall_s)
    
    
    gryffindore_common_room = data_cache.add_room(Room("gryffindore_common_room"))
    
    gcr_n = data_cache.add_location(gryffindore_common_room.add_location("north"))
    gcr_e = data_cache.add_location(gryffindore_common_room.add_location("east"))
    gcr_w = data_cache.add_location(gryffindore_common_room.add_location("west"))
    gcr_s = data_cache.add_location(gryffindore_common_room.add_location("south"))
    gcr_m = data_cache.add_location(gryffindore_common_room.add_location("middle"))
    
    Link(gcr_n, gcr_m)
    Link(gcr_n, gcr_e)
    Link(gcr_n, gcr_w)
    Link(gcr_e, gcr_m)
    Link(gcr_e, gcr_s)
    Link(gcr_w, gcr_m)
    Link(gcr_w, gcr_s)
    Link(gcr_s, gcr_m)
    
    #Replace with global?
    comp_man = ComponentManager()
    chair1 = data_cache.add_object(Entity(comp_man))
    chair2 = data_cache.add_object(Entity(comp_man))
    comp_man.add_component_to_object("description_component", chair1)
    comp_man.add_component_to_object("description_component", chair2)
    comp_man.add_component_to_object("type_component", chair1)
    comp_man.add_component_to_object("type_component", chair2)
    chair1.name = "chair1"
    chair2.name = "chair2"
    chair1.type = "chair"
    chair2.type = "chair"
    chair1.description = "A simple chair"
    chair2.description = "A simple chair"
    
    
    
    gcr_n.add_object(chair1)
    gcr_w.add_object(chair2)

    return data_cache

def aggregate_by_contents(start_loc):
    contents = defaultdict(set)
    for loc in walk_tree_bf(start_loc):
        if not loc.contents:
            contents["nothing"].add(loc)
        else:
            #print(loc.contents)
            for _, c in loc.contents.items():
                contents[c.type].add(loc)
    return contents

def display_room(start_loc):
    #aggregate by contents
    contents = aggregate_by_contents(start_loc)
    
    for k, v in contents.items():
        print(k +", "+(str(v)))
    
        


if __name__ == '__main__':
    pass
    #display_room(gcr_s)
    
    