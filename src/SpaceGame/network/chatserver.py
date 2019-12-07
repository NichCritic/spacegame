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
import tornado.locks
import tornado.web
import tornado.websocket

import uuid

from tornado import gen
from tornado.options import define

import json
import asyncio


define("port", default=8888, help="run on the given port", type=int)


class MessageBuffer(object):

    def __init__(self):
        self.cond = tornado.locks.Condition()
        self.cache = []
        self.cache_size = 1

    def get_messages_since(self, cursor=None):
        results = []
        for msg in reversed(self.cache):
            # logging.info(msg)
            if msg.id == cursor:
                break
            results.append(msg)
        results.reverse()
        self.cache = []
        return results

    def new_messages(self, messages):
        # logging.info("Sending new message to %r listeners", len(self.waiters))
        self.cache.extend(messages)
        if len(self.cache) > self.cache_size:
            self.cache = self.cache[-self.cache_size:]
        self.cond.notify_all()


# Making this a non-singleton is left as an exercise for the reader.
#global_message_buffer = MessageBuffer()
#user_message_buffers = data_cache.user_message_buffers


class BaseHandler(tornado.web.RequestHandler):

    def create_player(self):
        with self.session_manager.get_session() as session:
            player = self.player_factory.create_player(
                MessageBuffer(), self.current_user["id"])
            self.current_user["player_id"] = player.id
            avatar_id = self.account_utils.get_previous_avatar_for_player(
                player.id, session)
            if avatar_id is None:
                self.redirect("/charater_select")
                return
            self.player_factory.set_player_avatar(player, avatar_id)

    def get_current_user(self):
        user_json = self.get_secure_cookie("chatdemo_user")
        if not user_json:
            return None
        # return {"name": "Nicholas", "email": "n.aelick@gmail.com", "id":
        # "11111", "given_name": 'Nicholas', "acct_id": 1, "player_id":
        # "11111"}
        return tornado.escape.json_decode(user_json)


class MainHandler(BaseHandler):

    @tornado.web.authenticated
    def get(self):
        self.render("client/index2.html", messages=[])


class TestHandler(BaseHandler):

    @tornado.web.authenticated
    def get(self):
        self.render("client/index5.html", messages=[])


class ShopHandler(BaseHandler):

    def initialize(self, account_utils, player_factory, session_manager, node_factory):
        self.account_utils = account_utils
        self.player_factory = player_factory
        self.session_manager = session_manager
        self.node_factory = node_factory

    def man_dist(self, pos_a, pos_b):
        return abs(pos_a.x - pos_b.x) + abs(pos_a.y - pos_b.y)

    def get_player(self):
        if not self.current_user['id'] in self.player_factory.players:
            self.clear()
            self.set_status(500)
            logging.info("Finish called get_player")
            self.finish("No currently signed in user")
            return

        player = self.player_factory.players[self.current_user['id']]
        return player

    def get_closest_shop(self, av):

        shops = self.node_factory.create_node_list(
            ["position", "shop"], [], av.sector.neighbours)

        if not shops:
            self.clear()
            self.set_status(404)
            logging.info("Finish called get_closest_shop")
            self.finish("Not near any shops")
            return

        closest = shops[0]

        for shop in shops:
            if self.man_dist(av.position, closest.position) < self.man_dist(av.position, shop.position):
                closest = shop

        return closest

    @tornado.web.authenticated
    def get(self):
        player = self.get_player()
        av = self.node_factory.create_node(
            player.avatar_id, ["position", "sector", "inventory"])

        closest = self.get_closest_shop(av)
        closest.add_or_attach_component('inventory', {'inventory': {}})
        data = closest.shop.shop_data
        data['inventory'] = closest.inventory.inv
        data['player_inventory'] = av.inventory.inv
        logging.info("Finish called closest_shop get")
        self.finish(data)

    @tornado.web.authenticated
    def post(self):
        post_data = self.get_argument("body")
        json_data = json.loads(post_data)

        player = self.get_player()
        av = self.node_factory.create_node(
            player.avatar_id, ["position", "sector", "inventory"])
        closest_shop = self.get_closest_shop(av)

        shop_data = closest_shop.shop.shop_data

        items = shop_data["buy_items"] if json_data[
            'msg'] == 'sell' else shop_data["sale_items"]

        item_id = json_data["item_id"]

        selected_item = None
        for i in items:
            if i["id"] == item_id:
                selected_item = i

        player = self.get_player()

        av = self.node_factory.create_node(
            player.avatar_id, [])

        av.add_or_attach_component('transaction', {"transactions": []})

        logging.info("adding transaction")

        if json_data['msg'] == 'buy':
            av.transaction.transactions.append({
                "buyer_id": av.id,
                "seller_id": closest_shop.id,
                "item_id": item_id,
                "quantity": 1,
                "price": selected_item["cost"]
            })

        if json_data['msg'] == 'sell':
            av.transaction.transactions.append({
                "buyer_id": closest_shop.id,
                "seller_id": av.id,
                "item_id": item_id,
                "quantity": 1,
                "price": selected_item["cost"]
            })
        logging.info("Finish called shop post")
        self.finish({"success": True})


