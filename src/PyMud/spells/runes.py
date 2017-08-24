

class Rune(object):

    def __init__(self, node, next=None):
        self.mana = 0
        self.max_mana = 100
        self.next = next
        self.active = False
        self.node = node

    def on_charged(self):
        print("Oncharged calleds")
        if self.next:
            self.next.mana = self.mana
            self.mana = 0
            self.next.release()

    def add_next(self, n):
        if self.next:
            self.next.add_next(n)
        else:
            self.next = n

    def activate(self):
        if not self.active:
            self.active = True
            if self.mana > 0:
                self.release()
            else:
                self.acquire()


class Luv(Rune):

    def acquire(self):
        self.node.add_or_attach_component(
            'on_hold', {'callback': 'luv_aq', 'data': {}, 'timeout': 5})

    def release(self):
        print('Luv release {}'.format(self.node))
        self.node.add_or_attach_component(
            'on_hold', {'callback': 'luv_rel', 'data': {}, 'timeout': 5})


class Tir(Rune):

    def acquire(self, node):
        pass

    def release(self, node):
        pass


runes = {"luv": Luv}
