'''
Created on 2014-02-25

@author: Nich
'''

import model.base as base
from model.base import SessionManager
from model.account import AccountUtils

from objects.node_factory import NodeFactoryDB
from objects.components import components

from player.avatar import AvatarFactory
from player.player import PlayerFactory
from objects.component_manager import ComponentManager, DBComponentSource, ArrayComponentSource

from Systems.NetworkMessageSystem import NetworkMessageSystem
from Systems.input_system import InputSystem
from Systems.purePhysicsSystem import PhysicsSystem
from Systems.game_state_request import GameStateRequestSystem
from Systems.shooting_system import ShootingSystem
from Systems.server_update_system import ServerUpdateSystem
from Systems.historySystem import HistorySystem
from Systems.system_set import DBSystemSet
from Systems.spatial_system import SpatialSystem
from Systems.transaction_system import TransactionSystem
from Systems.collisionSystem import CollisionSystem
from Systems.collisionMovementSystem import CollisionMovementSystem
from Systems.collisionSink import CollisionSink

import objects.item


from command.command_handler import CommandHandler


def setup_objects(all_db_components, all_components, session):
    object_db = DBComponentSource(all_db_components, session)
    object_array = ArrayComponentSource(all_components)
    component_manager = ComponentManager([object_db, object_array])
    node_factory = NodeFactoryDB(component_manager)
    player_factory = PlayerFactory(component_manager)
    default_room = "6cb2fa80-ddb1-47bb-b980-31b01d97add5"
    avatar_factory = AvatarFactory(node_factory, component_manager, {
        "starting_room": default_room,
        "player_id": 0})
    account_utils = AccountUtils(avatar_factory)

    return avatar_factory, node_factory, object_db, player_factory, account_utils


def create_spacestations(node_factory, session):
    import math
    import random
    # for i in range(100000):
    #     x = math.floor(random.random() * 10000000 - 5000000)
    #     y = math.floor(random.random() * 10000000 - 5000000)
    gold = objects.item.get_item_by_name(session, 'gold')
    silver = objects.item.get_item_by_name(session, 'silver')
    copper = objects.item.get_item_by_name(session, 'copper')
    crystal = objects.item.get_item_by_name(session, 'crystal')

    node_factory.create_new_node(
        {
            'position': {'x': 0, 'y': 0},
            'area': {'radius': 250},
            'collidable': {},
            'type': {'type': 'bolfenn'},
            'shop': {"shop_data":
                     {
                         "name": "Bolfenn shop",
                         "items": [
                             {"id": crystal.id, "pos": 0, "text": crystal.name,
                              "cost": 100, "img": ""},
                             {"id": gold.id, "pos": 1, "text": gold.name,
                              "cost": 1000, "img": ""},
                             {"id": silver.id, "pos": 2, "text": silver.name,
                              "cost": 10000, "img": ""}
                         ]
                     }
                     },
            'money': {
                "money": 0
            },
            "inventory": {
                "inventory": f'{{"{gold.id}": {{"qty": 500}}, "{silver.id}": {{"qty": 500}}, "{crystal.id}": {{"qty": 500}}}}'
            }
        }

    )

    node_factory.create_new_node(
        {
            'position': {'x': 0, 'y': 5000},
            'area': {'radius': 250},
            'collidable': {},
            'type': {'type': 'bolfenn'},
            'shop': {"shop_data":
                     {
                         "name": "Not Bolfenn shop",
                         "items": [
                             {"id": crystal.id, "pos": 0, "text": crystal.name,
                              "cost": 10000, "img": ""},
                             {"id": gold.id, "pos": 1, "text": gold.name,
                              "cost": 1000, "img": ""},
                             {"id": silver.id, "pos": 2, "text": silver.name,
                              "cost": 100, "img": ""}
                         ]
                     }
                     },
            'money': {
                "money": 0
            },
            "inventory": {
                "inventory": f'{{"{gold.id}": {{"qty": 500}}, "{silver.id}": {{"qty": 500}}, "{crystal.id}": {{"qty": 500}}}}'
            }
        }

    )

    node_factory.create_new_node({
        "type": {"type": "asteroid"},
        "area": {"radius": 100},
        "position": {"x": 1500, "y": 0},
        "rotation": {"rotation": 10},
        "velocity": {"x": 0.05, "y": 0.08},
        "collidable": {},
        'force': {},
        'acceleration': {},
        'mass': {},
        'server_updated': {},
        'physics_update': {},
        'state_history': {}

    })


def setup_db(db):
    db_engine = base.engine(db)
    Session = base.create_sessionmaker(db_engine)
    base.Base.metadata.create_all(db_engine)
    session_manager = SessionManager(Session)
    return session_manager


class ObjectProvider(object):

    def __init__(self, Session):
        all_components = {}
        all_components.update(components)

        self.component_object = DBComponentSource(all_components)
        self.comp_manager = ComponentManager([self.component_object], Session)
        self.node_factory = NodeFactoryDB(all_components, Session)


def setup_commands(node_factory, session_manager, db_comps):
    command_handler = CommandHandler(node_factory, session_manager, db_comps)
    return command_handler


def register_systems(session_manager, object_db, node_factory, player_factory):
    system_set = DBSystemSet(object_db, session_manager)
    nms = NetworkMessageSystem(node_factory, player_factory)
    insys = InputSystem(node_factory)
    sersys = ServerUpdateSystem(node_factory)
    hissys = HistorySystem(node_factory)
    physys = PhysicsSystem(node_factory)
    shoot = ShootingSystem(node_factory)
    spatial = SpatialSystem(node_factory)
    collision = CollisionSystem(node_factory)
    coll_mov = CollisionMovementSystem(node_factory)
    transaction = TransactionSystem(node_factory)
    coll_sink = CollisionSink(node_factory)
    game_state_req = GameStateRequestSystem(node_factory)
    system_set.register(nms)
    system_set.register(insys)
    system_set.register(hissys)
    system_set.register(sersys)
    system_set.register(physys)
    system_set.register(shoot)
    system_set.register(spatial)
    system_set.register(collision)
    system_set.register(coll_mov)
    system_set.register(transaction)
    system_set.register(coll_sink)
    system_set.register(game_state_req)

    return system_set
