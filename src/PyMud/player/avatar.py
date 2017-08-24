'''
Created on 2013-11-18

@author: Nich
'''

from objects.baseobject import Entity


class Avatar(Entity):
    '''
    classdocs
    '''
    __mapper_args__ = {
        'polymorphic_identity': 'avatar'
    }

    def __init__(self):
        super(Avatar, self).__init__()


class AvatarFactory(object):

    def __init__(self, node_factory, component_manager, data=None):
        self.node_factory = node_factory
        self.component_manager = component_manager
        self.default_data = data

    def create_default_avatar(self, data=None):
        avatar = Avatar()
        default_data = self.default_data

        loc_data = {}
        if data and "starting_room" in data:
            loc_data["room"] = data["starting_room"]
        else:
            loc_data["room"] = default_data["starting_room"]

        room_container = self.component_manager.get_component(
            loc_data["room"], "container")

        self.component_manager.add_component_to_object(
            "container", avatar.id, {"parent_id": room_container.id})
        self.component_manager.add_component_to_object(
            "location", avatar.id, loc_data)
        self.component_manager.add_component_to_object(
            "names", avatar.id, None)
        self.component_manager.add_component_to_object(
            "visible_names", avatar.id)
        if data and "pid" in data:
            self.component_manager.add_component_to_object(
                "player_controlled", avatar.id, {"pid": data["player_id"]})
        else:
            self.component_manager.add_component_to_object(
                "player_controlled", avatar.id, {"pid": default_data["player_id"]})

        self.component_manager.add_component_to_object(
            "senses", avatar.id, None)
        self.component_manager.add_component_to_object(
            "avatar_type", avatar.id, None)
        self.component_manager.add_component_to_object(
            "health", avatar.id, {'health': 50, 'max_health': 100})
        self.component_manager.add_component_to_object(
            "mana", avatar.id, {'mana': 250, 'max_mana': 250})

        node = self.node_factory.create_node(
            avatar.id, ["location", "names", "player_controlled"])

        if data and "name" in data:
            node.names.name = data["name"]
            node.names.identifiers = data["name"]
        else:
            node.names.name = "alice"
            node.names.identifiers = "alice"

        print(data)
        print(default_data)

        return avatar

    def create_avatar(self, data):
        avatar = Avatar()

        self.component_manager.add_component_to_object("location", avatar)
        self.component_manager.add_component_to_object(
            "object_content", avatar)
        self.component_manager.add_component_to_object("description", avatar)
        self.component_manager.add_component_to_object("names", avatar)
        self.component_manager.add_component_to_object(
            "player_controlled", avatar, {"pid": data["player_id"]})
        self.component_manager.add_component_to_object("senses", avatar)
        self.component_manager.add_component_to_object("visible_names", avatar)

        node = self.node_factory.create_node(
            avatar.id, ["location", "names", "player_controlled"])
        node.location.room = data["starting_room"]
        node.location.location = data["starting_location"]
        node.names.name = "alice"

        return avatar
