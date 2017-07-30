'''
Created on 2014-02-25

@author: Nich
'''

import model.base as base
from model.base import SessionManager
from model.account import AccountUtils

from objects.node_factory import NodeFactoryDB
from objects.components import components
from room.room_components import components as room_components

from player.avatar import AvatarFactory
from player.player import PlayerFactory
from objects.component_manager import ComponentManager, DBComponentSource, ArrayComponentSource

from Systems.NetworkMessageSystem import NetworkMessageSystem
from Systems.network_av_system import NetworkAVSystem
from Systems.SpeakingSystem import SpeakingSystem
from Systems.CastingSystem import CastingSystem
from Systems.TakingSystem import TakingSystem
from Systems.DroppingSystem import DroppingSystem
from Systems.AVEventSystem import AVEventSystem
from Systems.RoomDescriptionSystem import DescriptionSystem, NetworkDescriptionSystem
from Systems.movement_system import MovementSystem
from Systems.exit_system import ExitSystem
from Systems.system_set import DBSystemSet
from Systems.visible_things_system import VisibleThingsSystem
from Systems.names_system import NamesSystem
from Systems.creating_system import CreatingSystem
from Systems.ChangingSystem import ChangingSystem
from Systems.HoldTriggerSystem import HoldTriggerSystem


from command.command_handler import CommandHandler
from command.command_token_matcher import CommandTokenMatcher
from command.command_packager import CommandPackager
from command.command_executor import CommandExecutor
from command.command_context_builder import CommandContextBuilder
from command.commands import verbs

from spells.spells import spells


def setup_objects(all_db_components, all_components, session):
    object_db = DBComponentSource(all_db_components, session)
    object_array = ArrayComponentSource(all_components)
    component_manager = ComponentManager([object_db, object_array])
    node_factory = NodeFactoryDB(component_manager)
    player_factory = PlayerFactory(component_manager)
    default_room = "f6fcdd97-29a7-4537-9ced-b463eb32d445"
    avatar_factory = AvatarFactory(node_factory, component_manager, {
            "starting_room": default_room,
            "player_id": 0})
    account_utils = AccountUtils(avatar_factory)

    return avatar_factory, node_factory, object_db, player_factory, account_utils


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
        all_components.update(room_components)

        self.component_object = DBComponentSource(all_components)
        self.comp_manager = ComponentManager([self.component_object], Session)
        self.node_factory = NodeFactoryDB(all_components, Session)


def setup_commands(node_factory):
    command_token_matcher = CommandTokenMatcher()
    command_packager = CommandPackager(verbs, spells)
    command_context_builder = CommandContextBuilder(node_factory, spells)
    command_executor = CommandExecutor()
    command_handler = CommandHandler(command_token_matcher, command_packager, command_executor, command_context_builder)
    return command_handler


def register_systems(session_manager, object_db, node_factory, player_factory):
    system_set = DBSystemSet(object_db, session_manager)
    nms = NetworkMessageSystem(node_factory, player_factory)
    speaking_system = SpeakingSystem(node_factory)
    casting_system = CastingSystem(node_factory, spells)
    taking_system = TakingSystem(node_factory)
    dropping_system = DroppingSystem(node_factory)
    hold_trigger_system = HoldTriggerSystem(node_factory)
    av_event_system = AVEventSystem(node_factory)
    nAVs = NetworkAVSystem(node_factory)
    #loc_sys = LocationSystem(node_factory)
    desc_sys = DescriptionSystem(node_factory)
    net_desc_sys = NetworkDescriptionSystem(node_factory, desc_sys)
    move_sys = MovementSystem(node_factory)
    exit_sys = ExitSystem(node_factory)
    visithing = VisibleThingsSystem(node_factory)
    names_sys = NamesSystem(node_factory)
    creating_sys = CreatingSystem(node_factory)
    changing_sys = ChangingSystem(node_factory)

    system_set.register(nms)
    system_set.register(speaking_system)
    system_set.register(casting_system)
    system_set.register(taking_system)
    system_set.register(hold_trigger_system)
    system_set.register(dropping_system)
    system_set.register(av_event_system)
    system_set.register(nAVs)
    #system_set.register(loc_sys)
    #system_set.register(desc_sys)
    system_set.register(net_desc_sys)
    system_set.register(move_sys)
    system_set.register(exit_sys)
    system_set.register(visithing)
    system_set.register(names_sys)
    system_set.register(creating_sys)
    system_set.register(changing_sys)

    #Todo: Doing these last so that the db components of each node still have a session when this is processed
    # But it would be best if that weren't the case
    #And it turns out that this doesn't consistently work anyways, so realistically you can't store references to db objects
    system_set.register(av_event_system)
    system_set.register(nAVs)

    return system_set
