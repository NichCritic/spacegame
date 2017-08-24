from Systems.system import System


class AVEventCleaner(System):
    manditory = ['av_events']

    def process(self):
        for node in self.get_nodes():
            events = node.av_events.events
            node.av_events.events[:] = [e for e in events if not e.handled]
            if not node.av_events.events:
                node.remove_component('av_events')
