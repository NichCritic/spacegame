'''
Created on 2014-02-25

@author: Nich
'''

import logging
import model.base as base
from model.base import SessionManager
from model.account import AccountUtils

from objects.node_factory import NodeFactoryDB
from objects.components import components

from player.avatar import AvatarFactory
from player.player import PlayerFactory
from objects.component_manager import ComponentManager, DBComponentSource, ArrayComponentSource

from Systems.aiAvoidShootingAlliesSystem import AIAvoidShootingAlliesSystem
from Systems.aiOrientTowardsTargetSystem import AIOrientTowardsTargetSystem
from Systems.aiReturnHomeSystem import AIReturnHomeSystem
from Systems.aiShootAtTargetSystem import AIShootAtTargetSystem
from Systems.applyUpgradeSystem import ApplyUpgradeSystem
from Systems.boundarySystem import BoundarySystem
from Systems.collisionDamageSystem import CollisionDamageSystem
from Systems.collisionMovementSystem import CollisionMovementSystem
from Systems.collisionSink import CollisionSink
from Systems.collisionSystem import CollisionSystem
from Systems.collisionVelocityDamageSystem import CollisionVelocityDamageSystem
from Systems.deathSystem import DeathSystem
from Systems.EventActiveSystem import EventActiveSystem
from Systems.EventProximityTriggerSystem import EventProximityTriggerSystem
from Systems.expirySystem import ExpirySystem
from Systems.game_state_request import GameStateRequestSystem
from Systems.historySystem import HistorySystem
from Systems.ImpulseSystem import ImpulseSystem
from Systems.input_system import InputSystem
from Systems.inventoryMassSystem import InventoryMassSystem
from Systems.miningSystem import MiningSystem
from Systems.movementTrackingSystem import MovementTrackingSystem
from Systems.NetworkMessageSystem import NetworkMessageSystem
from Systems.pickupSystem import PickupSystem
from Systems.playerDeathSystem import PlayerDeathSystem
from Systems.playerProximityTargetSystem import PlayerProximityTargetSystem
from Systems.processorSystem import ProcessorSystem
from Systems.proximitySystem import ProximitySystem
from Systems.proximityTargetSystem import ProximityTargetSystem
from Systems.purePhysicsSystem import PhysicsSystem
from Systems.server_update_system import ServerUpdateSystem
from Systems.shooting_system import ShootingSystem
from Systems.shopUnpackSystem import ShopUnpackSystem
from Systems.spatial_system import SpatialSystem
from Systems.system_set import SystemSet
from Systems.transaction_system import TransactionSystem

import objects.item
from gamedata.weapons import weapons
from gamedata.upgrades import upgrades


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
    import numpy.random
    from math import floor

    gold_ore = objects.item.get_item_by_name(session, 'gold ore').static_copy()
    silver_ore = objects.item.get_item_by_name(
        session, 'silver ore').static_copy()
    iron_ore = objects.item.get_item_by_name(session, 'iron ore').static_copy()

    # for i in range(100000):
    #     x = math.floor(random.random() * 10000000 - 5000000)
    #     y = math.floor(random.random() * 10000000 - 5000000)

    for i in range(200):

        x_pos = 10000 + int(floor(numpy.random.normal(scale=1000.0)))
        y_pos = int(floor(numpy.random.normal(scale=2000.0)))
        # rot = int(floor(numpy.random.rand() * 2 * math.pi))
        size = max(50, 50 + int(floor(numpy.random.normal(scale=50))))

        node_factory.create_new_node({
            "type": {"type": "asteroid"},
            "area": {"radius": size},
            "position": {"x": x_pos, "y": y_pos},
            "rotation": {"rotation": 0},
            "velocity": {"x": 0.00, "y": 0.00},
            "collidable": {},
            'force': {},
            'acceleration': {},
            # 'mass': {},
            'server_updated': {},
            'physics_update': {},
            'state_history': {},
            'minable': {"products": [iron_ore] * 100 + [silver_ore] * 10 + [gold_ore] * 1}

        })

    def test_script(trigger_node):
        import random
        import math
        logging.info("Triggered")
        ships = []
        for i in range(10):
            trigger_node.add_or_attach_component("position", {"x": 0, "y": 0})

            x_pos = trigger_node.position.x + i * 30
            y_pos = trigger_node.position.y + i * 30

            spawn_pos_x = x_pos + \
                math.sin(random.random() * 4 * math.pi) * 1000
            spawn_pos_y = y_pos + \
                math.cos(random.random() * 4 * math.pi) * 1000

            logging.info(f"{x_pos}, {y_pos}")

            ship = node_factory.create_new_node({
                "type": {"type": "ship"},
                "area": {"radius": 10},
                "position": {"x": spawn_pos_x, "y": spawn_pos_y},
                "rotation": {"rotation": 0},
                "velocity": {"x": 0, "y": 0},
                'force': {},
                'acceleration': {},
                'mass': {},
                'physics_update': {},
                'shoot_at_target': {},
                'avoid_shooting_allies': {},
                'player_proximity_target_behaviour': {},
                'orient_towards_target': {},
                'home': {"x": x_pos, "y": y_pos},
                'ai_return_home': {},
                'health': {'health': 100, 'max_health': 100},
                'collidable': {},
                'collision_movement': {},
                'allies': {'team': 'alpha'},
                'weapon': {'type': 'triple_shot'}
            })
            ships.append(ship)

    for i in range(100):
        x_pos = 10000 + floor(numpy.random.normal(scale=1000.0))
        y_pos = floor(numpy.random.normal(scale=2000.0))
        initial_cooldown = 0  # 3600000 * numpy.random.rand()

        node_factory.create_new_node({
            "area": {"radius": 100},
            "position": {"x": x_pos, "y": y_pos},
            # "type": {"type": "bolfenn"},
            "velocity": {"x": 0, "y": 0},  # Needed to pick up proximity
            "event": {"script": test_script, "cooldown": 3600000, "initial_cooldown": initial_cooldown},
            "event_proximity_trigger": {}
        })


