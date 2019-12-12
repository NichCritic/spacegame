from Systems.system import System
import math
import time
import random
import objects.item as Items


class ShopUnpackSystem(System):

    mandatory = ["shop_spec"]
    handles = ["shop_spec"]

    def __init__(self, node_factory, session_manager):
        self.node_factory = node_factory
        self.session_manager = session_manager

    def handle(self, node):
        '''
         {"shop_data": {
             "name": "Gold mine",
             "sale_items": [
                 {"id": iron_ore.id, "pos": 0, "cost": 10},
                 {"id": gold_ore.id, "pos": 1, "cost": 1000},
             ],
             "buy_items": [
                 {"id": gasoline.id, "pos": 0, "min_price": 1, "max_price": 500}
             ],
             "process": [
                 {"id": gasoline.id, "amt": 1, "products": [
                     {iron_ore.id: 10}, {gold_ore.id: 1}]}
             ]
         }}

        '''
        shop_data = {}

        shop_data["name"] = node.shop_spec.shop_data["name"]

        with self.session_manager.get_session() as session:
            shop_data["sale_items"] = []
            for item in node.shop_spec.shop_data["sale_items"]:
                shop_data["sale_items"].append({
                    "id": str(item["id"]),
                    "name": Items.get_item_by_id(session, item["id"]).name,
                    "pos": item["pos"],
                    "cost": item["cost"]
                })

        shop_data["buy_items"] = []
        for item in node.shop_spec.shop_data["buy_items"]:
            shop_data["buy_items"].append({
                "name": item["name"],
                "id": str(item["id"]),
                "pos": item["pos"],
                "cost": random.randint(item["min_price"], item["max_price"])
            })

        node.add_or_attach_component("shop", {"shop_data": shop_data})

        if 'process' in node.shop_spec.shop_data:
            node.add_or_attach_component(
                "processor", {"processes": node.shop_spec.shop_data["process"]})
