'''
Created on Nov 27, 2011

@author: Nich
'''
import uuid

from model.base import Base
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship



class Account(Base):
    __tablename__ = "account"
    
    id = Column(String, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String, unique = True)
    avatars = relationship("AccountAvatar")
    
    
    def __init__(self, first_name, last_name, email):
        self.id = str(uuid.uuid4())
        self.first_name = first_name
        self.last_name = last_name
        self.email = email

class AccountAvatar(Base):
    __tablename__ = "account_avatar"
    
    account_id = Column(String, ForeignKey("account.id"), primary_key = True)
    avatar_id = Column(String, ForeignKey("entity.id"), primary_key = True)
    avatar = relationship("Avatar")
    
class AccountUtils():
    def __init__(self, avatar_factory):
        
        self.avatar_factory = avatar_factory
    
    
    
    def print_all(self, session):
        
        for instance in session.query(Account).order_by(Account.account_id): 
            print(instance.name)
    
    
            
    def get(self, email, session):
        
        try:
            acct = session.query(Account).filter(Account.email==email).one()
            
            return acct
        except:
            return None
        
    def get_by_id(self, id, session):
        
        acct = session.query(Account).filter(Account.id==id).one()
        
        return acct
    
    def make_account(self, first_name, last_name, email, session):
        a = Account(first_name, last_name, email)
        session.add(a)
        return a
    
    def create_new_avatar_for_account(self, account_id, data, session):
        
        
        a = self.avatar_factory.create_default_avatar(data)
        account = session.query(Account).filter(Account.id==account_id).one()
        
        ac_av = AccountAvatar()
        ac_av.account_id = account.id
        ac_av.avatar = a
        account.avatars.append(ac_av)
        
        session.add(ac_av)
        
       
    def get_previous_avatar_for_player(self, player_id, session):
        from objects.components import PlayerControlled
        avatar = session.query(PlayerControlled.__table__).filter(PlayerControlled.pid==player_id).first()
        return avatar.entity_id
        
    def get_avatars_for_account(self, account, session):
        
        session.add(account)
        
        avatars = account.avatars
        
        
        return avatars
        
    def set_avatars_pid(self, avatar_id, player_id, session):
        from objects.components import PlayerControlled
        from sqlalchemy import update
        
        ex = update(PlayerControlled.__table__).where(PlayerControlled.entity_id==avatar_id).values(pid=player_id)
        session.execute(ex)
        
    
    
    def handle_login(self, user, player_factory, session):
        db_user = self.get(user["email"], session)
        if db_user is None:
            db_user = self.make_account("", "", user["email"], session)
        return db_user
    
#Base.metadata.create_all(engine)