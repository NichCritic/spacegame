'''
Created on 2011-08-13

@author: Nich
'''

import logging
import json


class CommandHandler():

    def __init__(self, node_factory):
        self.node_factory = node_factory

    def handle_command(self, source, command_json):
        av = self.node_factory.create_node(source.avatar_id, [])
        av.add_or_attach_component(
            'player_input', {})

        command = json.loads(command_json)

        av.player_input.data.extend(command['inputs'])

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
        av.add_or_attach_component('type', {'type': 'ship'})
        av.add_or_attach_component('physics_update', {})

        av.add_or_attach_component('game_state_request', {})
        av.add_or_attach_component('state_history', {})
        av.add_or_attach_component('money', {'money': 10000})
        av.add_or_attach_component('inventory', {'inventory': {}})
        return ("success",)
