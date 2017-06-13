'''
Created on 2013-11-17

@author: Nich
'''

import logging


        
class PlayerMock():
    def __init__(self, name):
        self.name = name
        
    def __str__(self):
        return self.name