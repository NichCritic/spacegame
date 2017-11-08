'''
Created on 2014-02-01

@author: Nich
'''
import unittest
import model.account as account
import model.base as base
from player.avatar import AvatarFactory
from objects.component_manager import ArrayComponentSource, DBComponentSource, ComponentManager
from objects.node_factory import NodeFactoryDB
from objects.components import components, db_components
from room.room_components import components as room_components, db_components as db_room_components


class Test(unittest.TestCase):

    def setUp(self):
        self.engine = base.engine('sqlite:///:memory:')
        self.Session = base.create_sessionmaker(self.engine)
        base.Base.metadata.create_all(self.engine)

        all_db_components = {}
        all_db_components.update(db_components)
        all_db_components.update(db_room_components)

        all_components = {}
        all_components.update(components)
        all_components.update(room_components)

        self.component_object = ArrayComponentSource(all_components)
        self.db_component_object = DBComponentSource(
            all_db_components, self.Session())
        self.comp_manager = ComponentManager(
            [self.db_component_object, self.component_object])
        self.node_factory = NodeFactoryDB(self.comp_manager)

        starting_room = self.node_factory.create_new_node({"container": {}})

        self.avatar_factory = AvatarFactory(self.node_factory, self.comp_manager, data={
                                            "starting_room": starting_room.id, "starting_location": "temp", "player_id": "temp"})

        self.account_utils = account.AccountUtils(self.avatar_factory)

        self.session = self.Session()
        self.db_component_object.set_session(self.session)

    def tearDown(self):
        self.session.commit()
        self.session.close()

        base.Base.metadata.drop_all(self.engine)
        pass

    def testCreate(self):
        session = self.Session()
        self.account_utils.make_account(
            "foo", "bar", "foobar@foobar.com", session)
        session.close()

    def testCreateAvatar(self):
        session = self.Session()
        acc = self.account_utils.make_account(
            "test", "test1", "test@test.com", session)

        data = {}

        self.account_utils.create_new_avatar_for_account(acc.id, data, session)
        self.account_utils.create_new_avatar_for_account(acc.id, data, session)

        session.add(acc)

        for assoc in acc.avatars:
            print(assoc.avatar.id)

        session.close()

    def testGetAvatar(self):
        session = self.Session()
        acc = self.account_utils.make_account(
            "test", "test2", "test@test.com", session)

        self.account_utils.create_new_avatar_for_account(acc.id, {}, session)
        self.account_utils.create_new_avatar_for_account(acc.id, {}, session)

        print(self.account_utils.get_avatars_for_account(acc, session))
        session.close()


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
