'''
Created on 2013-11-03

@author: Nich
'''

from model.base import Base
from sqlalchemy import Column, String, Integer, ForeignKey, PickleType, Boolean
from sqlalchemy.orm import relationship, backref
from objects.materials import materials


class AVEvents(object):

    def __init__(self, entity_id):
        self.entity_id = entity_id
        self.events = []


class AVMessages(object):

    def __init__(self, entity_id):
        self.entity_id = entity_id
        self.msg = []


class NetworkMessages(object):

    def __init__(self, entity_id):
        self.entity_id = entity_id
        self.msg = []


class VisibleObjects(object):

    def __init__(self, entity_id):
        self.entity_id = entity_id
        self.objects = []


class VisibleNames(object):

    def __init__(self, entity_id):
        self.entity_id = entity_id
        self.names = []
        self.ids = []


class Activating(object):

    def __init__(self, entity_id, format, target=None):
        self.entity_id = entity_id
        self.target = target
        self.format = format


class Looking(object):

    def __init__(self, entity_id, target=None):
        self.entity_id = entity_id
        self.target = target


class Changing(object):

    def __init__(self, entity_id, text, target):
        self.entity_id = entity_id
        self.text = text
        self.target = target


class Speaking(object):

    def __init__(self, entity_id, text, target, format):
        self.entity_id = entity_id
        self.text = text
        self.target = target
        self.format = format


class Creating(object):

    def __init__(self, entity_id, format, new_name):
        self.entity_id = entity_id
        self.format = format
        self.name = new_name


class Writing(object):

    def __init__(self, entity_id, format, target, rune):
        self.entity_id = entity_id
        self.format = format
        self.rune = rune
        self.target = target


class Moving(object):

    def __init__(self, entity_id, target, format):
        self.entity_id = entity_id
        self.target = target
        self.format = format


class Exiting(object):

    def __init__(self, entity_id, target):
        self.entity_id = entity_id
        self.target = target


class Entering(object):

    def __init__(self, entity_id, target):
        self.entity_id = entity_id
        self.target = target


class Projectile(object):

    def __init__(self, entity_id, on_hit, args, timeout=60):
        self.entity_id = entity_id
        self.on_hit = on_hit
        self.args = args
        self.timeout = timeout
        self.last_trigger = None


class Dodging(object):

    def __init__(self, entity_id, format, timeout=60):
        self.entity_id = entity_id
        self.format = format
        self.timeout = timeout
        self.last_trigger = None


class Ascending(object):

    def __init__(self, entity_id):
        self.entity_id = entity_id


class Runes(Base):
    __compname__ = "runes"
    __tablename__ = "runes"

    id = Column(Integer, primary_key=True)
    entity_id = Column(String, ForeignKey("entity.id"))
    active = Column(Boolean)
    runes_list = Column(PickleType)

    def __init__(self, entity_id, active, runes_list=None):
        self.entity_id = entity_id
        self.active = active
        self.runes_list = [] if runes_list is None else runes_list


class RuneData():

    def __init__(self, entity_id, runes, covered):
        self.entity_id = entity_id
        self.runes = runes
        self.rune_position = 0
        self.rune_number = 0
        self.covered = covered
        self.context = {}


class RuneActive():

    def __init__(self, entity_id):
        self.entity_id = entity_id


class OnHold(Base):
    __compname__ = "on_hold"
    __tablename__ = "on_hold"

    id = Column(Integer, primary_key=True)
    entity_id = Column(String, ForeignKey("entity.id"))
    callback = Column(String)
    timeout = Column(Integer)
    data = Column(PickleType)

    def __init__(self, entity_id, callback, timeout=0, data=None):
        self.entity_id = entity_id
        self.callback = callback
        self.timeout = timeout
        self.data = {} if data is None else data


class OnHoldTimeout(object):

    def __init__(self, entity_id, last_trigger):
        self.entity_id = entity_id
        self.last_trigger = last_trigger


