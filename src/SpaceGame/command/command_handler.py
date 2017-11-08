'''
Created on 2011-08-13

@author: Nich
'''

import logging
import json


class CommandHandler():

    def __init__(self, node_factory):
        self.node_factory = node_factory

    def handle_command(self, source, command):
        av = self.node_factory.create_node(source.avatar_id, [])
        av.add_or_update_component(
            'player_input', {"data": json.loads(command)})

        av.add_or_attach_component(
            'position', {})
        av.add_or_attach_component(
            'velocity', {})
        av.add_or_attach_component(
            'acceleration', {})
        av.add_or_attach_component(
            'force', {})
        av.add_or_attach_component(
            'rotation', {})

        av.add_or_attach_component('mass', {})
        av.add_or_attach_component('physics_update', {})

        av.add_or_attach_component('game_state_request', {})
        return ("success",)
