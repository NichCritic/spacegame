from Systems.AVEvent import AVEvent
from Systems.NetworkMessageSystem import NetworkMessage


class Rune(object):

    def __init__(self, node_factory):
        self.node_factory = node_factory


class Luv(Rune):

    def top(self, node_id, ctx):
        print("Top")
        if 'target' not in ctx:
            node = self.node_factory.create_node(node_id, [], ['container'])
            if node.has('container') and node.container.type == 'held':
                ctx['target'] = node.container.parent.entity_id
                return ('down')
            else:
                return ('stay')
        else:
            return ('down')

    def mid(self, node_id, ctx):
        print("Mid")
        if 'target' not in ctx:
            return ('up')
        target = self.node_factory.create_node(ctx['target'], [], ['mana'])
        node = self.node_factory.create_node(node_id, ['names'])

        node.add_or_attach_component('mana', {})

        if target.has('mana'):
            amt = max(target.mana.mana, 5)
            target.mana.mana -= amt
            node.mana.mana += amt

            out_msg = NetworkMessage(
                target.id, f"A luv rune on {node.names.name} flickers and you lose {amt} mana")
            target.add_or_attach_component("network_messages", {})
            target.network_messages.msg.append(out_msg)
            return ('left')
        del ctx['target']
        return ('up')

    def bottom(self, node_id, ctx):
        if 'target' not in ctx:
            return ('down')

        target = self.node_factory.create_node(ctx['target'], [], ['health'])
        node = self.node_factory.create_node(ctx['target'], [], ['mana'])

        if not target.has('health') or not node.has('mana'):
            del ctx['target']
            return ('down')

        amt = min(node.mana.mana, 10)
        node.mana.mana -= amt
        target.add_or_attach_component('change_health', {})
        target.change_health.amount += amt
        out_msg = NetworkMessage(
            target.id, f"A luv rune on {held_node.names.name} glows green for a brief moment")
        target.add_or_attach_component("network_messages", {})
        target.network_messages.msg.append(out_msg)
        return ('right')


class Tir(Rune):

    def acquire(self, node):
        pass

    def release(self, node):
        pass


runes = {"luv": Luv}
