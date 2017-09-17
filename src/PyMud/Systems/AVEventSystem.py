'''
Created on 2014-03-15

@author: Nich
'''

from Systems.system import System
from copy import copy


class Propagator(object):

    def propagate(self, event, fro, to):
        event.mark_visited(fro.id)
        if not event.has_visited(to.id):
            to.add_or_attach_component("av_events", None)
            to.av_events.events.append(copy(event))
        event.handle()


class AVEventExitPropagationSystem(System, Propagator):
    manditory = ["av_events", "exit"]

    def handle(self, fro):
        print(fro)
        to = self.node_factory.create_node(fro.exit.dest_id, [])
        for event in fro.av_events.events:
            self.propagate(event, fro, to)


class AVEventContainerPropagationSystem(System, Propagator):
    manditory = ["av_events", "container"]

    def handle(self, fro):

        for obj in fro.container.children:
            to = self.node_factory.create_node(obj.entity_id, [])
            for event in fro.av_events.events:
                self.propagate(event, fro, to)
                event.handle()
