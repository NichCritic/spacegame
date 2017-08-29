'''
Created on 2013-11-08

@author: Nich
'''
import unittest
import command.commands as commands


from objects.component_manager import ComponentManager, ArrayComponentSource
from objects.node_factory import NodeFactoryDB
from objects.components import components

    

class TestCommands(unittest.TestCase):


    def setUp(self):
        self.component_source = ArrayComponentSource(components)
        self.component_manager = ComponentManager([self.component_source])
        self.node_factory = NodeFactoryDB(self.component_manager)
        
        self.player = self.component_manager.create_entity({})
        

    def tearDown(self):
        pass


    def testSay(self):
        player_node = self.node_factory.create_node(self.player.id, [])
        message = "hello world"
        commands.say(message, player_node)
        
        self.assertTrue(player_node.has("speaking"))
        self.assertEqual(player_node.speaking.text, "hello world")
        
        
        
        
    

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()