def collision_test(node_factory, session):

    def create_asteroids(node):
        logging.info("CREATED ASTEROIDS")
        node_factory.create_new_node({
            "type": {"type": "asteroid"},
            "area": {"radius": 50},
            "position": {"x": 200, "y": 100},
            "rotation": {"rotation": 0},
            "velocity": {"x": -0.25, "y": 0.00},
            "collidable": {},
            'force': {},
            'acceleration': {},
            # 'mass': {"mass":100},
            'server_updated': {},
            'physics_update': {},
            'state_history': {},

        })

        node_factory.create_new_node({
            "type": {"type": "asteroid"},
            "area": {"radius": 50},
            "position": {"x": -200, "y": 90},
            "rotation": {"rotation": 0},
            "velocity": {"x": 0.25, "y": 0.00},
            "collidable": {},
            'force': {},
            'acceleration': {},
            # 'mass': {"mass":100},
            'server_updated': {},
            'physics_update': {},
            'state_history': {},

        })

    node_factory.create_new_node({
        "area": {"radius": 200},
        "position": {"x": 0, "y": 400},
        # "type": {"type": "bolfenn"},
        "velocity": {"x": 0, "y": 0},  # Needed to pick up proximity
        "event": {"script": create_asteroids, "cooldown": 30000, "initial_cooldown": 0},
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
    shoot = ShootingSystem(node_factory, weapons)
    movetrack = MovementTrackingSystem(node_factory)
    spatial = SpatialSystem(node_factory)
    proximity = ProximitySystem(node_factory)
    collision = CollisionSystem(node_factory)
    collision_vel_dam = CollisionVelocityDamageSystem(node_factory)
    collision_dam = CollisionDamageSystem(node_factory)
    player_death = PlayerDeathSystem(node_factory)
    death = DeathSystem(node_factory)
    pickup = PickupSystem(node_factory)
    coll_mov = CollisionMovementSystem(node_factory)
    boundary = BoundarySystem(node_factory)
    mining = MiningSystem(node_factory)
    transaction = TransactionSystem(node_factory)
    processor = ProcessorSystem(node_factory)
    proxy_target = ProximityTargetSystem(node_factory)
    player_proxy_target = PlayerProximityTargetSystem(node_factory)
    ai_return_home = AIReturnHomeSystem(node_factory)
    ai_orient_tow_tar = AIOrientTowardsTargetSystem(node_factory)
    ai_shootat_tar = AIShootAtTargetSystem(node_factory)
    ai_avoid_shooting_allies = AIAvoidShootingAlliesSystem(node_factory)
    impulse = ImpulseSystem(node_factory)
    event_proxy = EventProximityTriggerSystem(node_factory)
    event_active = EventActiveSystem(node_factory)
    apply_upgrades = ApplyUpgradeSystem(node_factory, upgrades)
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
    system_set.register(movetrack)
    system_set.register(spatial)
    system_set.register(proximity)
    system_set.register(collision)
    system_set.register(collision_dam)
    system_set.register(collision_vel_dam)
    system_set.register(player_death)
    system_set.register(death)
    system_set.register(pickup)
    system_set.register(coll_mov)
    system_set.register(boundary)
    system_set.register(mining)
    system_set.register(transaction)
    system_set.register(processor)
    system_set.register(proxy_target)
    system_set.register(player_proxy_target)
    system_set.register(ai_orient_tow_tar)
    system_set.register(ai_return_home)
    system_set.register(ai_shootat_tar)
    system_set.register(ai_avoid_shooting_allies)
    system_set.register(impulse)
    system_set.register(event_proxy)
    system_set.register(event_active)
    system_set.register(coll_sink)
    system_set.register(apply_upgrades)
    system_set.register(game_state_req)

    return system_set
