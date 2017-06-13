
'''
Created on 2014-01-27

@author: Nich
'''
import unittest
from multiprocessing import Queue
from PyMud.Systems.AnnoyingTickSystem import AnnoyingTickSystem
from PyMud.objects.node_factory import NodeFactoryDB
from PyMud.objects.component_manager import ComponentManager


class AnnoyingTickSystemTest(unittest.TestCase):


    def setUp(self):
        component_manager = ComponentManager([])
        node_factory = NodeFactoryDB({}, component_manager, None)
        self.ats = AnnoyingTickSystem(Queue(), node_factory)


    def tearDown(self):
        pass


    #def testGetNodes(self):
    #   self.ats.get_ids() 


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()