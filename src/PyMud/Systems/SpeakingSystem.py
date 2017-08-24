from Systems.AVEvent import AVEvent
from Systems.system import System


class SpeakingSystem(System):
    '''
    Handles when an entity says something out loud
    '''

    manditory = ["location", "speaking"]
    handles = ["speaking"]

    def create_av_event_data(self, location, speaking):
        if speaking.target:
            target = list(speaking.target.items())[0][1]
        else:
            target = None
        event = AVEvent("speaking", speaking.text, location.detach(),
                        speaking.entity_id, speaking.format, target)
        return event

    def handle(self, node):
        room_node = self.node_factory.create_node(node.location.room, [])
        av_event_data = self.create_av_event_data(node.location, node.speaking)
        room_node.add_or_attach_component("av_events", None)
        room_node.av_events.events.append(av_event_data)
