'''
Created on 2014-02-25

@author: Nich
'''

import PyMud.model.base as base
from PyMud.model.base import SessionManager
from PyMud.model.account import AccountUtils

from PyMud.objects.node_factory import NodeFactoryDB
from PyMud.objects.components import components
from PyMud.room.room_components import components as room_components

from PyMud.player.avatar import AvatarFactory
from PyMud.player.player import PlayerFactory
from PyMud.objects.component_manager import ComponentManager, DBComponentSource, ArrayComponentSource

from PyMud.Systems.NetworkMessageSystem import NetworkMessageSystem
from PyMud.Systems.network_av_system import NetworkAVSystem
from PyMud.Systems.SpeakingSystem import SpeakingSystem
from PyMud.Systems.AVEventSystem import AVEventSystem
from PyMud.Systems.RoomDescriptionSystem import DescriptionSystem, NetworkDescriptionSystem
from PyMud.Systems.movement_system import MovementSystem
from PyMud.Systems.system_set import DBSystemSet
from PyMud.Systems.visible_things_system import VisibleThingsSystem
from PyMud.Systems.names_system import NamesSystem
from PyMud.Systems.creating_system import CreatingSystem


from PyMud.command.command_handler import CommandHandler
from PyMud.command.command_token_matcher import CommandTokenMatcher
from PyMud.command.command_packager import CommandPackager
from PyMud.command.command_executor import CommandExecutor
from PyMud.command.command_context_builder import CommandContextBuilder
from PyMud.command.commands import verbs



def setup_objects(all_db_components, all_components, session):
    object_db = DBComponentSource(all_db_components, session)
    object_array = ArrayComponentSource(all_components)
    component_manager = ComponentManager([object_db, object_array])
    node_factory = NodeFactoryDB(component_manager)
    player_factory = PlayerFactory(component_manager)
    default_room = "e1a62c5e-42fb-48dc-a09a-c28400f554af"
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
    command_packager = CommandPackager(verbs)
    command_context_builder = CommandContextBuilder(node_factory)
    command_executor = CommandExecutor()
    command_handler = CommandHandler(command_token_matcher, command_packager, command_executor, command_context_builder)
    return command_handler


def register_systems(session_manager, object_db, node_factory, player_factory):
    system_set = DBSystemSet(object_db, session_manager)
    nms = NetworkMessageSystem(node_factory, player_factory)
    speaking_system = SpeakingSystem(node_factory)
    av_event_system = AVEventSystem(node_factory)
    nAVs = NetworkAVSystem(node_factory)
    #loc_sys = LocationSystem(node_factory)
    desc_sys = DescriptionSystem(node_factory)
    net_desc_sys = NetworkDescriptionSystem(node_factory, desc_sys)
    move_sys = MovementSystem(node_factory)
    visithing = VisibleThingsSystem(node_factory)
    names_sys = NamesSystem(node_factory)
    creating_sys = CreatingSystem(node_factory)

    system_set.register(nms)
    system_set.register(speaking_system)
    system_set.register(av_event_system)
    system_set.register(nAVs)
    #system_set.register(loc_sys)
    #system_set.register(desc_sys)
    system_set.register(net_desc_sys)
    system_set.register(move_sys)
    system_set.register(visithing)
    system_set.register(names_sys)
    system_set.register(creating_sys)

    return system_set
