import time
import logging
'''
Created on 2014-03-23

@author: Nich
'''


class SystemSet(object):
    '''
    classdocs
    '''

    def __init__(self):
        self.systems = []

    def register(self, system):
        self.systems.append(system)

    def process(self):

        for sys in self.systems:
            # before = time.time()
            # logging.info(f"{sys.__class__.__name__}")
            sys.process()
            # after = time.time()
            

