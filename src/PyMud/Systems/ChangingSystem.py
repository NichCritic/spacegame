import json


class ChangingSystem(object):
    '''
    Generates annoying ticks that everyone with a network connection gets (Debug)
    '''

    def __init__(self, node_factory):
        self.node_factory = node_factory

    def get_nodes(self):
        return self.node_factory.create_node_list(["changing"])

    def process(self):
        self.nodes = self.get_nodes()
        for node in self.nodes:
            try:
                comp = json.loads(node.changing.text)
                for comp_name, comp_data in comp.items():

                    for t_name, t_id in node.changing.target.items():
                        target = self.node_factory.create_node(t_id, [])
                        target.add_or_update_component(comp_name, comp_data)

            finally:
                node.remove_component('changing')
