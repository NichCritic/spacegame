
'''
Created on 2014-01-27

@author: Nich
'''
import unittest
import os
from description.description import ObjectDescriber
from objects.components import components, db_components
from room.room_components import db_components as db_room_components
from objects.component_manager import ComponentManager, ArrayComponentSource, DBComponentSource
from objects.node_factory import NodeFactoryDB
from Systems.system import System
from Systems.av_event_mixin import AVEventMixin


class TestSystem(System, AVEventMixin):

    def __init__(self, node_factory):
        self.node_factory = node_factory


class AVEventMixinTest(unittest.TestCase):

    def setUp(self):
        all_db = {}
        all_db.update(db_components)
        all_db.update(db_room_components)

        object_db = ArrayComponentSource(all_db)
        object_array = ArrayComponentSource(components)
        component_manager = ComponentManager([object_db, object_array])
        self.node_factory = NodeFactoryDB(component_manager)

        self.test_sys = TestSystem(self.node_factory)

        self.room = self.node_factory.create_new_node({"room": {}})

        self.item = self.node_factory.create_new_node(
            {"location": {"room": self.room.id},
             "speaking": {"text": "foo", "target": None,
                          "format": [([("visibility", 60)], [
                              "{player}'s lips move, but you can't make out what they're saying."])]}})

    def testAVEventAddsEventToRoom(self):
        self.test_sys.av_event(
            self.item, {'player': 'foo'}, self.item.speaking.format)
        self.assertTrue(self.room.entity_has('av_events'))


'''
the av event mixin makes it easier to send av events. It enables one method, 
av_event(), which takes the current node and a format object, and creates an av event in the same location as that node
'''