class InventoryHandler(BaseHandler):

    def initialize(self, account_utils, player_factory, session_manager, node_factory):
        self.account_utils = account_utils
        self.player_factory = player_factory
        self.session_manager = session_manager
        self.node_factory = node_factory

    def get_player(self):
        if not self.current_user['id'] in self.player_factory.players:
            self.clear()
            self.set_status(500)
            logging.info("Finish called inv get_player")
            self.finish("No currently signed in user")
            return

        player = self.player_factory.players[self.current_user['id']]
        return player

    @tornado.web.authenticated
    def get(self):
        import objects.item
        player = self.get_player()
        av = self.node_factory.create_node(player.avatar_id, ["inventory"], [])

        with self.session_manager.get_session() as session:
            inventory = av.inventory.inv
            items = [{"name": objects.item.get_item_by_id(
                session, it).name, "id": it, "qty": inventory[it]["qty"]} for it in inventory]

        data = {"inventory": items}
        logging.info("Finish called items get")
        self.finish(data)


class UpgradeHandler(BaseHandler):

    def initialize(self, account_utils, player_factory, session_manager, node_factory):
        self.account_utils = account_utils
        self.player_factory = player_factory
        self.session_manager = session_manager
        self.node_factory = node_factory

    def get_player(self):
        if not self.current_user['id'] in self.player_factory.players:
            self.clear()
            self.set_status(500)
            logging.info("Finish called inv get_player")
            self.finish("No currently signed in user")
            return

        player = self.player_factory.players[self.current_user['id']]
        return player

    @tornado.web.authenticated
    def get(self):
        import objects.item
        player = self.get_player()
        av = self.node_factory.create_node(player.avatar_id, ["inventory"], [])

        with self.session_manager.get_session() as session:
            inventory = av.inventory.inv
            items = [{"name": objects.item.get_item_by_id(
                session, it).name, "id": it, "qty": inventory[it]["qty"]} for it in inventory if objects.item.get_item_by_id(session, it).type == "upgrade"]

        data = {"upgrades": items}
        logging.info("Finish called items get")
        self.finish(data)

    @tornado.web.authenticated
    def post(self):
        import objects.item
        post_data = self.get_argument("body")
        json_data = json.loads(post_data)
        item_id = json_data["item_id"]

        player = self.get_player()
        av = self.node_factory.create_node(
            player.avatar_id, ["position", "sector", "inventory"])

        items = av.inventory.inv

        selected_item = None
        for i in items:
            logging.info(str(items))
            if i == item_id:
                selected_item = i

        with self.session_manager.get_session() as session:
            upgrade = items[selected_item]
            logging.info(upgrade)
            upgrade_name = objects.item.get_item_by_id(
                session, selected_item).name

            if upgrade['qty'] > 0:
                av.add_or_attach_component(
                    'apply_upgrade', {"upgrade_name": upgrade_name, "upgrade_id": selected_item})
                upgrade['qty'] -= 1

        self.finish({"success": True})


class MoneyHandler(BaseHandler):

    def initialize(self, account_utils, player_factory, session_manager, node_factory):
        self.account_utils = account_utils
        self.player_factory = player_factory
        self.session_manager = session_manager
        self.node_factory = node_factory

    def get_player(self):
        if not self.current_user['id'] in self.player_factory.players:
            self.clear()
            self.set_status(500)
            logging.info("Finish called MoneyHandler get_player")
            self.finish("No currently signed in user")
            return

        player = self.player_factory.players[self.current_user['id']]
        return player

    @tornado.web.authenticated
    def get(self):
        player = self.get_player()
        av = self.node_factory.create_node(player.avatar_id, ["money"], [])

        data = {"money": av.money.money}
        logging.info("Finish called MoneyHandler get")
        self.finish(data)


