'''
Created on 2013-11-27

@author: Nich
'''

from collections import defaultdict
from Systems.NetworkMessageSystem import NetworkMessage
from description.description import ObjectDescriber
import description.description_planner as dp
from pynlg.lexicon import XMLLexicon
import os


def walk_tree_bf(starting_node):
    queue = []
    visited = set()

    queue.append(starting_node)
    visited.add(starting_node)

    for n in queue:
        yield n
        for node in n.get_neighbours():
            if node not in visited:
                queue.append(node)
                visited.add(node)


class DescriptionSystem(object):
    '''
    Builds the description of a room from the description of the locations

    '''

    def __init__(self, node_factory):
        self.node_factory = node_factory
        lex = XMLLexicon(os.path.join(os.path.dirname(
            __file__), '../lexicon/default-lexicon.xml'))
        self.object_describer = ObjectDescriber(lex)

    def get_object_data(self, object_id):
        object_node = self.node_factory.create_node(
            object_id, ["names"], ["material", "avatar",
                                   "actions", "inner_location",
                                   "container", "surface",
                                   "open_container", "holding"])

        return object_node

    def describe_object(self, obj):
        return self.object_describer.describe_object(obj).realize()

    def describe_room_2(self, room_id, node):
        described = []
        description = ""
        room_node = self.node_factory.create_node(
            room_id, ["names", "container"])

        objects = self.node_factory.create_node_list(["names"], ["material", "avatar_type",
                                                                 "actions", "close_to",
                                                                 "container", "surface",
                                                                 "open_container", "holding"], entity_ids=[e.entity_id for e in room_node.container.children])

        ss = dp.subdivide(objects, ["material", "actions", "close_to"])

        print(ss)

        return ""

    def describe_room(self, room_id, node):
        described = []
        description = ""
        room_node = self.node_factory.create_node(
            room_id, ["names", "container"])

        objects = self.node_factory.create_node_list(["names"], ["material", "avatar_type",
                                                                 "actions", "close_to",
                                                                 "container", "surface",
                                                                 "open_container", "holding"], entity_ids=[e.entity_id for e in room_node.container.children])

        print(objects)

        # Handle avatars
        av_descs = []
        avatars = objects.subset(["avatar_type"])
        for av in avatars:
            av_desc = self.describe_object(av) + ' is'
            if av.id == node.id:
                av_desc = "You are"
            described.append(av.id)
            if av.has("close_to"):
                prox = self.get_object_data(av.close_to.n_id)
                prox_desc = self.describe_object(prox)
                av_desc = "{} standing by {}".format(av_desc, prox_desc)
                described.append(prox.id)
            else:
                av_desc = "{} here".format(av_desc)
            if av.container:
                for o in av.container.children:
                    o_n = self.get_object_data(o.entity_id)
                    o_d = self.describe_object(o_n)
                    if o_n.container.type == 'held':
                        av_desc += " holding {}".format(o_d)

            av_descs.append(av_desc)

        description += room_node.names.name + "\n"

        objects = [o for o in objects if not o.id in described]

        lc_descs = []
        o_descs = []

        for o in objects:
            o_desc = self.describe_object(o)
            described.append(o.id)
            if o.has("close_to"):
                prox = self.get_object_data(o.close_to.n_id)
                prox_desc = self.describe_object(prox)
                av_desc = "There is {} by {}".format(o_desc, prox_desc)
                described.append(prox.id)
                lc_descs.append(o_desc)
            else:
                o_descs.append(o_desc)

        if o_descs:
            o_desc = ". There is a {}.".format(", ".join(o_descs))
        else:
            o_desc = "."

        description += '. '.join(av_descs + lc_descs) + o_desc

        return description


class NetworkDescriptionSystem():

    def __init__(self, node_factory, desc_system):
        self.node_factory = node_factory
        self.desc_system = desc_system

    def get_nodes(self):
        return self.node_factory.create_node_list(["looking", "location"])

    def process(self):
        nodes = self.get_nodes()
        for node in nodes:
            msg = ""
            if node.looking.target is None:
                msg = self.desc_system.describe_room(
                    node.location.room, node)
            else:
                msg = self.desc_system.describe_object(node.looking.target)
            out_msg = NetworkMessage(node.id, msg)
            node.add_or_attach_component("network_messages", {})
            node.network_messages.msg.append(out_msg)
            node.remove_component("looking")


if __name__ == "__main__":
    from startup_scripts import setup_db, ObjectProvider, components
    Session = setup_db()
    op = ObjectProvider(Session)

    rds = DescriptionSystem(op.node_factory)


'''
class NetworkRoomDescriptionSystem(object):
    
    Builds the description of a room from the description of the locations
    
    
    def __init__(self, MessageQueue, node_factory, messanger_queue):
        self.message_queue = MessageQueue
        self.av_nodes = []
        self.node_factory = node_factory
        self.messanger_queue = messanger_queue
   
   
    def aggregate_by_contents(self, start_loc):
        contents = defaultdict(set)
        for loc in walk_tree_bf(start_loc):
            if not loc.contents:
                contents["nothing"].add(loc)
            else:
                print(loc.contents)
                for _, c in loc.contents.items():
                    contents[c.type].add(loc)
        return contents

    def display_room(self, start_loc):
        #aggregate by contents
        contents = self.aggregate_by_contents(start_loc)
        results = ""
        for k, v in contents.items():
            results += k +", "+(str(v))+"\n"
        return results
   
    def process_messages(self):
        
        while self.av_message_queue.qsize() >= 1:
            message = self.message_queue.get()
            
            
            out_msg = NetworkMessage(message.id, message.message.format(player = message.source_id, target = message.target_id, text = message.text))
            self.messanger_queue.put(out_msg)
                        
'''
