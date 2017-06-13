#!/usr/bin/env python
#
# Copyright 2009 Facebook
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import logging
import tornado.auth
import tornado.escape

import tornado.web

import uuid

from tornado import gen
from tornado.options import define






define("port", default=8888, help="run on the given port", type=int)


class MessageBuffer(object):
    def __init__(self):
        self.waiters = set()
        self.cache = []
        self.cache_size = 200

    def wait_for_messages(self, callback, cursor=None):
        if cursor:
            new_count = 0
            for msg in reversed(self.cache):
                if msg["id"] == cursor:
                    break
                new_count += 1
            if new_count:
                callback(self.cache[-new_count:])
                return
        self.waiters.add(callback)

    def cancel_wait(self, callback):
        self.waiters.remove(callback)

    def new_messages(self, messages):
        logging.info("Sending new message to %r listeners", len(self.waiters))
        for callback in self.waiters:
            try:
                callback(messages)
            except:
                logging.error("Error in waiter callback", exc_info=True)
        self.waiters = set()
        self.cache.extend(messages)
        if len(self.cache) > self.cache_size:
            self.cache = self.cache[-self.cache_size:]


# Making this a non-singleton is left as an exercise for the reader.
#global_message_buffer = MessageBuffer()
#user_message_buffers = data_cache.user_message_buffers



class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        user_json = self.get_secure_cookie("chatdemo_user")
        if not user_json: return None
        return tornado.escape.json_decode(user_json)


class MainHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        self.render("index.html", messages=[])

class CharacterCreateHandler(BaseHandler):
    def initialize(self, account_utils, player_factory, session_manager ):
        self.account_utils = account_utils
        self.player_factory = player_factory
        self.session_manager = session_manager
        
    @tornado.web.authenticated
    def get(self):
        self.render("character_create.html")
    
    @tornado.web.authenticated
    def post(self):
        #print(self.current_user)
        acct_id = self.current_user["acct_id"]
        
        #print(self.current_user)
        
        with self.session_manager.get_session() as session:
            self.account_utils.create_new_avatar_for_account(acct_id, session)
        
        #print("YESSSS, ALMIGHTYPOWER")
        #print(self.request.body)
        self.write({"result":"ok"})
        return
        #if self.get_argument("next", None):
        #    self.redirect(self.get_argument("next"))

class CharacterSelectHandler(BaseHandler):
    def initialize(self, account_utils, player_factory, session_manager):
        self.account_utils = account_utils
        self.player_factory = player_factory
        self.av = None
        self.session_manager = session_manager
    
    @tornado.web.authenticated
    def get(self):
        with self.session_manager.get_session() as session:
            acc_id = self.current_user["acct_id"]
            acc = self.account_utils.get_by_id(acc_id, session)
            avatars = acc.avatars
            
            #print(avatars)
            
            self.av = [{"index": index, "id":av.avatar_id} for index, av in enumerate(avatars)]
            
            self.render("character_select.html", characters=self.av)
    
    @tornado.web.authenticated
    @tornado.web.asynchronous
    def post(self):
        #print(self.request.body)
        with self.session_manager.get_session() as session:
            player = self.player_factory.get_player(self.current_user["player_id"])
            
            index = self.get_argument("id")
            
            acc_id = self.current_user["acct_id"]
            acc = self.account_utils.get_by_id(acc_id, session)
            avatars = self.account_utils.get_avatars_for_account(acc, session)
            
            #print(avatars)
            
            self.av = [{"index": index, "id":av.avatar_id} for index, av in enumerate(avatars)]
            
            player.set_avatar(self.av[int(index)]["id"])
            #TODO: messy hack
            self.account_utils.set_avatars_pid(self.av[int(index)]["id"], player.id, session)
            
            if self.get_argument("next", None):
                self.redirect(self.get_argument("next"))
            else:
                self.write(tornado.escape.to_basestring("ok"))
                self.finish()
        
        #if self.get_argument("next", None):
        #    self.redirect(self.get_argument("next"))
            


class CommandMessageHandler(BaseHandler):
    def initialize(self, command_handler, player_factory):
        self.command_handler = command_handler
        self.player_factory = player_factory
        
    @tornado.web.authenticated
    @tornado.web.asynchronous
    def post(self):
        message = {
            "id": str(uuid.uuid4()),
            "from": self.current_user["first_name"],
            "body": self.get_argument("body"),
        }
        logging.info(self.current_user)
        player = self.player_factory.get_player(self.current_user["player_id"])
        result = self.command_handler.handle_command(player, message["body"])
        logging.info(result)
        if result[0] == "error":
        # to_basestring is necessary for Python 3's json encoder,
        # which doesn't accept byte strings.
            message["body"] = "Sorry, I can't understand that"
        else:
            message["body"] = ""
        
        message["html"] = tornado.escape.to_basestring(
            self.render_string("message.html", message=message))
        if self.get_argument("next", None):
            self.redirect(self.get_argument("next"))
        else:
            self.write(message)
        self.player_factory.players[self.current_user["claimed_id"]].message_buffer.new_messages([message])
        self.finish()
        
     

'''
class MessageNewHandler(BaseHandler):
    
    
    @tornado.web.authenticated
    def post(self):
        message = {
            "id": str(uuid.uuid4()),
            "from": self.current_user["first_name"],
            "body": self.get_argument("body"),
        }
        
        
        # to_basestring is necessary for Python 3's json encoder,
        # which doesn't accept byte strings.
        message["html"] = tornado.escape.to_basestring(
            self.render_string("message.html", message=message))
        if self.get_argument("next", None):
            self.redirect(self.get_argument("next"))
        else:
            self.write(message)
        global_message_buffer.new_messages([message])
'''
        

class MessageUpdatesHandler(BaseHandler):
    def initialize(self, player_factory):
        #TODO: This seems strange
        self.player_factory = player_factory
    
    
    @tornado.web.authenticated
    @tornado.web.asynchronous
    def post(self):
        print(self.current_user["claimed_id"])
        cursor = self.get_argument("cursor", None)
        self.player_factory.players[self.current_user["claimed_id"]].message_buffer.wait_for_messages(self.on_new_messages,
                                                cursor=cursor)
        
        
        
        

    def on_new_messages(self, messages):
        # Closed client connection
        if self.request.connection.stream.closed():
            return
        self.finish(dict(messages=messages))

    def on_connection_close(self):
        self.player_factory.players[self.current_user["claimed_id"]].message_buffer.cancel_wait(self.on_new_messages)


class AuthLoginHandler(BaseHandler, tornado.auth.GoogleMixin):
    def initialize(self, account_utils, player_factory, session_manager):
        self.account_utils = account_utils
        self.player_factory = player_factory
        self.session_manager = session_manager
        
    
    @tornado.web.asynchronous
    @gen.coroutine
    def get(self):
        if self.get_argument("openid.mode", None):
            user = yield self.get_authenticated_user()
            
            with self.session_manager.get_session() as session:
            
                acct = self.account_utils.handle_login(user, self.player_factory, session)
                player = self.player_factory.create_player(MessageBuffer(), user["claimed_id"])
                
                
                user["acct_id"] = acct.id
                user["player_id"] = player.id
                
                
                self.set_secure_cookie("chatdemo_user",
                                       tornado.escape.json_encode(user))
                
                
                 
                
                
                self.redirect("/character_select")
                return
        self.authenticate_redirect(ax_attrs=["name", "email"])


class AuthLogoutHandler(BaseHandler):
    def get(self):
        self.clear_cookie("chatdemo_user")
        self.write("You are now logged out")



