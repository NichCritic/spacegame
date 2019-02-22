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

            if buyer.money.money < cost:
                # skip the transaction
                continue

            seller_inv = seller.inventory.inv
            if i_id not in seller_inv:
                continue

            if "qty" not in seller_inv[i_id]:
                # If the item in the inventory has no qty
                continue
            if not seller_inv[i_id]["qty"] >= qty:
                # If the qty is too low to sell
                continue

            buyer.money.money -= cost
            seller.money.money += cost

            buyer_inv = buyer.inventory.inv

            seller_inv[i_id]["qty"] -= qty

            if i_id in buyer_inv:
                if "qty" in buyer_inv[i_id]:
                    buyer_inv[i_id]["qty"] += qty
                else:
                    buyer_inv[i_id]["qty"] = qty
            else:
                buyer_inv[i_id] = {"qty": qty}

        node.transaction.transactions = []
