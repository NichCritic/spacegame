'''
Created on 2011-08-14

@author: Nich

'''
import tornado.ioloop
import os.path
import keys
from tornado.options import options, parse_command_line
from network.chatserver import MainHandler, AuthLoginHandler, AuthLogoutHandler, MessageUpdatesHandler, CommandMessageHandler, CharacterSelectHandler, CharacterCreateHandler, TestHandler, ShopHandler, InventoryHandler, UpgradeHandler, MoneyHandler, MinimapHandler, QuestHandler

from objects.components import components, db_components
import objects.item

from startup_scripts import register_systems, setup_commands, setup_db, setup_objects, collision_test, create_spacestations, unpack_db_objects, setup_quests


all_db_components = {}
all_db_components.update(db_components)

all_components = {}
all_components.update(components)


session_manager = setup_db('sqlite:///main.db')

with session_manager.get_session() as session:
    avatar_factory, node_factory, db_node_factory, object_db, player_factory, account_utils, fine_spatial_map, coarse_spatial_map = setup_objects(
        all_db_components, all_components, session)
    object_db.set_session(session)
    create_spacestations(db_node_factory, session)
    # collision_test(db_node_factory, session)
    unpack_db_objects(db_node_factory)


quest_manager, quest_systems = setup_quests(node_factory, session_manager)
command_handler = setup_commands(
    node_factory, session_manager, object_db, quest_manager)
system_set = register_systems(
    session_manager, object_db, node_factory, db_node_factory, player_factory, quest_systems, fine_spatial_map, coarse_spatial_map)


def main():
    parse_command_line()

    app = tornado.web.Application(
        [
            (r"/", MainHandler),
            (r"/test", TestHandler),
            (r"/auth/login", AuthLoginHandler, dict(account_utils=account_utils,
                                                    player_factory=player_factory, session_manager=session_manager)),
            (r"/auth/logout", AuthLogoutHandler),
            (r"/a/message/new", CommandMessageHandler, dict(account_utils=account_utils,
                                                            command_handler=command_handler, player_factory=player_factory, session_manager=session_manager)),
            (r"/a/message/updates", MessageUpdatesHandler, dict(account_utils=account_utils,
                                                                player_factory=player_factory, session_manager=session_manager, node_factory=node_factory, command_handler=command_handler)),
            (r"/character_select", CharacterSelectHandler, dict(account_utils=account_utils,
                                                                player_factory=player_factory, session_manager=session_manager, node_factory=node_factory)),
            (r"/character_create", CharacterCreateHandler, dict(account_utils=account_utils,
                                                                player_factory=player_factory, session_manager=session_manager)),
            (r"/shop", ShopHandler, dict(account_utils=account_utils,
                                         player_factory=player_factory, session_manager=session_manager, node_factory=node_factory)),
            (r"/inv", InventoryHandler, dict(account_utils=account_utils,
                                             player_factory=player_factory, session_manager=session_manager, node_factory=node_factory)),
            (r"/quests", QuestHandler, dict(account_utils=account_utils,
                                            player_factory=player_factory, session_manager=session_manager, node_factory=node_factory)),
            (r"/upgrade", UpgradeHandler, dict(account_utils=account_utils,
                                               player_factory=player_factory, session_manager=session_manager, node_factory=node_factory)),
            (r"/money", MoneyHandler, dict(account_utils=account_utils,
                                           player_factory=player_factory, session_manager=session_manager, node_factory=node_factory)),
            (r"/minimap", MinimapHandler, dict(account_utils=account_utils,
                                               player_factory=player_factory, session_manager=session_manager, node_factory=node_factory))
        ],
        cookie_secret=keys.cookie_secret,
        login_url="/auth/login",
        template_path=os.path.join(os.path.dirname(__file__), "templates"),
        static_path=os.path.join(os.path.dirname(__file__), "static"),
        xsrf_cookies=False,
        google_oauth={"key": keys.google_oauth_key,
                      "secret": keys.google_oauth_secret}
    )
    app.listen(options.port)
    system_set_callback = tornado.ioloop.PeriodicCallback(
        system_set.process, 50)

    system_set_callback.start()

    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    main()
