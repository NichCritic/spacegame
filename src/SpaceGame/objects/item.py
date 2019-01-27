# TODO


from model.base import Base
from sqlalchemy import Column, String, Integer, ForeignKey, PickleType, Boolean
from sqlalchemy.orm import relationship, backref


class StaticItem():

    def __init__(self, id, name):
        self.id = id
        self.name = name


class Item(Base):
    __tablename__ = "item"
    id = Column(Integer, primary_key=True)
    name = Column(String)

    def __init__(self, name):
        self.name = name

    def static_copy(self):
        return StaticItem(self.id, self.name)


def get_item_by_id(session, id):
    return session.query(Item).filter(Item.id == id).one()


def get_item_by_name(session, name):
    return session.query(Item).filter(Item.name == name).one()
