'''
Created on 2013-11-08

@author: Nich
'''
import unittest
from command.command_token_matcher import CommandTokenMatcher, build_grammar


class Foo(object):
    def __init__(self, names):
        self.names = names

class Test(unittest.TestCase):


    def setUp(self):
        
        
        self.command_context = {"names":Foo(["julie", "alice", "archway"])}
        self.command_grammar = build_grammar(self.command_context["names"].names)
        self.command_matcher = CommandTokenMatcher(self.command_context)

    def tearDown(self):
        pass


    def testgrammar(self):
        #print(self.command_grammar.parse("test"))
        self.assertTrue(self.command_grammar.parse("say hello world"))
        self.assertTrue(self.command_grammar.parse("say to alice hello world"))
        self.assertTrue(self.command_grammar.parse("look"))
        self.assertTrue(self.command_grammar.parse("look at julie"))
        self.assertTrue(self.command_grammar.parse("move to alice"))
        self.assertTrue(self.command_grammar.parse("quickly move to alice"))
        self.assertTrue(self.command_grammar.parse("move through archway"))
    
    
    
    def testMatcher(self):   
        self.assertEqual(self.command_matcher.map_command("say hello world",self.command_context), {"text":"hello world", "verb":"say"})
        self.assertEqual(self.command_matcher.map_command("say to julie hello world", self.command_context), {'verb': 'say', 'targets':['julie'], 'text':'hello world', "p_type":"to"})
        self.assertEqual(self.command_matcher.map_command("look", self.command_context), {'verb': 'look' })
        self.assertEqual(self.command_matcher.map_command("look julie", self.command_context), {'verb': 'look', 'targets':["julie"]})
        self.assertEqual(self.command_matcher.map_command("look at julie", self.command_context), {'verb': 'look', 'targets':["julie"], "p_type":"at"})
        self.assertEqual(self.command_matcher.map_command("move to alice", self.command_context), {'verb': 'move', 'targets':["alice"], "p_type":"to"})
        self.assertEqual(self.command_matcher.map_command("move through archway", self.command_context), {'verb': 'move', 'p_type':'through', 'targets':["archway"]})
        
        


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testgrammar']
    unittest.main()