from Systems.system import System
from Systems.av_event_mixin import AVEventMixin
from Systems.NetworkMessageSystem import NetworkMessage


class WritingSystem(System, AVEventMixin):
    '''
    Generates annoying ticks that everyone with a network connection gets (Debug)
    '''
    manditory = ['writing', 'location', 'names']
    handles = ['writing']

    def handle(self, node):
        for t_name, t_id in node.writing.target.items():
            target_object = self.node_factory.create_node(
                t_id, ['names'], ['runes'])

            if not target_object.has('runes'):
                target_object.add_or_attach_component(
                    "runes", {"active": False, "runes_list": []})
            target_object.runes.runes_list = target_object.runes.runes_list + \
                [node.writing.rune]

            print("Writing system got message from " + node.id)
            self.av_event(node, {'player': node.names.name,
                                 'target': target_object.names.name}, node.writing.format)
