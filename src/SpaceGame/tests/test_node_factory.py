'''
Created on 2013-11-24

@author: Nich
'''
import unittest

from objects.component_manager import ComponentManager, ArrayComponentSource
from objects.node_factory import NodeFactoryDB


class TestComponent0(object):
    __compname__ = "test_component0"

    def __init__(self, entity_id, some_string=None):
        self.entity_id = entity_id
        self.some_string = some_string


class TestComponent1(object):
    __compname__ = "test_component1"

    def __init__(self, entity_id, some_string=None):
        self.entity_id = entity_id
        self.some_string = some_string


class TestComponent2(object):
    __compname__ = "test_component2"

    def __init__(self, entity_id, some_string=None):
        self.entity_id = entity_id
        self.some_string = some_string


class TestComponent3(object):
    __compname__ = "test_component3"

    def __init__(self, entity_id, some_string=None):
        self.entity_id = entity_id
        self.some_string = some_string


class TestComponent4(object):
    __compname__ = "test_component4"

    def __init__(self, entity_id, some_string=None):
        self.entity_id = entity_id
        self.some_string = some_string


class TestComponent5(object):
    __compname__ = "test_component5"

    def __init__(self, entity_id, some_string=None):
        self.entity_id = entity_id
        self.some_string = some_string


class Test(unittest.TestCase):

    def setUp(self):

        self.components = {"test_component0": TestComponent0,
                           "test_component1": TestComponent1,
                           "test_component2": TestComponent2,
                           "test_component3": TestComponent3,
                           "test_component4": TestComponent4,
                           "test_component5": TestComponent5,
                           }

        self.component_source = ArrayComponentSource(self.components)

        self.component_manager = ComponentManager([self.component_source])

        # all components
        self.test_entity1 = self.component_manager.create_entity({"test_component0": {"some_string": "E1C0"},
                                                                  "test_component1": {"some_string": "E1C1"},
                                                                  "test_component2": {"some_string": "E1C2"},
                                                                  "test_component3": {"some_string": "E1C3"},
                                                                  "test_component4": {"some_string": "E1C4"},
                                                                  })
        # no components
        self.test_entity2 = self.component_manager.create_entity({})

        # even components
        self.test_entity3 = self.component_manager.create_entity({
            "test_component0": {"some_string": "E3C0"},

            "test_component2": {"some_string": "E3C2"},

            "test_component4": {"some_string": "E3C4"},

        })

        # odd components
        self.test_entity4 = self.component_manager.create_entity({"test_component1": {"some_string": "E4C1"},

                                                                  "test_component3": {"some_string": "E4C3"},


                                                                  })

        # copy of entity1 to make sure that they stay distinct
        self.test_entity5 = self.component_manager.create_entity({"test_component0": {"some_string": "E5C0"},
                                                                  "test_component1": {"some_string": "E5C1"},
                                                                  "test_component2": {"some_string": "E5C2"},
                                                                  "test_component3": {"some_string": "E5C3"},
                                                                  "test_component4": {"some_string": "E5C4"},
                                                                  })

        self.node_factory = NodeFactoryDB(self.component_manager)

    def tearDown(self):
        pass

    def testCreateNodesOneComponent(self):
        node_list = self.node_factory.create_node_list(["test_component2"])
        # We got the right number of nodes
        self.assertEqual(len(node_list), 3)
        # And node 2 isn't in it
        id_list = [node.id for node in node_list]
        self.assertFalse(self.test_entity2.id in id_list)
        # And neither is 4
        self.assertFalse(self.test_entity4.id in id_list)
        # But 5 is
        self.assertTrue(self.test_entity5.id in id_list)
        for node in node_list:
            # And it has the right component objects
            self.assertTrue(node.test_component2)

            # But not any of the others
            with self.assertRaises(AttributeError):
                print(node.test_component1)
                print(node.test_component3)
                print(node.test_component4)
                print(node.test_component5)

    def testCreateNodesTwoComponents(self):
        node_list = self.node_factory.create_node_list(
            ["test_component0", "test_component1"])
        # We got the right number of nodes
        # Only 1 and 5 should pass
        self.assertEqual(len(node_list), 2)
        # And node 2 isn't in it
        id_list = [node.id for node in node_list]
        self.assertFalse(self.test_entity2.id in id_list)
        # And neither is 3 or 4
        self.assertFalse(self.test_entity3.id in id_list)
        self.assertFalse(self.test_entity4.id in id_list)
        # But 1 and 5 are
        self.assertTrue(self.test_entity1.id in id_list)
        self.assertTrue(self.test_entity5.id in id_list)

        # And they have the right component objects
        for node in node_list:
            self.assertIsNotNone(node.test_component0)
            self.assertIsNotNone(node.test_component1)

            # But not any of the others
            with self.assertRaises(AttributeError):
                print(node.test_component2)
                print(node.test_component3)
                print(node.test_component4)

    def testComponentNotExists(self):
        with self.assertRaises(AttributeError):
            self.node_factory.create_node_list(["test_component6"])

    def testComponentNotOnAnyEntity(self):
        node_list = self.node_factory.create_node_list(["test_component5"])
        self.assertEqual([], node_list)

    def test_optional_component(self):
        node_list = self.node_factory.create_node_list(
            ["test_component1", "test_component3"], optional=["test_component2"])
        # We got the right number of nodes
        # Only 1 and 5 should pass
        self.assertEqual(len(node_list), 3)
        # And node 2, 3 isn't in it
        id_list = [node.id for node in node_list]
        self.assertFalse(self.test_entity2.id in id_list)
        self.assertFalse(self.test_entity3.id in id_list)

        # But 1, 4 and 5 are
        self.assertTrue(self.test_entity1.id in id_list)
        self.assertTrue(self.test_entity5.id in id_list)
        self.assertTrue(self.test_entity4.id in id_list)

        # And they have the right component objects
        for node in node_list:
            self.assertIsNotNone(node.test_component1)
            self.assertIsNotNone(node.test_component3)

            # But not any of the others
            with self.assertRaises(AttributeError):
                print(node.test_component0)
                print(node.test_component4)

        # Get all of the nodes with optional component test_component_2
        id_list_2 = [node.id for node in node_list.subset(["test_component2"])]
        print(id_list_2)
        # 1 and 5 qualify but 4 doesn't
        self.assertTrue(self.test_entity1.id in id_list_2)
        self.assertTrue(self.test_entity5.id in id_list_2)
        self.assertFalse(self.test_entity4.id in id_list_2)

    def testOptional(self):
        names = self.node_factory.create_node_list(
            ["test_component2"], optional=["test_component1"])
        print(names)
        self.assertEqual(len(names), 3)
        self.assertEqual(len(names.subset(["test_component1"])), 2)


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
