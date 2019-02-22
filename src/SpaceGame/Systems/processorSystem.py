from Systems.system import System
import math
import time
from itertools import takewhile
import logging


class ProcessorSystem(System):

    manditory = ["processor"]
    handles = []

    def __init__(self, node_factory):
        self.node_factory = node_factory
        self.sim_time = 0

    def handle(self, node):
        if time.time() * 1000 - node.processor.last_update < 6000:
            node.processor.update = time.time() * 1000
            return

        for process in node.processor.processes:
            #{"id": iron_ore.id, "amt": 5, "products": [{iron.id: 1}]}
            node.add_or_attach_component('inventory', {"inventory": {}})

            if not process["id"] == None:
                s_id = str(process["id"])
                if s_id not in node.inventory.inv:
                    continue

                if "qty" not in node.inventory.inv[s_id]:
                    continue

                if node.inventory.inv[s_id]["qty"] < process["amt"]:
                    continue
                node.inventory.inv[s_id]["qty"] -= process["amt"]

            for i, amt in process["products"].items():
                s_i = str(i)
                if s_i not in node.inventory.inv:
                    node.inventory.inv[s_i] = {"qty": amt}
                elif "qty" not in node.inventory.inv[s_i]:
                    node.inventory.inv[s_i]["qty"] = amt
                else:
                    node.inventory.inv[s_i]["qty"] += amt

        node.processor.last_update = time.time() * 1000