class MinimapHandler(BaseHandler):

    def initialize(self, account_utils, player_factory, session_manager, node_factory):
        self.account_utils = account_utils
        self.player_factory = player_factory
        self.session_manager = session_manager
        self.node_factory = node_factory

    def get_player(self):
        if not self.current_user['id'] in self.player_factory.players:
            self.clear()
            self.set_status(500)
            logging.info("Finish called Minimap get_player")
            self.finish("No currently signed in user")
            return

        player = self.player_factory.players[self.current_user['id']]
        return player

    @tornado.web.authenticated
    def get(self):
        nodes = self.node_factory.create_node_list(["position", "area"], [])
        player = self.get_player()
        av = self.node_factory.create_node(
            player.avatar_id, ["position", "area"], [])

        data = {"positions": [{"id": n.id, "radius": n.area.radius, "x": n.position.x,
                               "y": n.position.y} for n in nodes if n.area.radius > 90],
                "player": {"id": av.id, "radius": av.area.radius, "x": av.position.x,
                           "y": av.position.y}}
        logging.info("Finish called Minimap get")
        self.finish(data)


class CharacterCreateHandler(BaseHandler):

    def initialize(self, account_utils, player_factory, session_manager):
        self.account_utils = account_utils
        self.player_factory = player_factory
        self.session_manager = session_manager

    @tornado.web.authenticated
    def get(self):
        self.render("character_create.html")

    @tornado.web.authenticated
    def post(self):
        # print(self.current_user)
        acct_id = self.current_user["acct_id"]

        # print(self.current_user)
        # print(self.request.body)

        post_data = self.request.body.decode('utf-8')

        post_data = post_data.split('&')

        post_data = dict([p.split('=') for p in post_data])

        data = {"name": post_data['character_name']}

        with self.session_manager.get_session() as session:
            self.account_utils.create_new_avatar_for_account(
                acct_id, data, session)

        # print(self.request.body)
        self.write({"result": "ok"})
        logging.info("Finish called CharacterCreateHandler get")
        self.finish()
        # if self.get_argument("next", None):
        #    self.redirect(self.get_argument("next"))


class CharacterSelectHandler(BaseHandler):

    def initialize(self, account_utils, player_factory, node_factory, session_manager):
        self.account_utils = account_utils
        self.player_factory = player_factory
        self.node_factory = node_factory
        self.av = None
        self.session_manager = session_manager

    @tornado.web.authenticated
    def get(self):
        with self.session_manager.get_session() as session:
            acc_id = self.current_user["acct_id"]
            acc = self.account_utils.get_by_id(acc_id, session)
            avatars = acc.avatars

            if not self.current_user['id'] in self.player_factory.players:
                player = self.player_factory.create_player(
                    MessageBuffer(), self.current_user["id"])
                self.current_user["player_id"] = player.id

            self.av = []

            for i, avatar in enumerate(avatars):
                id = avatar.avatar_id
                avatar_node = self.node_factory.create_node(
                    id, [], ['player_controlled'])
                name = "TEMP"
                location = "TEMP"
                description = "temp_description"

                if avatar_node.has('player_controlled'):
                    avatar_node.remove_component('player_controlled')

                self.av.append({
                    "index": i,
                    "id": id,
                    "name": name,
                    "location": location,
                    "description": description
                })

            self.render("character_select.html", characters=self.av)

    @tornado.web.authenticated
    def post(self):
        # print(self.request.body)
        with self.session_manager.get_session() as session:
            # import pdb; pdb.set_trace()
            player = self.player_factory.get_player(
                self.current_user["player_id"])

            index = self.get_argument("id")

            acc_id = self.current_user["acct_id"]
            acc = self.account_utils.get_by_id(acc_id, session)
            avatars = self.account_utils.get_avatars_for_account(acc, session)

            # print(avatars)

            self.av = [{"index": index, "id": av.avatar_id}
                       for index, av in enumerate(avatars)]

            self.player_factory.set_player_avatar(
                player, self.av[int(index)]["id"])
            # TODO: messy hack
            self.account_utils.set_avatars_pid(
                self.av[int(index)]["id"], player.id, session)

            if self.get_argument("next", None):
                self.redirect(self.get_argument("next"))
            else:
                self.write(tornado.escape.to_basestring("ok"))
                logging.info("Finish called CharacterSelectHandler post")
                self.finish()

        # if self.get_argument("next", None):
        #    self.redirect(self.get_argument("next"))


class CommandMessageHandler(BaseHandler):

    def initialize(self, command_handler, player_factory, session_manager, account_utils):
        self.command_handler = command_handler
        self.player_factory = player_factory
        self.session_manager = session_manager
        self.account_utils = account_utils

    @tornado.web.authenticated
    def post(self):
        message = {
            "id": str(uuid.uuid4()),
            "from": self.current_user["email"],
            "body": self.get_argument("body"),
        }
        # logging.info(self.current_user)
        if not self.current_user['id'] in self.player_factory.players:
            self.create_player()
        player = self.player_factory.get_player(self.current_user["player_id"])
        result = self.command_handler.handle_command(player, message["body"])
        # logging.info(result)
        if result[0] == "error":
            # to_basestring is necessary for Python 3's json encoder,
            # which doesn't accept byte strings.
            message["body"] = ["Sorry, I can't understand that"]
        else:
            message["body"] = [""]
        message["html"] = tornado.escape.to_basestring(
            self.render_string("message.html", message=message))
        if self.get_argument("next", None):
            self.redirect(self.get_argument("next"))
        else:
            self.write(message)
        # self.player_factory.players[self.current_user[
            # "id"]].message_buffer.new_messages([message])
        self.finish()


