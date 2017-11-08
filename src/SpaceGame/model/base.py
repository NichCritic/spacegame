'''
Created on 2014-01-30

@author: Nich
'''
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from contextlib import contextmanager

def engine(dbstring = 'sqlite:///fake.db', echo=False):
    engine = create_engine(dbstring, echo=echo)
    return engine

def create_sessionmaker(engine):
    Session = sessionmaker(bind=engine)
    my_scoped_session = scoped_session(Session)
    
    return my_scoped_session


class SessionManager():
    def __init__(self, Session):
        self.Session = Session
    
    @contextmanager  
    def get_session(self):
        try:
            
            session = self.Session()
            yield session
        except:
            raise
        finally:
            session.commit()
            session.close()
     


Base = declarative_base()