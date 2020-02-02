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


# class Sector():
#     '''
#     A sector is position / 2500
#     neightbours has the list of all entities in the sector
#     '''

#     def __init__(self, entity_id, sx, sy, fx, fy, neighbours, fine_neighbours):
#         self.entity_id = entity_id
#         self.sx = sx
#         self.sy = sy
#         self.fx = fx
#         self.fy = fy
#         self.neighbours = neighbours
#         self.fine_neighbours = fine_neighbours


class SectorsCoarse():

    def __init__(self, entity_id, sector_rect):
        self.entity_id = entity_id
        self.sector_rect = sector_rect


class SectorsFine():

    def __init__(self, entity_id, sector_rect):
        self.entity_id = entity_id
        self.sector_rect = sector_rect


class NeighboursCoarse():

    def __init__(self, entity_id, neighbours=None):
        self.entity_id = entity_id
        self.neighbours = set() if neighbours is None else neighbours


class NeighboursFine():

    def __init__(self, entity_id, neighbours=None):
        self.entity_id = entity_id
        self.neighbours = set() if neighbours is None else neighbours


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
        self.inventory = inventory


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


class Thrust():

    def __init__(self, entity_id, thrust):
        self.entity_id = entity_id
        self.thrust = thrust


class Rotation():

    def __init__(self, entity_id, rotation=0):
        self.entity_id = entity_id
        self.rotation = rotation


class RotationalVelocity():

    def __init__(self, entity_id, vel):
        self.entity_id = entity_id
        self.vel = vel


class Mass():

    def __init__(self, entity_id, mass=200):
        self.entity_id = entity_id
        self.mass = mass


class Type():

    def __init__(self, entity_id, type):
        self.entity_id = entity_id
        self.type = type


class PhysicsUpdate():

    def __init__(self, entity_id, last_update=None, packets=None):
        self.entity_id = entity_id
        import time
        self.last_update = time.time() * 1000 if last_update is None else last_update
        self.packets = [] if packets is None else packets


class GameStateRequest():

    def __init__(self, entity_id):
        self.entity_id = entity_id


class Shooting():

    def __init__(self, entity_id, inputs=None):
        self.entity_id = entity_id
        self.inputs = inputs if not inputs is None else []


class ShootingVars():

    def __init__(self, entity_id):
        self.entity_id = entity_id
        self.last_update = time.time() * 1000
        self.bullets_fired = 0
        # Make none to use firing rate as a default since 0 is valid
        self.residual_cooldown = None


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

    def __init__(self, entity_id, history=None):
        self.entity_id = entity_id
        self.history = [] if history is None else history


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


class ShootAtTarget():

    def __init__(self, entity_id, firing_angle=5):
        self.entity_id = entity_id
        self.firing_angle = firing_angle


class ProximityTargetBehaviour():

    def __init__(self, entity_id, exclusion_list=None):
        self.entity_id = entity_id
        self.exclusion_list = [] if exclusion_list is None else exclusion_list


class PlayerProximityTargetBehaviour():

    def __init__(self, entity_id):
        self.entity_id = entity_id


class Health():

    def __init__(self, entity_id, health, max_health, base_health=None):
        self.entity_id = entity_id
        self.health = health
        self.max_health = max_health
        self.base_health = max_health if base_health is None else base_health


class CollisionDamage():

    def __init__(self, entity_id, damage):
        self.entity_id = entity_id
        self.damage = damage


class CollisionVelocityDamage():

    def __init__(self, entity_id, damage, min_velocity=0, max_velocity=100):
        self.entity_id = entity_id
        self.damage = damage
        self.min_velocity = min_velocity
        self.max_velocity = max_velocity


class CollisionMovement():

    def __init__(self, entity_id):
        self.entity_id = entity_id


class ClientSync():

    def __init__(self, entity_id, sync_key):
        self.entity_id = entity_id
        self.sync_key = sync_key


