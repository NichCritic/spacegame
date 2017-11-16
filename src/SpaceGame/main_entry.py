'''
Created on 2011-08-14

@author: Nich

'''
import tornado.ioloop
import os.path
import keys
from tornado.options import options, parse_command_line
from network.chatserver import MainHandler, AuthLoginHandler, AuthLogoutHandler, MessageUpdatesHandler, CommandMessageHandler, CharacterSelectHandler, CharacterCreateHandler, TestHandler

from objects.components import components, db_components

from startup_scripts import register_systems, setup_commands, setup_db, setup_objects


all_db_components = {}
all_db_components.update(db_components)

all_components = {}
all_components.update(components)


session_manager = setup_db('sqlite:///main.db')

with session_manager.get_session() as session:
    avatar_factory, node_factory, object_db, player_factory, account_utils = setup_objects(
        all_db_components, all_components, session)


command_handler = setup_commands(node_factory)
system_set = register_systems(
    session_manager, object_db, node_factory, player_factory)


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
                                                                player_factory=player_factory, session_manager=session_manager, node_factory=node_factory)),
            (r"/character_select", CharacterSelectHandler, dict(account_utils=account_utils,
                                                                player_factory=player_factory, session_manager=session_manager, node_factory=node_factory)),
            (r"/character_create", CharacterCreateHandler, dict(account_utils=account_utils,
                                                                player_factory=player_factory, session_manager=session_manager)),
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
        system_set.process, 200, io_loop=tornado.ioloop.IOLoop.instance())
    system_set_callback.start()

    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    main()