class Taking(object):

    def __init__(self, entity_id, target, format):
        self.entity_id = entity_id
        self.target = target
        self.format = format


class Putting(object):

    def __init__(self, entity_id, targets, type, format):
        self.entity_id = entity_id
        self.targets = targets
        self.format = format
        self.type = type


class Dropping(object):

    def __init__(self, entity_id, target, format):
        self.entity_id = entity_id
        self.target = target
        self.format = format


class Exit(Base):
    __compname__ = "exit"
    __tablename__ = "exit"

    id = Column(Integer, primary_key=True)
    entity_id = Column(String, ForeignKey("entity.id"))
    dest_id = Column(String)

    def __init__(self, entity_id, dest_id):
        self.entity_id = entity_id
        self.dest_id = dest_id


class DetatchedLocation(object):

    def __init__(self, entity_id, room):
        self.entity_id = entity_id
        self.room = room


class Location(Base):
    __compname__ = "location"
    __tablename__ = "location"

    id = Column(Integer, primary_key=True)
    entity_id = Column(String, ForeignKey("entity.id"))
    room = Column(Integer)

    x = Column(Integer)
    y = Column(Integer)
    z = Column(Integer)

    def __init__(self, entity_id, room=0):
        self.entity_id = entity_id
        self.room = room

    def detach(self):
        return DetatchedLocation(self.entity_id, self.room)


class Size(Base):
    __compname__ = "size"
    __tablename__ = "size"

    id = Column(Integer, primary_key=True)
    entity_id = Column(String, ForeignKey("entity.id"))
    qty = Column(Integer)

    def __init__(self, entity_id, qty):
        self.entity_id = entity_id
        self.qty = qty


class Capacity(Base):
    __compname__ = "capacity"
    __tablename__ = "capacity"

    id = Column(Integer, primary_key=True)
    entity_id = Column(String, ForeignKey("entity.id"))
    n_in = Column(Integer)
    n_on = Column(Integer)
    n_under = Column(Integer)

    def __init__(self, entity_id, n_in=0, n_on=0, n_under=0):
        self.entity_id = entity_id
        self.n_in = n_in
        self.n_on = n_on
        self.n_under = n_under


class Temperature(Base):
    __compname__ = "temperature"
    __tablename__ = "temperature"

    id = Column(Integer, primary_key=True)
    entity_id = Column(String, ForeignKey("entity.id"))
    temperature = Column(Integer)

    def __init__(self, entity_id, temperature=0):
        self.entity_id = entity_id
        self.temperature = temperature


class Names(Base):
    __compname__ = "names"
    __tablename__ = "names"
    id = Column(Integer, primary_key=True)
    entity_id = Column(String, ForeignKey("entity.id"))
    name = Column(String)
    identifiers = Column(String)

    def __init__(self, entity_id, name="temp_name", identifiers="foo bar baz"):
        self.name = name
        self.entity_id = entity_id
        self.identifiers = identifiers

    def __repr__(self):
        return "<" + self.name + ">"


class Type(Base):
    __compname__ = "type"
    __tablename__ = "type"
    id = Column(Integer, primary_key=True)
    entity_id = Column(String, ForeignKey("entity.id"))
    type = Column(String)

    def __init__(self, entity_id, type="temp_type"):
        self.entity_id = entity_id
        self.type = type


class CloseTo(Base):
    __compname__ = "close_to"
    __tablename__ = "close_to"
    id = Column(Integer, primary_key=True)
    entity_id = Column(String, ForeignKey("entity.id"))
    n_id = Column(String, ForeignKey("entity.id"))

    def __init__(self, entity_id, n_id):
        self.entity_id = entity_id
        self.n_id = n_id


class AvatarType(Base):
    __compname__ = "avatar_type"
    __tablename__ = "avatar_type"
    id = Column(Integer, primary_key=True)
    entity_id = Column(String, ForeignKey("entity.id"))

    def __init__(self, entity_id):
        self.entity_id = entity_id


