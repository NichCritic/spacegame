'''
Created on 2013-11-22

@author: Nich
'''
import unittest
from Systems.network_av_system import NetworkAVSystem  # , NetworkAVNode
from messages.message_types import AVMessage
from multiprocessing import Queue
from objects.components import Location,  Senses, AVMessages


class NetworkAVNode(object):

    def __init__(self, entity_id, location, senses, av_messages):
        self.id = entity_id
        self.location = location
        self.senses = senses
        self.av_messages = av_messages


class NodeFactory():

    def __init__(self, nodes):
        self.nodes = nodes

    def create_node_list(self, data, optional=None):
        return NodeList(self.nodes)


class NodeList(list):

    def __init__(self, nodes):
        self.nodes = nodes

    def subset(self, data):
        return self.nodes


class NetworkAVTest(unittest.TestCase):

    def setUp(self):
        message_template = [([("loudness", 50), ("targeted",), ("is_caller",)], ['You say to {target}, "{text}".']),
                            ([("loudness", 50), ("targeted",), ("is_target",)], [
                             '{player} says to you, "{text}".']),
                            ([("loudness", 50), ("targeted",), ],
                             ['{player} says to {target}, "{text}".']),
                            ([("loudness", 50), ("is_caller",)],
                             ['You say, "{text}".']),
                            ([("loudness", 50)],
                             ['{player} says, "{text}".']),
                            ([("visibility", 60), ("is_caller")],
                             ["You can't hear your own voice!"]),

                            ([("visibility", 60), ("is_caller")],             [
                             "{player}'s lips move, but you can't make out what they're saying."])
                            ]

        self.AVMessageQueue = Queue()
        self.out_queue = Queue()

        # default player, default room
        self.player1 = NetworkAVNode("1", Location(
            "1", "0"), Senses("1"), AVMessages("1"))
        # different room, same location
        self.player2 = NetworkAVNode("2", Location(
            "2", "1"), Senses("2"), AVMessages("1"))
        # same room, too far away
        self.player3 = NetworkAVNode("3", Location(
            "3", "0"), Senses("3"), AVMessages("1"))
        # same room, too far away
        self.player4 = NetworkAVNode("4", Location(
            "4", "0"), Senses("4"), AVMessages("1"))

        self.player_fact = NodeFactory(
            [self.player1, self.player2, self.player3, self.player4])
        self.netAVSystem = NetworkAVSystem(self.player_fact)

        self.message1 = AVMessage("test_message", "test1", Location(
            "5", "0"), "1", message_template, target_id=self.player4.id)
        self.message2 = AVMessage("test_message", "test2", Location(
            "6", "0"), "4", message_template, target_id=self.player3.id)
        self.message3 = AVMessage("test_message", "test3", Location(
            "7", "0"), "1", message_template)

        self.player1.av_messages.msg.append(self.message1)
        self.player1.av_messages.msg.append(self.message2)
        self.player1.av_messages.msg.append(self.message3)
        self.player2.av_messages.msg.append(self.message1)
        self.player2.av_messages.msg.append(self.message2)
        self.player2.av_messages.msg.append(self.message3)
        self.player3.av_messages.msg.append(self.message1)
        self.player3.av_messages.msg.append(self.message2)
        self.player3.av_messages.msg.append(self.message3)
        self.player4.av_messages.msg.append(self.message1)
        self.player4.av_messages.msg.append(self.message2)
        self.player4.av_messages.msg.append(self.message3)

    def tearDown(self):
        pass

    def testNetworkAVSystem(self):
        self.netAVSystem.process()

        sorted(['You say to 4, "test1".',
                '1 says to you, "test1".',
                'You say, "test3".',
                '1 says, "test3".',
                '4 says to 3, "test2".',
                'You say to 3, "test2".'])


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testAVSystem']
    unittest.main()
