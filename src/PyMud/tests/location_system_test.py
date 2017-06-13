'''
Created on 2013-11-30

@author: Nich
'''
import unittest
from PyMud.Systems.LocationSystem import LocationSystem
from PyMud.tests.test_data import create_test_room

class LocationSystemTest(unittest.TestCase):


    def setUp(self):
        pass
        


    def tearDown(self):
        pass

    
    '''
    def testGetObjectsWithinDist(self):
        _, gcr_n, chair1, chair2, node_factory = create_test_room()
        chair_node = node_factory.create_node(chair1.id, ["location"])
        location_system = LocationSystem(node_factory)
        self.assertEqual([chair2], location_system.get_objects_within_dist(chair_node, 30)) 
    '''

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()