'''
Created on 2013-11-01

@author: Nich
'''
import uuid
import logging

from PyMud.model.base import Base
from sqlalchemy import Column, String, Integer


class Entity(Base):
    __tablename__ = "entity"
    
    id = Column(String, primary_key=True)
    type = Column(String)
    
    __mapper_args__ = {
        'polymorphic_on':type,
        'polymorphic_identity':'entity'
    }
    
    
    def __init__(self):
        self.id = str(uuid.uuid4())
     
    
    
    def __repr__(self):
        return "<"+str(self.id)+">"
    

 
    
        
                
    
    
    