class PlayerControlled(Base):
    __compname__ = "player_controlled"
    __tablename__ = "player_controlled"
    id = Column(Integer, primary_key=True)

    entity_id = Column(String, ForeignKey("entity.id"))
    pid = Column(String)

    def __init__(self, entity_id, pid=0):
        self.entity_id = entity_id
        self.pid = pid


class Senses(Base):
    __compname__ = "senses"
    __tablename__ = "senses"

    id = Column(Integer, primary_key=True)
    entity_id = Column(String, ForeignKey("entity.id"))
    sight = Column(Integer)
    hearing = Column(Integer)

    def __init__(self, entity_id, sight=20, hearing=30):
        self.entity_id = entity_id
        self.sight = sight
        self.hearing = hearing


class Material(Base):
    __compname__ = "material"
    __tablename__ = "material"

    id = Column(Integer, primary_key=True)
    entity_id = Column(String, ForeignKey("entity.id"))
    material_id = Column(Integer)

    def __init__(self, entity_id, material_id):
        self.entity_id = entity_id
        self.material_id = material_id

    def get_material(self):
        return materials.items[self.material_id]

    def __repr__(self):
        return str(self.get_material())


class Health(Base):
    __compname__ = "health"
    __tablename__ = "health"

    id = Column(Integer, primary_key=True)
    entity_id = Column(String, ForeignKey("entity.id"))
    health = Column(Integer)
    max_health = Column(Integer)

    def __init__(self, entity_id, health=None, max_health=100):
        self.entity_id = entity_id
        self.health = max_health if health is None else health
        self.max_health = max_health


class Mana(Base):
    __compname__ = "mana"
    __tablename__ = "mana"

    id = Column(Integer, primary_key=True)
    entity_id = Column(String, ForeignKey("entity.id"))
    mana = Column(Integer)
    max_mana = Column(Integer)

    def __init__(self, entity_id, mana=None, max_mana=100):
        self.entity_id = entity_id
        self.mana = max_mana if mana is None else mana
        self.max_mana = max_mana


class ChangeHealth(object):

    def __init__(self, entity_id, amount=0):
        self.entity_id = entity_id
        self.amount = amount


class Container(Base):

    __tablename__ = 'container'
    id = Column(Integer, primary_key=True)
    parent_id = Column(Integer, ForeignKey('container.id'))
    entity_id = Column(String, ForeignKey("entity.id"))
    type = Column(String)  # in, on, under
    children = relationship("Container",
                            backref=backref('parent', remote_side=[id])
                            )

    def __init__(self, entity_id, parent_id=0, type="in"):
        self.entity_id = entity_id
        self.parent_id = parent_id
        self.type = type

    def __repr__(self):
        return "{}: {}".format(self.id, self.children)


components = {
    "activating": Activating,
    "ascending": Ascending,
    "av_events": AVEvents,
    "av_messages": AVMessages,
    "changing": Changing,
    "change_health": ChangeHealth,
    "creating": Creating,
    "dodging": Dodging,
    "dropping": Dropping,
    "entering": Entering,
    "exiting": Exiting,
    "looking": Looking,
    "moving": Moving,
    "network_messages": NetworkMessages,
    "on_hold_timeout": OnHoldTimeout,
    "projectile": Projectile,
    "putting": Putting,
    "rune_active": RuneActive,
    "rune_data": RuneData,
    "speaking": Speaking,
    "taking": Taking,
    "visible_names": VisibleNames,
    "visible_objects": VisibleObjects,
    "writing": Writing,
}

db_components = {
    "avatar_type": AvatarType,
    "close_to": CloseTo,
    "container": Container,
    "exit": Exit,
    "health": Health,
    "location": Location,
    "mana": Mana,
    "material": Material,
    "names": Names,
    "on_hold": OnHold,
    "player_controlled": PlayerControlled,
    "runes": Runes,
    "senses": Senses,
    "temperature": Temperature,
    "type": Type,
}
