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
        p = Player(message_buffer, pid, avatar)
        
        if avatar:     
            self.component_manager.add_component_to_object('player_controlled', avatar.id, {'pid':p.id})
        self.players[p.id] = p
        
        return p
    
    def get_player(self, pid):
        return self.players[pid]
    
    def get_players(self):
        return self.players

    def set_player_avatar(self, p, av_id):


        #if we already have an avatar, remove it
        if p.avatar_id:
            if p.avatar_id == av_id:
                #already set
                return
            #This can fail if the entry is manually removed from the db but should otherwise always be true
            if self.component_manager.entity_has_component(p.avatar_id, "player_controlled"):
                self.component_manager.remove_component("player_controlled", p.avatar_id)

        p.avatar_id = av_id
        self.component_manager.add_component_to_object('player_controlled', av_id, {'pid':p.id})

        
       


class Player(object):
    
    def __init__(self, message_buffer, id= None, avatar=None):
        #TODO: Ideally get this from google
        self.id = uuid.uuid4() if id == None else id
        self.message_buffer = message_buffer
        self.avatar_id = avatar
        
        
        
    
    
    
        
    
