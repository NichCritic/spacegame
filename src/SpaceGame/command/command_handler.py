'''
Created on 2011-08-13

@author: Nich
'''

import logging
import json


class CommandHandler():

    def __init__(self, node_factory, session_manager, db_comps):
        self.node_factory = node_factory
        self.session_manager = session_manager
        self.db_comps = db_comps

    def handle_command(self, source, command_json):
        av = self.node_factory.create_node(source.avatar_id, [])
        av.add_or_attach_component(
            'player_input', {})

        command = json.loads(command_json)

        av.player_input.data.extend(command['inputs'])

        av.add_or_attach_component(
            'health', {"health": 1000, "max_health": 1000})

        av.add_or_attach_component(
            'position', {})
        av.add_or_attach_component('area', {'radius': 8})
        av.add_or_attach_component('collidable', {})

        av.add_or_attach_component(
            'velocity', {})
        av.add_or_attach_component(
            'acceleration', {})
        av.add_or_attach_component(
            'force', {})
        av.add_or_attach_component(
            'rotation', {})

        av.add_or_attach_component('mass', {})
        av.add_or_attach_component('type', {'type': 'ship'})
        av.add_or_attach_component('physics_update', {})

        av.add_or_attach_component('game_state_request', {})
        av.add_or_attach_component('state_history', {})
        av.add_or_attach_component('animated', {'update_rate': 200})
        av.add_or_attach_component('collision_velocity_damage', {"damage": 200, "min_velocity":0.2, "max_velocity":1})
        av.add_or_attach_component('collision_movement', {})

        av.add_or_attach_component('weapon', {'type':'single_shot'})

        with self.session_manager.get_session() as session:
            self.db_comps.set_session(session)
            av.add_or_attach_component('inventory', {'inventory': {}})
            av.add_or_attach_component('money', {'money': 10000})

        return ("success",)
