
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
from Systems.ProjectileSystem import ProjectileSystem, ProjectileDodgingSystem


class ProjectileDodgingSystemTest(unittest.TestCase):

    def setUp(self):
        all_db = {}
        all_db.update(db_components)
        all_db.update(db_room_components)

        object_db = ArrayComponentSource(all_db)
        object_array = ArrayComponentSource(components)
        component_manager = ComponentManager([object_db, object_array])
        self.node_factory = NodeFactoryDB(component_manager)

        self.proj_sys = ProjectileSystem(self.node_factory)
        self.dodge_sys = ProjectileDodgingSystem(self.node_factory)

    def testDodgeCancelsOutProjectile(self):
        node = self.node_factory.create_new_node({'projectile': {'on_hit': lambda: None, 'args': {}},
                                                  'dodging': {"format": {}}})
        self.dodge_sys.handle(node, 0)

        self.assertFalse(node.has('projectile'))
        self.assertFalse(node.has('dodging'))

    def testDodgeTimesOutAfterSpecifiedTime(self):
        node = self.node_factory.create_new_node(
            {'dodging': {'format': '', 'timeout': 60}})

        self.dodge_sys.handle(node, 10000)
        self.assertTrue(node.has('dodging'))
        self.dodge_sys.handle(node, 10030)
        self.assertTrue(node.has('dodging'))
        self.dodge_sys.handle(node, 10070)
        self.assertFalse(node.has('dodging'))


class ProjectileSystemTest(unittest.TestCase):

    def setUp(self):
        all_db = {}
        all_db.update(db_components)
        all_db.update(db_room_components)

        object_db = ArrayComponentSource(all_db)
        object_array = ArrayComponentSource(components)
        component_manager = ComponentManager([object_db, object_array])
        self.node_factory = NodeFactoryDB(component_manager)

        self.proj_sys = ProjectileSystem(self.node_factory)

    def testProcess(self):
        self.proj_sys.process()

    def testGetsNodes(self):
        node = self.node_factory.create_new_node(
            {'projectile': {'on_hit': lambda: None, 'args': {}}})
        # import pdb
        # pdb.set_trace()
        num = len(self.proj_sys.get_nodes())
        self.assertEqual(num, 1)

    def testProcessingHandlesProjectileAfterTimeout(self):
        node = self.node_factory.create_new_node(
            {'projectile': {'on_hit': lambda: None, 'args': {}, 'timeout': 60}})
        self.proj_sys.handle(node, 1000000)
        self.assertTrue(node.entity_has('projectile'))
        self.proj_sys.handle(node, 1000050)
        self.assertTrue(node.entity_has('projectile'))
        self.proj_sys.handle(node, 1000100)
        self.assertFalse(node.entity_has('projectile'))

    def testProcessingCallsOnHitAfterTimeout(self):
        l = []

        def on_hit(l):
            l.append(1)

        node = self.node_factory.create_new_node(
            {'projectile': {'on_hit': on_hit, 'args': {'l': l}}})
        self.proj_sys.handle(node, 1000000)
        self.assertEqual(len(l), 0)
        self.proj_sys.handle(node, 1000050)
        self.assertEqual(len(l), 0)
        self.proj_sys.handle(node, 1000100)
        self.assertEqual(len(l), 1)


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