class Animated():

    def __init__(self, entity_id, update_rate):
        self.entity_id = entity_id
        self.update_rate = update_rate


class Event():

    def __init__(self, entity_id, script, cooldown, initial_cooldown=0, random_cooldown=False):
        self.entity_id = entity_id
        self.script = script
        self.cooldown = initial_cooldown
        self.cooldown_time = cooldown
        self.random_cooldown = random_cooldown


class EventActive():

    def __init__(self, entity_id):
        self.entity_id = entity_id
        self.triggerer = None


class EventProximityTrigger():

    def __init__(self, entity_id):
        self.entity_id = entity_id


class NoSync():

    def __init__(self, entity_id):
        self.entity_id = entity_id


class Moved():

    def __init__(self, entity_id):
        self.entity_id = entity_id


class Impulses():

    def __init__(self, entity_id):
        self.entity_id = entity_id
        self.left = 0
        self.right = 0
        self.shoot = 0
        self.thrust = 0
        self.mine = 0
        self.brake = 0


class Allies():

    def __init__(self, entity_id, team):
        self.entity_id = entity_id
        self.team = team


class NoTargetAllies():

    def __init__(self, entity_id):
        self.entity_id = entity_id


class Home():

    def __init__(self, entity_id, x, y):
        self.entity_id = entity_id
        self.x = x
        self.y = y


class AIReturnHome():

    def __init__(self, entity_id):
        self.entity_id = entity_id


class AvoidShootingAllies():

    def __init__(self, entity_id):
        self.entity_id = entity_id


class AppliedUpgrades():
    # Upgrades are stored as key:data, where the key looks up the function and
    # the function is called with node, data

    def __init__(self, entity_id, upgrades=None):
        self.entity_id = entity_id
        self.upgrades = {} if upgrades is None else upgrades


class ApplyUpgrade():

    def __init__(self, entity_id, upgrade_name, upgrade_id):
        self.entity_id = entity_id
        self.upgrade_id = upgrade_id
        self.upgrade_name = upgrade_name


class Weapon():

    def __init__(self, entity_id, type, firing_rate=200):
        self.entity_id = entity_id
        self.type = type
        self.firing_rate = firing_rate


class Dead():

    def __init__(self, entity_id):
        self.entity_id = entity_id


class Updated():

    def __init__(self, entity_id):
        self.entity_id = entity_id


class Bought():

    def __init__(self, entity_id, item_id, qty):
        self.entity_id = entity_id
        self.item_id = item_id
        self.qty = qty


class Sold():

    def __init__(self, entity_id, item_id, qty):
        self.entity_id = entity_id
        self.item_id = item_id
        self.qty = qty


class ActiveQuests():

    def __init__(self, entity_id):
        self.entity_id = entity_id
        self.quests = {}


class QuestStatusUpdated():

    def __init__(self, entity_id, quest, stage):
        self.entity_id = entity_id
        self.quest = quest
        self.stage = stage


class Quests():

    def __init__(self, entity_id, quests=None):
        self.entity_id = entity_id
        self.quests = {} if quests == None else quests


class TrackedIds():

    def __init__(self, entity_id, ids=None):
        self.entity_id = entity_id
        self.ids = ids if ids is not None else []


class DropOnDeath():

    def __init__(self, entity_id, products, qty):
        self.entity_id = entity_id
        self.products = products
        self.qty = qty


class Rooted():

    def __init__(self, entity_id):
        self.entity_id = entity_id


class PingNeighbours():

    def __init__(self, entity_id):
        self.entity_id = entity_id


class Attached():

    def __init__(self, entity_id, target_id, x=0, y=0, rotation=0):
        self.entity_id = entity_id
        self.target_id = target_id
        self.x = x
        self.y = y
        self.rotation = rotation


class IgnoreCollisions():

    def __init__(self, entity_id, ids=None):
        self.entity_id = entity_id
        self.ids = [] if ids is None else ids


