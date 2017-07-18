'''
Created on 2014-03-22

@author: Nich
'''


import unittest
import model.base as base
from objects.component_manager import ArrayComponentSource, DBComponentSource, ComponentManager
from objects.node_factory import NodeFactoryDB
from objects.components import components, db_components
from room.room_components import db_components as db_room_components, components as room_components
from room.room import RoomFactory
from Systems.RoomDescriptionSystem import NetworkDescriptionSystem, DescriptionSystem

class Test(unittest.TestCase):


    def setUp(self):
        self.engine = base.engine('sqlite://', echo=True)
        self.Session = base.create_sessionmaker(self.engine)
        base.Base.metadata.create_all(self.engine)
        
        all_db_components = {}
        all_db_components.update(db_components)
        all_db_components.update(db_room_components)
        
        all_components = {}
        all_components.update(components)
        all_components.update(room_components)
        
        self.array_component = ArrayComponentSource(all_components)
        self.component_object = DBComponentSource(all_db_components)
        self.comp_manager = ComponentManager([self.component_object, self.array_component])
        self.node_factory = NodeFactoryDB(self.comp_manager)
        
        self.session = self.Session()
        self.component_object.set_session(self.session)
        
        room_factory = RoomFactory(self.comp_manager)
        self.test_room = room_factory.create_room("test", 0, 20, 20, 20)
        
        
        self.chair1 = self.comp_manager.create_entity({
                                         "names": {"name":"chair1"},
                                         "description":{"description":"A simple chair"},
                                         "type":{"type":"chair1"},
                                         "location":{"room":self.test_room, "x":3, "y":3, "z":3},
                                         "network_messages":None                                     
                                         })
        self.chair2 = self.comp_manager.create_entity({
                                         "names": {"name":"chair1"},
                                         "description":{"description":"A simple chair"},
                                         "location":{"room":self.test_room, "x":3, "y":3, "z":3},
                                         "type":{"type":"chair1"},
                                         
                                         
                                         })
        self.chair3 = self.comp_manager.create_entity({
                                         "names": {"name":"chair1"},
                                         "description":{"description":"A simple chair"},
                                         "location":{"room":self.test_room, "x":3, "y":3, "z":3},
                                         "type":{"type":"chair1"},
                                         "network_messages":None
                                         
                                         })
        
        
        
        
        self.session.commit()
        self.description_system = DescriptionSystem(self.node_factory)
        self.net_desc_sys = NetworkDescriptionSystem(self.node_factory, self.description_system)

    def tearDown(self):
        pass


    def testProcess(self):
        self.comp_manager.create_entity({
                                         "looking":None, 
                                         "location":{"room":self.test_room, "x":0 ,"y":0,"z":0}
                                        
                                         
                                         })
        
        self.net_desc_sys.process()
        
        


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()