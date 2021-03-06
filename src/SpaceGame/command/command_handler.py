'''
Created on 2011-08-13

@author: Nich
'''

import logging
import json
from gamedata.ships import default_ship


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

        default_ship(av)

        return ("success",)
