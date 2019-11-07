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

from Systems.collisionMovementSystem import CollisionMovementSystem
from Systems.collisionSink import CollisionSink
from Systems.collisionSystem import CollisionSystem
from Systems.collisionDamageSystem import CollisionDamageSystem
from Systems.game_state_request import GameStateRequestSystem
from Systems.historySystem import HistorySystem
from Systems.input_system import InputSystem
from Systems.inventoryMassSystem import InventoryMassSystem
from Systems.miningSystem import MiningSystem
from Systems.NetworkMessageSystem import NetworkMessageSystem
from Systems.processorSystem import ProcessorSystem
from Systems.proximitySystem import ProximitySystem
from Systems.purePhysicsSystem import PhysicsSystem
from Systems.server_update_system import ServerUpdateSystem
from Systems.shooting_system import ShootingSystem
from Systems.shopUnpackSystem import ShopUnpackSystem
from Systems.spatial_system import SpatialSystem
from Systems.system_set import SystemSet
from Systems.transaction_system import TransactionSystem
from Systems.expirySystem import ExpirySystem
from Systems.pickupSystem import PickupSystem
from Systems.aiOrientTowardsTargetSystem import AIOrientTowardsTargetSystem
from Systems.proximityTargetSystem import ProximityTargetSystem
from Systems.EventProximityTriggerSystem import EventProximityTriggerSystem
from Systems.EventActiveSystem import EventActiveSystem

import objects.item


from command.command_handler import CommandHandler


def setup_objects(all_db_components, all_components, session):
    object_db = DBComponentSource(all_db_components, session)
    object_array = ArrayComponentSource(all_components)
    component_manager = ComponentManager([object_array])
    db_component_manager = ComponentManager([object_db, object_array])
    node_factory = NodeFactoryDB(component_manager)
    db_node_factory = NodeFactoryDB(db_component_manager)
    player_factory = PlayerFactory(component_manager)
    default_room = "6cb2fa80-ddb1-47bb-b980-31b01d97add5"
    avatar_factory = AvatarFactory(db_node_factory, db_component_manager, {
        "starting_room": default_room,
        "player_id": 0})
    account_utils = AccountUtils(avatar_factory)

    return avatar_factory, node_factory, db_node_factory, object_db, player_factory, account_utils


def unpack_db_objects(node_factory):
    import json
    node_list = node_factory.create_node_list(["instance_components"], [])

    for node in node_list:
        icomp = json.loads(node.instance_components.components)
        # import pdb
        # pdb.set_trace()
        for component, data in icomp.items():
            if isinstance(data, str):
                node.add_or_attach_component(data, {})
                node.add_or_attach_component(component, {})
                node.components[component].__dict__.update(
                    node.components[data].__dict__)
            else:
                node.add_or_attach_component(component, data)


def create_spacestations(node_factory, session):
    import math
    import random

    gold_ore = objects.item.get_item_by_name(session, 'gold ore').static_copy()
    silver_ore = objects.item.get_item_by_name(
        session, 'silver ore').static_copy()
    iron_ore = objects.item.get_item_by_name(session, 'iron ore').static_copy()

    # for i in range(100000):
    #     x = math.floor(random.random() * 10000000 - 5000000)
    #     y = math.floor(random.random() * 10000000 - 5000000)
    node_factory.create_new_node({
        "type": {"type": "asteroid"},
        "area": {"radius": 100},
        "position": {"x": 1500, "y": 0},
        "rotation": {"rotation": 10},
        "velocity": {"x": 0.00, "y": 0.00},
        "collidable": {},
        'force': {},
        'acceleration': {},
        'mass': {},
        'server_updated': {},
        'physics_update': {},
        'state_history': {},
        'minable': {"products": [iron_ore] * 100 + [silver_ore] * 10 + [gold_ore] * 1}

    })

    node_factory.create_new_node({
        "type": {"type": "ship"},
        "area": {"radius": 25},
        "position": {"x": 100, "y": 100},
        "rotation": {"rotation": 0},
        "velocity": {"x": 0, "y": 0},
        'force': {},
        'acceleration': {},
        'mass': {},
        'physics_update': {},
        'state_history': {},
        'orient_towards_target': {},
        'proximity_target_behaviour': {},
        'health': {'health': 100, 'max_health': 100},
        'collidable': {}
    })

    def test_script():
        logging.info("Event fired!")

    node_factory.create_new_node({
        "area": {"radius": 100},
        "position": {"x": -1500, "y": -1500},
        "velocity": {"x": 0, "y": 0},  # Needed to pick up proximity
        "event": {"script": test_script},
        "event_proximity_trigger": {}
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
    system_set = SystemSet()
    shopUnpackSystem = ShopUnpackSystem(node_factory, session_manager)
    nms = NetworkMessageSystem(node_factory, player_factory)
    expiry = ExpirySystem(node_factory)
    invmass = InventoryMassSystem(node_factory)
    insys = InputSystem(node_factory)
    sersys = ServerUpdateSystem(node_factory)
    hissys = HistorySystem(node_factory)
    physys = PhysicsSystem(node_factory)
    shoot = ShootingSystem(node_factory)
    spatial = SpatialSystem(node_factory)
    proximity = ProximitySystem(node_factory)
    collision = CollisionSystem(node_factory)
    collision_dam = CollisionDamageSystem(node_factory)
    pickup = PickupSystem(node_factory)
    coll_mov = CollisionMovementSystem(node_factory)
    mining = MiningSystem(node_factory)
    transaction = TransactionSystem(node_factory)
    processor = ProcessorSystem(node_factory)
    proxy_target = ProximityTargetSystem(node_factory)
    ai_orient_tow_tar = AIOrientTowardsTargetSystem(node_factory)
    event_proxy = EventProximityTriggerSystem(node_factory)
    event_active = EventActiveSystem(node_factory)
    coll_sink = CollisionSink(node_factory)

    game_state_req = GameStateRequestSystem(node_factory)
    system_set.register(shopUnpackSystem)
    system_set.register(nms)
    system_set.register(expiry)
    system_set.register(invmass)
    system_set.register(insys)
    system_set.register(hissys)
    system_set.register(sersys)
    system_set.register(physys)
    system_set.register(shoot)
    system_set.register(spatial)
    system_set.register(proximity)
    system_set.register(collision)
    system_set.register(collision_dam)
    system_set.register(pickup)
    system_set.register(coll_mov)
    system_set.register(mining)
    system_set.register(transaction)
    system_set.register(processor)
    system_set.register(proxy_target)
    system_set.register(ai_orient_tow_tar)
    system_set.register(event_proxy)
    system_set.register(event_active)
    system_set.register(coll_sink)
    system_set.register(game_state_req)

    return system_set
