'''
Created on 2013-12-01

@author: Nich
'''
import uuid


class PlayerFactory(object):
    '''
    classdocs
    '''


    def __init__(self, component_manager):
        self.players = {}
        self.component_manager = component_manager
        
    
    def create_player(self, message_buffer, pid=None, avatar=None):
        p = Player(message_buffer, avatar) if pid == None else Player(message_buffer, pid, avatar)
        
        if avatar:     
            player_controlled = self.component_manager.get_component(avatar.id, "player_controlled")
            player_controlled.pid = p.id
        self.players[p.id] = p
        
        return p
    
    def get_player(self, pid):
        return self.players[pid]
    
    def get_players(self):
        return self.players
        
       


class Player(object):
    
    def __init__(self, message_buffer, id= None, avatar=None):
        #TODO: Ideally get this from google
        self.id = uuid.uuid4() if id == None else id
        self.message_buffer = message_buffer
        self.avatar = avatar
        
        
    def set_avatar(self, avatar_id):
        self.avatar_id = avatar_id
    
    
        
    
