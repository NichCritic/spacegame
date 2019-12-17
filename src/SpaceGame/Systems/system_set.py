import time
import logging
# import tracemalloc
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
        # tracemalloc.start()

    def register(self, system):
        self.systems.append(system)

    def process(self):

        for sys in self.systems:
            # before = time.time()
            # logging.info(f"{sys.__class__.__name__}")

            sys.process()

        # s2 = tracemalloc.take_snapshot()

        # comp = s2.statistics('lineno')

        # logging.info("[ Top 5 ]")
        # for stat in comp[:5]:
        #     logging.info(stat)
