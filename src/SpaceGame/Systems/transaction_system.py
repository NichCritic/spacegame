from Systems.system import System
import time
from itertools import takewhile
import json
import logging


class TransactionSystem(System):

    manditory = ["transaction"]
    handles = ["transaction"]

    def __init__(self, node_factory):
        self.node_factory = node_factory

    def handle(self, node):
        for t in node.transaction.transactions:
            b_id = t['buyer_id']
            s_id = t['seller_id']
            i_id = str(t['item_id'])
            qty = t['quantity']
            cost = t['price']

            buyer = self.node_factory.create_node(b_id, ["inventory", "money"])
            seller = self.node_factory.create_node(
                s_id, ["inventory", "money"])

            # TODO: Verify that the buyer actually has the money
            buyer.money.money -= cost
            seller.money.money += cost

            buyer_inv = json.loads(buyer.inventory.inv)

            seller_inv = json.loads(seller.inventory.inv)

            if i_id in buyer_inv:
                if "qty" in buyer_inv[i_id]:
                    buyer_inv[i_id]["qty"] += qty
                else:
                    buyer_inv[i_id]["qty"] = qty
            else:
                buyer_inv[i_id] = {"qty": qty}

            # TODO Verify seller actually has the item
            if i_id in seller_inv:
                if "qty" in seller_inv[i_id]:
                    seller_inv[i_id]["qty"] -= qty
                else:
                    seller_inv[i_id]["qty"] = 0

            buyer.inventory.inv = json.dumps(buyer_inv)
            seller.inventory.inv = json.dumps(seller_inv)

        node.transaction.transactions = []
