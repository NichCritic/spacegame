from Systems.system import System


class PickupSystem(System):

    manditory = ["colliding", "pickup"]
    optional = []

    def __init__(self, node_factory):
        self.node_factory = node_factory

    def handle(self, node):
        # TODO: Probably need to choose the person who gets the item randomly
        for collision in node.colliding.collisions:
            c_node = self.node_factory.create_node(
                collision["collider"], [], ["inventory"])

            # No point if they can't pick it up anyways
            if not c_node.has("inventory"):
                continue

            inv = c_node.inventory.inv
            i_id = node.pickup.item_id
            qty = node.pickup.qty

            if i_id in inv:
                if "qty" in inv[i_id]:
                    inv[i_id]["qty"] += qty
                else:
                    inv[i_id]["qty"] = qty
            else:
                inv[i_id] = {"qty": qty}

            # Remove the item once it's been collected
            node.remove_all_components()
            return
