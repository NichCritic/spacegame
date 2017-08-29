from Systems.system import System
from spells.runes import runes
from itertools import dropwhile


class RuneProcessingSystem(System):
    manditory = ['runes', 'rune_data', 'rune_active']
    optional = []

    @staticmethod
    def index_to_position(rune, position):
        if position == 0:
            return rune.top
        if position == 1:
            return rune.mid
        if position == 2:
            return rune.bottom

    def handle(self, node):
        # Find the current rune function
        rune_number = node.rune_data.rune_number
        rune_position = node.rune_data.rune_position
        rune_list = node.rune_data.runes

        rune = rune_list[rune_number]

        rune_fn = RuneProcessingSystem.index_to_position(rune, rune_position)

        # Call the current rune fn
        direction = rune_fn(node.id, node.rune_data.context)

        # Update the position
        if direction == ('left'):
            node.rune_data.rune_number = rune_number - 1 % len(rune_list)
        if direction == ('right'):
            node.rune_data.rune_number = rune_number + 1 % len(rune_list)
        if direction == ('up'):
            node.rune_data.rune_position = rune_position - 1 % 3
        if direction == ('down'):
            node.rune_data.rune_position = rune_position + 1 % 3
