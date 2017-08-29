'''
Created on 2014-02-01

@author: Nich
'''
import unittest
import model.base as base
from objects.component_manager import ArrayComponentSource, DBComponentSource, ComponentManager
from objects.node_factory import NodeFactoryDB
from objects.components import components, db_components
from room.room_components import db_components as db_room_components, components as room_components
from room.room import RoomFactory


class Test(unittest.TestCase):

    def setUp(self):
        self.engine = base.engine('sqlite://', echo=True)
        self.Session = base.create_sessionmaker(self.engine)
        base.Base.metadata.create_all(self.engine)

        all_db_components = {}
        all_db_components.update(db_components)
        all_db_components.update(db_room_components)

        all_components = {}
        all_components.update(components)
        all_components.update(room_components)

        self.array_component = ArrayComponentSource(all_components)
        self.component_object = DBComponentSource(all_db_components)
        self.comp_manager = ComponentManager(
            [self.component_object, self.array_component])
        self.node_factory = NodeFactoryDB(self.comp_manager)

        self.session = self.Session()
        self.component_object.set_session(self.session)

        self.chair1 = self.comp_manager.create_entity({
            "names": {"name": "chair1"},
            "type": {"type": "chair1"},
            "network_messages": None
        })
        self.chair2 = self.comp_manager.create_entity({
            "names": {"name": "chair1"},
            "type": {"type": "chair1"},
            "creating": {'new_name': 'foo', 'format': 'bar'}
        })
        self.chair3 = self.comp_manager.create_entity({
            "names": {"name": "chair1"},
            "type": {"type": "chair1"},
            "network_messages": None

        })

        room_factory = RoomFactory(self.comp_manager)
        self.test_room = room_factory.create_room("test", 0, 20, 20, 20)
        self.session.commit()

    def tearDown(self):
        self.session.commit()
        self.session.close()
        base.Base.metadata.drop_all(self.engine)
        pass

    def testCreate(self):
        names = self.node_factory.create_node_list(["names"])
        print(names)
        self.assertEqual(len(names), 4)

        names = self.node_factory.create_node_list(["names", "creating"])
        self.assertEqual(len(names), 1)
        print(names)

    def testRoom(self):
        print("------------TEST ROOM--------------")
        room = self.node_factory.create_node(self.test_room, ["names"])
        print(room.names.name)
        self.assertEqual(room.names.name, "test")
        print("--------END TEST ROOM--------------")

    def testOptional(self):
        names = self.node_factory.create_node_list(
            ["names"], optional=["creating"])
        print(names)
        self.assertEqual(len(names), 4)
        self.assertEqual(len(names.subset(["creating"])), 1)


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
