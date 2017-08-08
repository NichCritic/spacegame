'''
Created on 2013-11-15

@author: Nich
'''
from model.base import Base
from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship, backref


class Container(Base):
    
    __tablename__ = 'container'
    id = Column(Integer, primary_key=True)
    parent_id = Column(Integer, ForeignKey('container.id'))
    entity_id = Column(String, ForeignKey("entity.id"))
    children = relationship("Container",
                backref=backref('parent', remote_side=[id])
            )
    def __init__(self, entity_id, parent_id=0):
        self.entity_id = entity_id
        self.parent_id = parent_id

    def __repr__(self):
        return "{}".format(self.children)
        
    
class Room(Base):
    __tablename__ = 'room'
    id = Column(Integer, primary_key=True)
    entity_id = Column(String, ForeignKey("entity.id"))


    def __init__(self, entity_id):
        self.entity_id = entity_id

   
    

components = {
}


db_components  = {
    "container":Container,
   "room":Room 
}


    
       
        