'''
Created on Nov 1, 2014

@author: Nich
'''
import unittest
from PyMud.objects.components import components, db_components
from PyMud.room.room_components import db_components as db_room_components, components as room_components

from PyMud.startup_scripts import register_systems, setup_commands, setup_db, setup_objects
from PyMud.Systems.AVEventSystem import AVEventSystem
from PyMud.Systems.AVEvent import AVEvent

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
                                                "container":{"parent_id":self.room.container.id}
                                                
                                                })
        self.p2 = node_factory.create_new_node({
                                                "container":{"parent_id":self.room.container.id}
                                                
                                                })
        self.p3 = node_factory.create_new_node({
                                                "container":{"parent_id":self.room.container.id}
                                                
                                                })
        
        self.av_event_system = AVEventSystem(node_factory)
        
        self.message_templates = [([("loudness", 50), ("targeted",), ("is_caller",)], ['You say to {target}, "{text}".']),
                             ([("loudness", 50), ("targeted",), ("is_target",)], ['{player} says to you, "{text}".']),
                             ([("loudness", 50), ("targeted",),],                 ['{player} says to {target}, "{text}".']),
                             ([("loudness", 50), ("is_caller",)],               ['You say, "{text}".']),
                             ([("loudness", 50)],                              ['{player} says, "{text}".']),
                             ([("visibility", 60), ("is_caller")],              ["You can't hear your own voice!"]),          
                                                    
                             ([("visibility", 60), ("is_caller")],             ["{player}'s lips move, but you can't make out what they're saying."])
                             ]

    def tearDown(self):
        pass


    def testAVEventSystemProcess(self):
        event1 = AVEvent("test_event1", "test_event1", None, self.p1.id, self.message_templates)  
        event2 = AVEvent("test_event2", "test_event2", None, self.p1.id, self.message_templates)
        event3 = AVEvent("test_event3", "test_event3", None, self.p1.id, self.message_templates)

        self.room.av_events.events.append(event1)
        self.room.av_events.events.append(event2)
        self.room.av_events.events.append(event3)
        
        self.av_event_system.process()
        
        p1_node = self.node_factory.create_node(self.p1.id, {"av_messages"})
        p2_node = self.node_factory.create_node(self.p2.id, {"av_messages"})
        p3_node = self.node_factory.create_node(self.p3.id, {"av_messages"})
        
        self.assertTrue(p1_node.has("av_messages"))
        self.assertTrue(p2_node.has("av_messages"))
        self.assertTrue(p3_node.has("av_messages"))
         

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testAVEventSystemProcess']
    unittest.main()