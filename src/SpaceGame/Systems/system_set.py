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

        system_times = {}
        # before = time.time()
        # logging.info("--------------------------------")
        for sys in self.systems:
            # logging.info(f"{sys.__class__.__name__}")
            before_s = time.time()
            sys.process()
            after_s = time.time()
            system_times[sys.__class__.__name__] = after_s - before_s

        # after = time.time()
        # logging.info(f"All systems ran in {after-before}s")
        # logging.info("Slow systems:")

        # for n, t in reversed(sorted(system_times.items(), key = lambda x: x[1])[-5:]):
        #     logging.info(f"{n}: {t}s")
        # s2 = tracemalloc.take_snapshot()

        # comp = s2.statistics('lineno')

        # logging.info("[ Top 5 ]")
        # for stat in comp[:5]:
        #     logging.info(stat)
