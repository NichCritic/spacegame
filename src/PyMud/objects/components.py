'''
Created on 2013-11-03

@author: Nich
'''

from model.base import Base
from sqlalchemy import Column, String, Integer, ForeignKey, PickleType
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


class Speaking(object):

    def __init__(self, entity_id, text, target, format):
        self.entity_id = entity_id
        self.text = text
        self.target = target
        self.format = format


class Creating(object):

    def __init__(self, entity_id):
        self.entity_id = entity_id


class Moving(object):

    def __init__(self, entity_id, x, y, z):
        self.entity_id = entity_id
        self.x = x
        self.y = y
        self.z = z


class Exiting(object):

    def __init__(self, entity_id, exit_id):
        self.entity_id = entity_id
        self.exit_id = exit_id


class Holding(object):

    def __init__(self, entity_id, held_entity_id):
        self.entity_id = entity_id
        self.held_entity_id = held_entity_id


class HeldBy(object):

    def __init__(self, entity_id, holding_entity_id):
        self.entity_id = entity_id
        self.holding_entity_id = holding_entity_id


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
    exit = Column(String)

    dest_room = Column(String)
    dest_x = Column(Integer)
    dest_y = Column(Integer)
    dest_z = Column(Integer)

    def __init__(self, entity_id, room=0, x=0, y=0, z=0):
        self.entity_id = entity_id
        self.dest_room = room

        self.dest_x = x
        self.dest_y = y
        self.dest_z = z


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
    "network_messages": NetworkMessages,
    "speaking": Speaking,
    "looking": Looking,
    "av_events": AVEvents,
    "av_messages": AVMessages,
    "moving": Moving,
    "exiting": Exiting,
    "visible_objects": VisibleObjects,
    "visible_names": VisibleNames,
    "creating": Creating,
    "holding": Holding,
    "held_by": HeldBy,
    "taking": Taking,
    "dropping": Dropping,
    "on_hold_timeout": OnHoldTimeout
}

db_components = {
    "temperature": Temperature,
    "location": Location,
    "description": Description,
    "type": Type,
    "names": Names,
    "player_controlled": PlayerControlled,
    "senses": Senses,
    "aliases": Aliases,
    "space": Space,
    "material": Material,
    "exit": Exit,
    "on_hold": OnHold,
    "surface": Surface
}
