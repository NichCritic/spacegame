'''
Created on 2014-03-09

@author: Nich
'''
import unittest
from PyMud.objects.component_manager import ArrayComponentSource

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

class TestArrayComponentSource(unittest.TestCase):


    def setUp(self):
        self.components = {"test_component0":TestComponent0,
                           "test_component1":TestComponent1,
                           "test_component2":TestComponent2,
                           "test_component3":TestComponent3,
                           "test_component4":TestComponent4,
                           "test_component5":TestComponent5,
                           }
        self.component_source = ArrayComponentSource(self.components)
        self.entity1 = self.component_source.create_entity()
        self.entity2 = self.component_source.create_entity()
        

    def tearDown(self):
        pass


    def testAddGetComponent(self):
        self.component_source.add_component_to_object("test_component0", self.entity1.id, {"some_string":"test1"})
        comp = self.component_source.get_component(self.entity1.id, "test_component0")
        self.assertEqual(comp.some_string, "test1")
        
        
    def testGetSupportedSubset(self):
        self.assertEqual(sorted(["test_component0", "test_component3" ]), sorted(self.component_source.get_supported_subset(["test_component0", "test_component6", "test_component3", "test_component7"])))
        
    def testHas(self):
        self.assertTrue(self.component_source.has("test_component0"))
        self.assertTrue(self.component_source.has("test_component1"))
        self.assertTrue(self.component_source.has("test_component2"))
        self.assertTrue(self.component_source.has("test_component3"))
        self.assertTrue(self.component_source.has("test_component4"))
        self.assertTrue(self.component_source.has("test_component5"))
        self.assertFalse(self.component_source.has("test_component6"))
        
    def testGetEntitiesForComponent(self):
        entities = [self.component_source.create_entity() for _ in range(10)]
        even_entities = []
        odd_entities = []
        for i, e in enumerate(entities):
            counter = i%2
            self.component_source.add_component_to_object("test_component"+str(0+counter), e.id, None)
            self.component_source.add_component_to_object("test_component"+str(2+counter), e.id, None)
            self.component_source.add_component_to_object("test_component"+str(4+counter), e.id, None)
            if counter == 0:
                even_entities.append(e.id)
            else:
                odd_entities.append(e.id)
        
        
        self.assertEqual(sorted(even_entities), sorted(self.component_source.get_entities_for_component("test_component2")))
        self.assertEqual(sorted(odd_entities), sorted(self.component_source.get_entities_for_component("test_component5")))


    def test_remove_component(self):
        entity1 = self.component_source.create_entity()
        self.component_source.add_component_to_object("test_component0", entity1.id, {"some_string":"test1"})
        comp = self.component_source.get_component(entity1.id, "test_component0")
        self.assertEqual(comp.some_string, "test1")
        self.component_source.remove_component(entity1.id, "test_component0")
        with self.assertRaises(AttributeError):
            self.component_source.get_component(entity1.id, "test_component0")
            
            
    
        
        
        

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()