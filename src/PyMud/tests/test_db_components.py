'''
Created on 2014-02-01

@author: Nich
'''
import unittest
import PyMud.model.base as base
from PyMud.objects.component_manager import ComponentManager, DBComponentSource
from PyMud.objects.components import db_components
from PyMud.room.room_components import db_components as db_room_components



class Test(unittest.TestCase):


    def setUp(self):
        self.engine = base.engine('sqlite://', echo = False)
        self.Session = base.create_sessionmaker(self.engine)
        base.Base.metadata.create_all(self.engine)
        
        all_components = {}
        all_components.update(db_components)
        all_components.update(db_room_components)
        
        self.component_object = DBComponentSource(all_components)
        self.component_manager = ComponentManager([self.component_object])
        
        


    def tearDown(self):
        base.Base.metadata.drop_all(self.engine)
        pass


    def testCreateDBtable(self):
        session = self.Session()
        self.component_object.set_session(session)
        
        e = self.component_manager.create_entity({})
        self.component_manager.add_component_to_object("location", e.id, None)
        
        session.commit()
        session.close()
        
    def testGetComponent(self):
        session = self.Session()
        self.component_object.set_session(session)
        e = self.component_manager.create_entity({})
        self.component_manager.add_component_to_object("temperature", e.id, {"temperature":50})
        
        temperature = self.component_manager.get_component(e.id, "temperature")
        self.assertEqual(temperature.temperature, 50)
        session.commit()
        session.close()
        
    def testGetEntitiesForComponent(self):
        session = self.Session()
        self.component_object.set_session(session)
        e = self.component_manager.create_entity({})
        self.component_manager.add_component_to_object("temperature", e.id, {"temperature":50})
        
        entities = self.component_manager.get_entities_for_component("temperature")
        print(entities)
        self.assertEqual(entities[0], e.id)
        
        session.commit()
        session.close()
        
    
    
        
    
        


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()