class MessageUpdatesHandler(tornado.websocket.WebSocketHandler):

    def initialize(self, player_factory, account_utils, session_manager, node_factory, command_handler):
        # TODO: This seems strange
        self.player_factory = player_factory
        self.account_utils = account_utils
        self.session_manager = session_manager
        self.node_factory = node_factory
        self.command_handler = command_handler

    def create_player(self):
        with self.session_manager.get_session() as session:
            player = self.player_factory.create_player(
                MessageBuffer(), self.current_user["id"])
            self.current_user["player_id"] = player.id
            avatar_id = self.account_utils.get_previous_avatar_for_player(
                player.id, session)
            if avatar_id is None:
                self.redirect("/charater_select")
                return
            self.player_factory.set_player_avatar(player, avatar_id)

    def get_current_user(self):
        user_json = self.get_secure_cookie("chatdemo_user")
        if not user_json:
            return None
        # return {"name": "Nicholas", "email": "n.aelick@gmail.com", "id":
        # "11111", "given_name": 'Nicholas', "acct_id": 1, "player_id":
        # "11111"}
        return tornado.escape.json_decode(user_json)

    async def get(self, *args, **kwargs):
        if (not self.current_user):
            self.set_status(401)
            self.finish("Unauthorized")
            logging.info("CLOSED CONNECTION")
            return
        logging.info("OPENING THE CONNECTION")
        await super(MessageUpdatesHandler, self).get(*args, **kwargs)

    def open(self):
        # pass
        tornado.ioloop.IOLoop.current().spawn_callback(self.start_poll)
        # else:
        #     self.close()
        #     

    async def start_poll(self):
        await self.poll()

    async def poll(self):
        # print(self.current_user["id"])
        while True:
            try:

                if not self.current_user['id'] in self.player_factory.players:
                    self.create_player()
                msg_buffer = self.player_factory.players[
                    self.current_user["id"]].message_buffer
                messages = msg_buffer.get_messages_since(cursor=None)
                while not messages:
                    logging.info("WAIT_ON_MESSAGES")
                    self.wait_future = msg_buffer.cond.wait()
                    try:
                        await self.wait_future
                    except asyncio.CancelledError:
                        return
                    messages = msg_buffer.get_messages_since(None)
                logging.info("SENDING MESSAGES")
                self.write_message(dict(messages=[m.msg for m in messages]))

            except Exception as e:
                import traceback
                traceback.print_exc()
                logging.error(e)
                self.clear()
                return
    async def on_message(self, message):
        # logging.info(message)
        if not self.current_user['id'] in self.player_factory.players:
            self.create_player()
        player = self.player_factory.get_player(self.current_user["player_id"])
        self.command_handler.handle_command(player, message)
        # await self.poll()



class AuthLoginHandler(tornado.web.RequestHandler, tornado.auth.GoogleOAuth2Mixin):

    def initialize(self, account_utils, player_factory, session_manager):
        self.account_utils = account_utils
        self.player_factory = player_factory
        self.session_manager = session_manager

    async def get(self):
        # print(self.get_query_argument("code", False))
        if self.get_query_argument("code", False):

            access = await self.get_authenticated_user(
                redirect_uri='http://naelick.com:8888/auth/login',
                code=self.get_query_argument('code'))

            logging.info(access)
            user = await self.oauth2_request(
                "https://www.googleapis.com/oauth2/v2/userinfo",
                access_token=access["access_token"])

            logging.info(user)
            with self.session_manager.get_session() as session:
                acct = self.account_utils.handle_login(
                    user, self.player_factory, session)
                player = self.player_factory.create_player(
                    MessageBuffer(), user["id"])

                user["acct_id"] = acct.id
                user["player_id"] = player.id

                self.set_secure_cookie("chatdemo_user",
                                       tornado.escape.json_encode(user))

                self.redirect("/character_select")
        else:
            self.authorize_redirect(
                redirect_uri='http://naelick.com:8888/auth/login',
                client_id="746170306889-840qspkc0dcdlb3sur4ml7daalll4uvo.apps.googleusercontent.com",
                scope=['profile', 'email'],
                response_type='code',
                extra_params={'approval_prompt': 'auto'})


class AuthLogoutHandler(BaseHandler):

    def get(self):
        self.clear_cookie("chatdemo_user")
        self.render('logout.html')
