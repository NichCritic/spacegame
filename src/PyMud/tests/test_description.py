
'''
Created on 2014-01-27

@author: Nich
'''
import unittest
import os
from description.description import ObjectDescriber
from pynlg.lexicon import XMLLexicon
from objects.components import components, db_components
from room.room_components import db_components as db_room_components
from objects.component_manager import ComponentManager, ArrayComponentSource, DBComponentSource
from objects.node_factory import NodeFactoryDB
import model.base as base


class AnnoyingTickSystemTest(unittest.TestCase):

    def setUp(self):
        all_db = {}
        all_db.update(db_components)
        all_db.update(db_room_components)

        object_db = ArrayComponentSource(all_db)
        object_array = ArrayComponentSource(components)
        component_manager = ComponentManager([object_db, object_array])
        self.node_factory = NodeFactoryDB(component_manager)

        lex = XMLLexicon(os.path.join(os.path.dirname(
            __file__), '../lexicon/default-lexicon.xml'))
        self.od = ObjectDescriber(lex)

    def testSingleItem(self):
        e = self.node_factory.create_new_node({
            "container": {"parent_id": 0},
            "names": {"name": "foo", "identifiers": "foo"},
            "material": {"material_id": 2}
        })

        data = ("material", [[e]])

        self.assertEqual(self.od.describe(data).realize(), "the wooden foo")

    def testTwoItems(self):
        e1 = self.node_factory.create_new_node({
            "container": {"parent_id": 0},
            "names": {"name": "foo", "identifiers": "foo"},
            "material": {"material_id": 2}
        })

        e2 = self.node_factory.create_new_node({
            "container": {"parent_id": 0},
            "names": {"name": "bar", "identifiers": "bar"},
            "material": {"material_id": 1}
        })

        data = ("material", [[e1], [e2]])

        self.assertEqual(self.od.describe(data).realize(),
                         "the wooden foo and the crystal bar")

    def testThreeItems(self):
        e1 = self.node_factory.create_new_node({
            "container": {"parent_id": 0},
            "names": {"name": "foo", "identifiers": "foo"},
            "material": {"material_id": 2}
        })

        e2 = self.node_factory.create_new_node({
            "container": {"parent_id": 0},
            "names": {"name": "bar", "identifiers": "bar"},
            "material": {"material_id": 2}
        })

        e3 = self.node_factory.create_new_node({
            "container": {"parent_id": 0},
            "names": {"name": "baz", "identifiers": "baz"},
            "material": {"material_id": 1}
        })

        data = ("material", [[e1, e2], [e3]])

        self.assertEqual(self.od.describe(data).realize(),
                         "the wooden foo and bar and the crystal baz")

    def testNested(self):
        e1 = self.node_factory.create_new_node({
            "container": {"parent_id": 0},
            "names": {"name": "foo", "identifiers": "foo"},
            "material": {"material_id": 2}
        })

        e2 = self.node_factory.create_new_node({
            "container": {"parent_id": 0},
            "names": {"name": "bar", "identifiers": "bar"},
            "material": {"material_id": 2},
            "close_to": {"n_id": e1.id}
        })

        e3 = self.node_factory.create_new_node({
            "container": {"parent_id": 0},
            "names": {"name": "baz", "identifiers": "baz"},
            "material": {"material_id": 1}
        })

        data = ("close_to", [[e2], [("material", [[e1], [e3]])]])

        expect = "the bar is close to the foo. The wooden foo and the crystal baz"


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
