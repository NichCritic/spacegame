'''
Created on 2013-11-03

@author: Nich
'''

from model.base import Base
from sqlalchemy import Column, String, Integer, ForeignKey, PickleType, Boolean
from sqlalchemy.orm import relationship, backref, reconstructor
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

class Casting(object):

    def __init__(self, entity_id, spell, target, format):
        self.entity_id = entity_id
        self.spell = spell
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

    def __init__(self, entity_id, x, y, z):
        self.entity_id = entity_id
        self.x = x
        self.y = y
        self.z = z


class Exiting(object):

    def __init__(self, entity_id, target):
        self.entity_id = entity_id
        self.target = target

class Entering(object):

    def __init__(self, entity_id, target):
        self.entity_id = entity_id
        self.target = target

class Ascending(object):

    def __init__(self, entity_id):
        self.entity_id = entity_id

class Holding(object):

    def __init__(self, entity_id, held_entity_id):
        self.entity_id = entity_id
        self.held_entity_id = held_entity_id


class HeldBy(object):

    def __init__(self, entity_id, holding_entity_id):
        self.entity_id = entity_id
        self.holding_entity_id = holding_entity_id


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

    def __init__(self, entity_id, room, x, y, z):
        self.entity_id = entity_id
        self.room = room

        self.x = x
        self.y = y
        self.z = z

class Location(Base):
    __compname__ = "location"
    __tablename__ = "location"

    id = Column(Integer, primary_key=True)
    entity_id = Column(String, ForeignKey("entity.id"))
    room = Column(Integer)

    x = Column(Integer)
    y = Column(Integer)
    z = Column(Integer)

    def __init__(self, entity_id, room=0, x=0, y=0, z=0):
        self.entity_id = entity_id
        self.room = room

        self.x = x
        self.y = y
        self.z = z

    def detach(self):
        return DetatchedLocation(self.entity_id, self.room, self.x, self.y, self.z)


class Space(Base):
    __compname__ = "space"
    __tablename__ = "space"

    id = Column(Integer, primary_key=True)
    entity_id = Column(String, ForeignKey("entity.id"))

    width = Column(Integer)
    length = Column(Integer)
    height = Column(Integer)

    def __init__(self, entity_id, width, length, height):
        self.entity_id = entity_id

        self.width = width
        self.length = length
        self.height = height


class Temperature(Base):
    __compname__ = "temperature"
    __tablename__ = "temperature"

    id = Column(Integer, primary_key=True)
    entity_id = Column(String, ForeignKey("entity.id"))
    temperature = Column(Integer)

    def __init__(self, entity_id, temperature=0):
        self.entity_id = entity_id
        self.temperature = temperature


class Description(Base):
    __compname__ = "description"
    __tablename__ = "description"

    id = Column(Integer, primary_key=True)
    entity_id = Column(String, ForeignKey("entity.id"))
    description = Column(String)

    def __init__(self, entity_id, description="temp_description"):
        # todo will have to be replaced with something more robust
        self.entity_id = entity_id
        self.description = description


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


class Aliases(Base):
    __compname__ = "aliases"
    __tablename__ = "aliases"
    id = Column(Integer, primary_key=True)
    entity_id = Column(String, ForeignKey("entity.id"))
    alias_id = Column(String)

    def __init__(self, entity_id, alias_id=0):
        self.name = "temp_name"
        self.entity_id = entity_id
        self.alias_id = alias_id


class Type(Base):
    __compname__ = "type"
    __tablename__ = "type"
    id = Column(Integer, primary_key=True)
    entity_id = Column(String, ForeignKey("entity.id"))
    type = Column(String)

    def __init__(self, entity_id, type="temp_type"):
        self.entity_id = entity_id
        self.type = type

class Avatar(Base):
    __compname__ = "avatar"
    __tablename__ = "avatar"
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

'Allow the entity to have things placed on top of it'


class Surface(Base):
    __compname__ = 'surface'
    __tablename__ = 'surface'
    id = Column(Integer, primary_key=True)
    parent_id = Column(Integer, ForeignKey('surface.id'))
    entity_id = Column(String, ForeignKey("entity.id"))
    children = relationship("Surface",
                            backref=backref('parent', remote_side=[id])
                            )

    def __init__(self, entity_id, parent_id=0):
        self.entity_id = entity_id
        self.parent_id = parent_id

components = {
    "ascending": Ascending,
    "av_events": AVEvents,
    "av_messages": AVMessages,
    "casting": Casting,
    "changing": Changing,
    "creating": Creating,
    "dropping": Dropping,
    "entering": Entering,
    "exiting": Exiting,
    "held_by": HeldBy,
    "holding": Holding,
    "looking": Looking,
    "moving": Moving,
    "network_messages": NetworkMessages,
    "on_hold_timeout": OnHoldTimeout,
    "speaking": Speaking,
    "taking": Taking,
    "visible_names": VisibleNames,
    "visible_objects": VisibleObjects,
    "writing": Writing,
}

db_components = {
    "aliases": Aliases,
    "avatar": Avatar,
    "description": Description,
    "exit": Exit,
    "location": Location,
    "material": Material,
    "names": Names,
    "on_hold": OnHold,
    "player_controlled": PlayerControlled,
    "runes": Runes
    "senses": Senses,
    "space": Space,
    "surface": Surface, 
    "temperature": Temperature,
    "type": Type,
}
