
from Systems.AVEvent import AVEvent
from Systems.system import System
from Systems.av_event_mixin import AVEventMixin
'''
Created on 2014-03-31

@author: Nich
'''


class CreatingSystem(System, AVEventMixin):

    manditory = ['creating', 'location', 'names']
    handles = ['creating']

    '''
    Create a new entity in the node's current room
    '''

    def handle(self, node):
        room = node.location.room
        room_node = self.node_factory.create_node(room, ["container"])
        obj = self.node_factory.create_new_node({
            "container": {"parent_id": room_node.container.id},
            "location": {"room": room},
            "names": {'name': node.creating.name, 'identifiers': node.creating.name},

        })

        self.av_event(node, {'player': node.names.name,
                             'target': node.creating.name}, node.creating.format)
