'''
Created on 2013-11-03

@author: Nich
'''

from model.base import Base
from sqlalchemy import Column, String, Integer, ForeignKey, PickleType, Boolean
from sqlalchemy.orm import relationship, backref


class NetworkMessages(object):

    def __init__(self, entity_id):
        self.entity_id = entity_id
        self.msg = []

    def send(self, text):
        import Systems.NetworkMessageSystem as NetMes
        message = NetMes.NetworkMessage(self.entity_id, text)
        self.msg.append(message)


class PlayerControlled(Base):
    __compname__ = "player_controlled"
    __tablename__ = "player_controlled"
    id = Column(Integer, primary_key=True)

    entity_id = Column(String, ForeignKey("entity.id"))
    pid = Column(String)

    def __init__(self, entity_id, pid=0):
        self.entity_id = entity_id
        self.pid = pid


class PlayerInput():

    def __init__(self, entity_id, data=None):
        self.entity_id = entity_id
        self.data = [] if data is None else data


class Position():

    def __init__(self, entity_id, x=0, y=0):
        self.entity_id = entity_id
        self.x = x
        self.y = y


class Sector():
    '''
    A sector is position / 2500
    neightbours has the list of all entities in the sector
    '''

    def __init__(self, entity_id, sx, sy, neighbours):
        self.entity_id = entity_id
        self.sx = sx
        self.sy = sy
        self.neighbours = neighbours


class Shop():

    def __init__(self, entity_id, shop_data):
        self.entity_id = entity_id
        self.shop_data = shop_data


class Velocity():

    def __init__(self, entity_id, x=0, y=0):
        self.entity_id = entity_id
        self.x = x
        self.y = y


class Acceleration():

    def __init__(self, entity_id, x=0, y=0):
        self.entity_id = entity_id
        self.x = x
        self.y = y


class Force():

    def __init__(self, entity_id, x=0, y=0):
        self.entity_id = entity_id
        self.x = x
        self.y = y


class Rotation():

    def __init__(self, entity_id, rotation=0):
        self.entity_id = entity_id
        self.rotation = rotation


class Mass():

    def __init__(self, entity_id, mass=200):
        self.entity_id = entity_id
        self.mass = mass


class Type():

    def __init__(self, entity_id, type):
        self.entity_id = entity_id
        self.type = type


class PhysicsUpdate():

    def __init__(self, entity_id, last_update=None):
        self.entity_id = entity_id
        import time
        self.last_update = time.time() * 1000 if last_update is None else last_update
        self.packets = []


class GameStateRequest():

    def __init__(self, entity_id):
        self.entity_id = entity_id


class Shooting():

    def __init__(self, entity_id, time):
        self.entity_id = entity_id
        self.time = time


class ServerUpdated():

    def __init__(self, entity_id):
        self.entity_id = entity_id


class StateHistory():

    def __init__(self, entity_id):
        self.entity_id = entity_id
        self.history = []


class Camera():

    def __init__(self, entity_id, radius):
        self.new_entities = {}
        self.tracked_entites = {}
        self.leaving_entities = {}
        self.radius = radius
        self.entity_id = entity_id


class Renderable():

    def __init__(self, entity_id):
        self.entity_id = entity_id


components = {
    "acceleration": Acceleration,
    "force": Force,
    "game_state_request": GameStateRequest,
    "mass": Mass,
    "network_messages": NetworkMessages,
    "physics_update": PhysicsUpdate,
    "player_input": PlayerInput,
    "position": Position,
    "server_updated": ServerUpdated,
    "shooting": Shooting,
    "state_history": StateHistory,
    "type": Type,
    "rotation": Rotation,
    "velocity": Velocity,
    "camera": Camera,
    "renderable": Renderable,
    "shop": Shop,
    "sector": Sector
}

db_components = {
    "player_controlled": PlayerControlled
}
