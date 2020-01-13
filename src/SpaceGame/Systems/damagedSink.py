from Systems.system import System
import math
import logging
import time


class DamagedSink(System):

    mandatory = ["damaged"]
    optional = []
    handles = ["damaged"]

    def __init__(self, node_factory):
        self.node_factory = node_factory

    def handle(self, node):
        pass