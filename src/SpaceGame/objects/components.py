'''
Created on 2013-11-03

@author: Nich
'''

from model.base import Base
from sqlalchemy import Column, String, Integer, Float, ForeignKey, PickleType, Boolean
from sqlalchemy.orm import relationship, backref
import time


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


class DBPosition(Base):
    __compname__ = "db_position"
    __tablename__ = "db_position"
    id = Column(Integer, primary_key=True)
    entity_id = Column(String, ForeignKey("entity.id"))
    x = Column(Float)
    y = Column(Float)

    def __init__(self, entity_id, x, y):
        self.entity_id = entity_id
        self.x = x
        self.y = y


class Persisted():

    def __init__(entity_id, persisted_properties=None):
        self.entity_id = entity_id
        # PersistedProperties is a dict mapping component name to the name of
        # the db_component that persists it
        self.persisted_properties = {} if persisted_properties == None else persisted_properties


class InstanceComponents(Base):
    __compname__ = "instance_components"
    __tablename__ = "instance_components"

    id = Column(Integer, primary_key=True)
    entity_id = Column(String, ForeignKey("entity.id"))
    components = Column(String)

    def __init__(self, entity_id, components="{}"):
        self.entity_id = entity_id
        self.components = components


class Position():

    def __init__(self, entity_id, x=0, y=0):
        self.entity_id = entity_id
        self.x = x
        self.y = y


class Area():

    def __init__(self, entity_id, radius):
        self.entity_id = entity_id
        self.radius = radius


class Collidable():

    def __init__(self, entity_id):
        self.entity_id = entity_id


class Pickup():

    def __init__(self, entity_id, item_id, qty):
        self.entity_id = entity_id
        self.item_id = item_id
        self.qty = qty


class Colliding():

    def __init__(self, entity_id, collisions):
        self.entity_id = entity_id
        self.collisions = [] if not collisions else collisions


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


class ShopSpec():

    def __init__(self, entity_id, shop_data):
        self.entity_id = entity_id
        self.shop_data = shop_data


class Money():

    def __init__(self, entity_id, money):
        self.entity_id = entity_id
        self.money = money


class Inventory():

    def __init__(self, entity_id, inventory):
        self.entity_id = entity_id
        self.inv = inventory


class InventoryMass():

    def __init__(self, entity_id, inventory_mass=0):
        self.entity_id = entity_id
        self.inventory_mass = inventory_mass


class Transaction():

    def __init__(self, entity_id, transactions):
        self.entity_id = entity_id
        self.transactions = transactions


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

    def __init__(self, entity_id, firing_rate, inputs=None):
        self.entity_id = entity_id
        self.inputs = inputs if not inputs is None else []
        self.firing_rate = firing_rate

class ShootingVars():
    def __init__(self, entity_id):
        self.entity_id = entity_id
        self.last_update = time.time() * 1000
        self.bullets_fired = 0
        self.residual_cooldown = None #Make none to use firing rate as a default since 0 is valid


class Mining():

    def __init__(self, entity_id, time):
        self.entity_id = entity_id
        self.time = time


class Minable():

    def __init__(self, entity_id, products):
        self.entity_id = entity_id
        self.products = products


class Proximity():

    def __init__(self, entity_id, proximity_map=None):
        self.entity_id = entity_id
        self.proximity_map = {} if proximity_map is None else proximity_map


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


class Processor():

    def __init__(self, entity_id, processes, last_update=None):
        self.entity_id = entity_id
        self.processes = processes
        self.last_update = time.time() * 1000 if last_update is None else last_update


class Expires():

    def __init__(self, entity_id, expiry_time_ms, creation_time):
        self.entity_id = entity_id
        self.expiry_time_ms = expiry_time_ms
        self.creation_time = creation_time


class Target():

    def __init__(self, entity_id, target_id):
        self.entity_id = entity_id
        self.id = target_id


class OrientTowardsTarget():

    def __init__(self, entity_id):
        self.entity_id = entity_id


class ProximityTargetBehaviour():

    def __init__(self, entity_id):
        self.entity_id = entity_id


class Health():

    def __init__(self, entity_id, health, max_health):
        self.entity_id = entity_id
        self.health = health
        self.max_health = max_health


class CollisionDamage():

    def __init__(self, entity_id, damage):
        self.entity_id = entity_id
        self.damage = damage


class ClientSync():

    def __init__(self, entity_id, sync_key):
        self.entity_id = entity_id
        self.sync_key = sync_key


components = {
    "acceleration": Acceleration,
    "area": Area,
    "camera": Camera,
    "collidable": Collidable,
    "colliding": Colliding,
    "expires": Expires,
    "force": Force,
    "game_state_request": GameStateRequest,
    "inventory": Inventory,
    "inventory_mass": InventoryMass,
    "mass": Mass,
    "minable": Minable,
    "mining": Mining,
    "money": Money,
    "network_messages": NetworkMessages,
    "persisted": Persisted,
    "physics_update": PhysicsUpdate,
    "pickup": Pickup,
    "player_controlled": PlayerControlled,
    "player_input": PlayerInput,
    "position": Position,
    "processor": Processor,
    "proximity": Proximity,
    "renderable": Renderable,
    "rotation": Rotation,
    "sector": Sector,
    "server_updated": ServerUpdated,
    "shooting": Shooting,
    "shooting_vars": ShootingVars,
    "shop": Shop,
    "shop_spec": ShopSpec,
    "state_history": StateHistory,
    "transaction": Transaction,
    "type": Type,
    "velocity": Velocity,
    "target": Target,
    "orient_towards_target": OrientTowardsTarget,
    "proximity_target_behaviour": ProximityTargetBehaviour,
    "health": Health,
    "collision_damage": CollisionDamage,
    "client_sync": ClientSync
}

db_components = {
    "instance_components": InstanceComponents,
    "db_position": DBPosition
}
