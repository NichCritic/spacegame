'''
Created on Nov 1, 2014

@author: Nich
'''
import unittest
from objects.components import components, db_components
from room.room_components import db_components as db_room_components, components as room_components

from startup_scripts import register_systems, setup_commands, setup_db, setup_objects
from Systems.creating_system import CreatingSystem

all_db_components = {}
all_db_components.update(db_components)
all_db_components.update(db_room_components)

all_components = {}
all_components.update(components)
all_components.update(room_components)


class Test(unittest.TestCase):

    def setUp(self):
        session_manager = setup_db('sqlite://')

        with session_manager.get_session() as session:
            avatar_factory, node_factory, object_db, player_factory, account_utils = setup_objects(
                all_db_components, all_components, session)
        self.node_factory = node_factory
        self.room = node_factory.create_new_node({
            "container": {"parent_id": 0},
            "av_events": {}
        })

        self.p1 = node_factory.create_new_node({
            "container": {"parent_id": self.room.container.id},
            "location": {"room": self.room.id}
        })

        self.creating_system = CreatingSystem(node_factory)

    def tearDown(self):
        pass

    def testCreatingSystemProcess(self):

        self.p1.add_or_attach_component(
            "creating", {"format": '', "new_name": "foo"})
        self.creating_system.process()

    def testCreatedEntityHasSameParent(self):
        self.p1.add_or_attach_component(
            "creating", {"format": '', "new_name": "foo"})
        self.creating_system.process()
        self.assertEqual(len(self.room.container.children), 2)


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testAVEventSystemProcess']
    unittest.main()
