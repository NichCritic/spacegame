'''
Created on 2013-11-21

@author: Nich
'''
import unittest

from Systems.messanger import MessagePassingModule
from multiprocessing import Queue

class Test(unittest.TestCase):


    def setUp(self):
        self.q = Queue()
        self.mpm = MessagePassingModule(self.q)
        


    def tearDown(self):
        pass


    def testSendAVMessage(self):
        self.mpm.sendAVMessage(msg_type = "player_say", source_id = 1, location=(1, 2, 3), message_templates = {}, text = "Hello World")
        message = self.q.get()
        self.assertEqual(message.__class__.__name__, "AVMessage")
        
        
        
        


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()