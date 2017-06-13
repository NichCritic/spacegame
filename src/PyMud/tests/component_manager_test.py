'''
Created on 2013-11-24

@author: Nich
'''
import unittest

from PyMud.objects.component_manager import ComponentManager, ArrayComponentSource
from PyMud.objects.node_factory import NodeFactoryDB

class TestComponent0(object):
    __compname__ = "test_component0"
    
    def __init__(self, entity_id, some_string = None):
        self.entity_id = entity_id
        self.some_string = some_string
        
class TestComponent1(object):
    __compname__ = "test_component1"
    
    def __init__(self, entity_id, some_string = None):
        self.entity_id = entity_id
        self.some_string = some_string
        
        
class TestComponent2(object):
    __compname__ = "test_component2"
    
    def __init__(self, entity_id, some_string = None):
        self.entity_id = entity_id
        self.some_string = some_string
        
class TestComponent3(object):
    __compname__ = "test_component3"
    
    def __init__(self, entity_id, some_string = None):
        self.entity_id = entity_id
        self.some_string = some_string
        
        
class TestComponent4(object):
    __compname__ = "test_component4"
    
    def __init__(self, entity_id, some_string = None):
        self.entity_id = entity_id
        self.some_string = some_string
        
class TestComponent5(object):
    __compname__ = "test_component5"
    
    def __init__(self, entity_id, some_string = None):
        self.entity_id = entity_id
        self.some_string = some_string

class Test(unittest.TestCase):

    

    def setUp(self):
        
        
        
        self.components1 = {"test_component0":TestComponent0,
                           "test_component1":TestComponent1,
                           "test_component2":TestComponent2,
                           "test_component3":TestComponent3,
                           }
        self.components2 =  {
                           "test_component4":TestComponent4,
                           "test_component5":TestComponent5,
                           }
        
        
        self.component_source1 = ArrayComponentSource(self.components1)
        self.component_source2 = ArrayComponentSource(self.components2)
        
        self.component_manager = ComponentManager([self.component_source1, self.component_source2])
        
        #all components
        self.test_entity1 = self.component_manager.create_entity({"test_component0":{"some_string":"E1C0"},
                                                                  "test_component1":{"some_string":"E1C1"},
                                                                  "test_component2":{"some_string":"E1C2"},
                                                                  "test_component3":{"some_string":"E1C3"},
                                                                  "test_component4":{"some_string":"E1C4"},
                                                                  })
        #no components
        self.test_entity2 = self.component_manager.create_entity({})
        
        #even components
        self.test_entity3 = self.component_manager.create_entity({
                                                                  "test_component0":{"some_string":"E3C0"},
                                                                  
                                                                  "test_component2":{"some_string":"E3C2"},
                                                                  
                                                                  "test_component4":{"some_string":"E3C4"},
                                                                  
                                                                  })
        
        
        #odd components
        self.test_entity4 = self.component_manager.create_entity({"test_component1":{"some_string":"E4C1"},
                                                                  
                                                                  "test_component3":{"some_string":"E4C3"},
                                                                
                                                                  
                                                                  })
        
        #copy of entity1 to make sure that they stay distinct
        self.test_entity5 = self.component_manager.create_entity({"test_component0":{"some_string":"E5C0"},
                                                                  "test_component1":{"some_string":"E5C1"},
                                                                  "test_component2":{"some_string":"E5C2"},
                                                                  "test_component3":{"some_string":"E5C3"},
                                                                  "test_component4":{"some_string":"E5C4"},
                                                                  })
        
        


    def tearDown(self):
        pass


    def testAddGetComponent(self):
        self.component_manager.add_component_to_object("test_component0", self.test_entity2.id, {"some_string":"test1"})
        comp = self.component_manager.get_component(self.test_entity2.id, "test_component0")
        self.assertEqual(comp.some_string, "test1")
        
        
    def testGetSupportedSubset(self):
        self.assertEqual(sorted(["test_component0", "test_component3" ]), sorted(self.component_source1.get_supported_subset(["test_component0", "test_component6", "test_component3", "test_component7"])))
        
    def testHas(self):
        self.assertTrue(self.component_manager.has_component("test_component0"))
        self.assertTrue(self.component_manager.has_component("test_component1"))
        self.assertTrue(self.component_manager.has_component("test_component2"))
        self.assertTrue(self.component_manager.has_component("test_component3"))
        self.assertTrue(self.component_manager.has_component("test_component4"))
        self.assertTrue(self.component_manager.has_component("test_component5"))
        self.assertFalse(self.component_manager.has_component("test_component6"))
        
    def testGetEntitiesForComponent(self):
        entities = [self.component_manager.create_entity({}) for _ in range(10)]
        even_entities = []
        odd_entities = []
        for i, e in enumerate(entities):
            counter = i%2
            self.component_manager.add_component_to_object("test_component"+str(0+counter), e.id, None)
            self.component_manager.add_component_to_object("test_component"+str(2+counter), e.id, None)
            self.component_manager.add_component_to_object("test_component"+str(4+counter), e.id, None)
            if counter == 0:
                even_entities.append(e.id)
            else:
                odd_entities.append(e.id)
        
        print(entities)
        print(sorted(self.component_manager.get_entities_for_component("test_component2")))
        print(even_entities)
        self.assertTrue(set(even_entities).issubset(set(self.component_manager.get_entities_for_component("test_component2"))))
        self.assertTrue(set(odd_entities).issubset(set(self.component_manager.get_entities_for_component("test_component5"))))


    def test_remove_component(self):
        entity1 = self.component_manager.create_entity({})
        self.component_manager.add_component_to_object("test_component0", entity1.id, {"some_string":"test1"})
        comp = self.component_manager.get_component(entity1.id, "test_component0")
        self.assertEqual(comp.some_string, "test1")
        self.component_manager.remove_component("test_component0", entity1.id)
        with self.assertRaises(AttributeError):
            self.component_manager.get_component(entity1.id, "test_component0")
        
        


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()