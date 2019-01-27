from Systems.system import System
import math
import time
from itertools import takewhile


class TransactionSystem(System):

    manditory = ["transaction"]
    handles = ["transaction"]

    def __init__(self, node_factory):
        self.node_factory = node_factory

    def handle(self, node):
        for t in node.transaction.transactions:
            b_id = t['buyer_id']
            s_id = t['seller_id']
            i_id = t['item_id']
            qty = t['quantity']
            cost = t['price']

            buyer = self.node_factory.create_node(b_id, ["inventory", "money"])
            seller = self.node_factory.create_node(
                s_id, ["inventory", "money"])

            # TODO: Verify that the buyer actually has the money
            buyer.money.money -= cost
            seller.money.money += cost

            if i_id in buyer.inventory.inventory:
                if "qty" in buyer.inventory.inventory[i_id]:
                    buyer.inventory.inventory[i_id]["qty"] += qty
                else:
                    buyer.inventory.inventory[i_id]["qty"] = qty
            else:
                buyer.inventory.inventory[i_id] = {"qty": qty}

            # TODO Verify seller actually has the item
            if i_id in seller.inventory.inventory:
                if "qty" in buyer.inventory.inventory[i_id]:
                    seller.inventory.inventory[i_id]["qty"] -= qty
                else:
                    seller.inventory.inventory[i_id]["qty"] = 0

        node.transaction.transactions = []
