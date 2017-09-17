from Systems.system import System
from Systems.av_event_mixin import AVEventMixin


class SpeakingSystem(System, AVEventMixin):
    '''
    Handles when an entity says something out loud
    '''

    manditory = ["location", "speaking", "names"]
    handles = ["speaking"]

    def handle(self, node):

        data = {'player': node.names.name,
                'text': node.speaking.text}
        if node.speaking.target:
            data['target'] = str(node.speaking.target)

        self.av_event(node, data, node.speaking.format)
