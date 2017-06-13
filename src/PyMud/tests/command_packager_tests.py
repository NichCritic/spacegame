'''
Created on 2013-11-18

@author: Nich
'''
import unittest
from PyMud.command.command_packager import CommandPackager
from PyMud.command.commands import verbs

class CommandPackagerTest(unittest.TestCase):

    def setUp(self):
        self.command_packager = CommandPackager(verbs)

    def tearDown(self):
        pass

    def testFindCommand(self):
        cmd_obj = {"verb": "say", "text": "Hello World", "target": "Player1"}
        command_package = self.command_packager.find_command(cmd_obj, {})
        verb_function = verbs["say"]["function"]
        self.assertEqual(command_package.verb_function, verb_function)


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
