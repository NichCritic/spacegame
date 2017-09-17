from Systems.AVEvent import AVEvent2


class AVEventMixin(object):

    def get_room(self, node):
        if node.has('location'):
            return self.node_factory.create_node(node.location.room, [])
        return None

    def create_av_event_data(self, data, format):
        print(data)
        # import pdb
        # pdb.set_trace()
        return AVEvent2(format, data=data)

    def av_event(self, node, data, format):
        room = self.get_room(node)
        if room:
            av_event_data = self.create_av_event_data(data, format)
            room.add_or_attach_component("av_events", None)
            room.av_events.events.append(av_event_data)
