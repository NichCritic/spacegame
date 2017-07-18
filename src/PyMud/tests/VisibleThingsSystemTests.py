'''
Created on Nov 1, 2014

@author: Nich
'''
import unittest
from objects.components import components, db_components
from room.room_components import db_components as db_room_components, components as room_components

from startup_scripts import register_systems, setup_commands, setup_db, setup_objects
from Systems.visible_things_system import VisibleThingsSystem


all_db_components = {}
all_db_components.update(db_components)
all_db_components.update(db_room_components)

all_components = {}
all_components.update(components)
all_components.update(room_components)

class Test(unittest.TestCase):


    def setUp(self):
        session_manager = setup_db('sqlite://')
        
        
        with session_manager.get_session() as session:
            avatar_factory, node_factory, object_db, player_factory, account_utils = setup_objects(all_db_components, all_components, session)
        self.node_factory = node_factory    
        self.room = node_factory.create_new_node({
                                      "container":{"parent_id":0},
                                      "av_events":{}
                                      })
        
        self.p1 = node_factory.create_new_node({
                                                "container":{"parent_id":self.room.container.id},
                                                "senses":{},
                                                "location":{"room":self.room.id, "x":0, "y":0, "z":0} 
                                                })
        self.p2 = node_factory.create_new_node({
                                                "container":{"parent_id":self.room.container.id},
                                                "senses":{},
                                                "location":{"room":self.room.id, "x":0, "y":0, "z":0}
                                                
                                                })
        self.p3 = node_factory.create_new_node({
                                                "container":{"parent_id":self.room.container.id},
                                                "senses":{},
                                                "location":{"room":self.room.id, "x":0, "y":0, "z":0}
                                                
                                                })
        
        self.visible_things_system = VisibleThingsSystem(node_factory)
        
        

    def tearDown(self):
        pass


    def testAVEventSystemProcess(self):
        
        
        self.visible_things_system.process()
        
        p1_node = self.node_factory.create_node(self.p1.id, {"visible_objects"})
        p2_node = self.node_factory.create_node(self.p2.id, {"visible_objects"})
        p3_node = self.node_factory.create_node(self.p3.id, {"visible_objects"})
        
        self.assertTrue(p1_node.has("visible_objects"))
        self.assertTrue(p2_node.has("visible_objects"))
        self.assertTrue(p3_node.has("visible_objects"))
         

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testAVEventSystemProcess']
    unittest.main()