class Beam():

    def __init__(self, entity_id, length, width):
        self.entity_id = entity_id
        self.length = length
        self.width = width


class Charging():

    def __init__(self, entity_id, charge_time=0):
        self.entity_id = entity_id
        self.charge_time = charge_time


class Charged():

    def __init__(self, entity_id, charge_time=0):
        self.entity_id = entity_id
        self.charge_time = charge_time


class Damaged():

    def __init__(self, entity_id, amount):
        self.entity_id = entity_id
        self.amount = amount


class Respawn():

    def __init__(self, entity_id, respawn_time, spec):
        self.entity_id = entity_id
        self.respawn_time = respawn_time
        self.spec = spec


class Spawn():

    def __init__(self, entity_id, start_time):
        self.entity_id = entity_id
        self.start_time = start_time

components = {
    "acceleration": Acceleration,
    "active_quests": ActiveQuests,
    "ai_return_home": AIReturnHome,
    "allies": Allies,
    "animated": Animated,
    "applied_upgrades": AppliedUpgrades,
    "apply_upgrade": ApplyUpgrade,
    "area": Area,
    "attached": Attached,
    "avoid_shooting_allies": AvoidShootingAllies,
    "bought": Bought,
    "beam": Beam,
    "camera": Camera,
    "charging": Charging,
    "charged": Charged,
    "client_sync": ClientSync,
    "collidable": Collidable,
    "colliding": Colliding,
    "collision_damage": CollisionDamage,
    "collision_movement": CollisionMovement,
    "collision_velocity_damage": CollisionVelocityDamage,
    "damaged": Damaged,
    "dead": Dead,
    "drop_on_death": DropOnDeath,
    "event": Event,
    "event_active": EventActive,
    "event_proximity_trigger": EventProximityTrigger,
    "expires": Expires,
    "force": Force,
    "game_state_request": GameStateRequest,
    "health": Health,
    "home": Home,
    "ignore_collisions": IgnoreCollisions,
    "impulses": Impulses,
    "inventory": Inventory,
    "inventory_mass": InventoryMass,
    "mass": Mass,
    "minable": Minable,
    "mining": Mining,
    "money": Money,
    "moved": Moved,
    "network_messages": NetworkMessages,
    "no_sync": NoSync,
    "no_target_allies": NoTargetAllies,
    "orient_towards_target": OrientTowardsTarget,
    "persisted": Persisted,
    "physics_update": PhysicsUpdate,
    "pickup": Pickup,
    "ping_neighbours": PingNeighbours,
    "player_controlled": PlayerControlled,
    "player_input": PlayerInput,
    "player_proximity_target_behaviour": PlayerProximityTargetBehaviour,
    "proximity_target_behaviour": ProximityTargetBehaviour,
    "position": Position,
    "processor": Processor,
    "proximity": Proximity,
    "quests": Quests,
    "quest_status_updated": QuestStatusUpdated,
    "renderable": Renderable,
    "respawn": Respawn,
    "rotation": Rotation,
    "rotational_velocity": RotationalVelocity,
    "sectors_coarse": SectorsCoarse,
    "sectors_fine": SectorsFine,
    "server_updated": ServerUpdated,
    "shoot_at_target": ShootAtTarget,
    "shooting": Shooting,
    "shooting_vars": ShootingVars,
    "shop": Shop,
    "shop_spec": ShopSpec,
    "sold": Sold,
    "spawn": Spawn,
    "state_history": StateHistory,
    "target": Target,
    "thrust": Thrust,
    "transaction": Transaction,
    "tracked_ids": TrackedIds,
    "type": Type,
    "updated": Updated,
    "velocity": Velocity,
    "weapon": Weapon,
    "neighbours_coarse": NeighboursCoarse,
    "neighbours_fine": NeighboursFine
}

db_components = {
    "instance_components": InstanceComponents,
    "db_position": DBPosition
}
