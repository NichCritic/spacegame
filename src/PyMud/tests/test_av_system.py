'''
Created on 2014-02-01

@author: Nich
'''
import unittest
import model.base as base
from objects.components import components, db_components
from room.room_components import db_components as db_room_components, components as room_components
from startup_scripts import setup_objects, setup_db
from objects.components import components
from Systems.AVEventSystem import AVEventExitPropagationSystem
from Systems.system_set import DBSystemSet


class Test(unittest.TestCase):

    def setUp(self):
        all_db_components = {}
        all_db_components.update(db_components)
        all_db_components.update(db_room_components)

        all_components = {}
        all_components.update(components)
        all_components.update(room_components)

        self.session_manager = setup_db('sqlite://')

        with self.session_manager.get_session() as session:
            avatar_factory, node_factory, object_db, player_factory, account_utils = setup_objects(
                all_db_components, all_components, session)

        self.node_factory = node_factory
        self.system_set = DBSystemSet(object_db, self.session_manager)
        self.av_prop = AVEventExitPropagationSystem(node_factory)
        self.system_set.register(self.av_prop)

    def test_get_nodes(self):
        e = self.node_factory.create_new_node({})
        e.add_or_attach_component('av_events', None)

        with self.session_manager.get_session() as session:
            self.system_set.db_components.set_session(session)
            # import pdb
            # pdb.set_trace()
            nodes = self.av_prop.get_nodes()
        # Just av_events shouldn't be enough
        self.assertEqual(len(nodes), 0)


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
