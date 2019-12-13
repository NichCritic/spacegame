from functools import partial
from gamedata.quests import QuestStage
from Systems.system import System
from objects.components import components
import objects
import logging

class QIntroS2Active():
    def __init__(self, entity_id):
        self.entity_id = entity_id

class QIntroS3Active():
    def __init__(self, entity_id):
        self.entity_id = entity_id
        self.sold_items = 0

quest_components = {
    "q_intro_s2_active": QIntroS2Active,
    "q_intro_s3_active": QIntroS3Active
}

components.update(quest_components)

class Stage1(QuestStage):

    def attach(self, av):
        logging.info("Intro Stage 1 attached")
        self.quest.next(av)

def check_condition(quest, iron_ore_id, av):
    logging.info(f"{av.id} in stage2 quest radius")
    if not av.entity_has("q_intro_s2_active"):
        return

    av.add_or_attach_component("inventory", {})
    inv = av.inventory.inv
    logging.info(f"{av.id} has {inv[iron_ore_id]['qty']} iron ore")
    if iron_ore_id in inv and inv[iron_ore_id]['qty'] >= 10:
        av.delete_component("q_intro_s2_active")
        quest.next(av)

class Stage2(QuestStage):
    def __init__(self, quest, node_factory, session_manager,):
        self.session_manager = session_manager
        super().__init__(quest, node_factory)

    def attach(self, av):
        logging.info(f"Intro Stage 2 attached to {av.id}")
        av.add_or_attach_component("q_intro_s2_active", {})

    

    def initialize_world(self):
        with self.session_manager.get_session() as session:
            iron_ore = objects.item.get_item_by_name(session, 'iron ore').static_copy()

        condition = partial(check_condition, self, iron_ore.id)

        self.node_factory.create_new_node({
            "area": {"radius": 200},
            "position": {"x": 0, "y": 0},
            # "type": {"type": "bolfenn"},
            "velocity": {"x": 0, "y": 0},  # Needed to pick up proximity
            "event": {"script": condition, "cooldown": 3600, "initial_cooldown": 0},
            "event_proximity_trigger": {}
        })

class Stage3System(System):
    mandatory = ["q_intro_s3_active", "sold"]
    optional = []
    handles = []

    def __init__(self, quest, item_id, node_factory):
        self.node_factory = node_factory
        self.quest = quest
        self.item_id = item_id

    def handle(self, node):
        pass

class Stage3(QuestStage):
    def __init__(self, quest, node_factory, session_manager):
        self.session_manager = session_manager
        super().__init__(quest, node_factory)

    def register_systems(self, system_set):
        with self.session_manager.get_session() as session:
            iron_ore = objects.item.get_item_by_name(session, 'iron ore').static_copy()
        system = Stage3System(self.quest, iron_ore.id, self.node_factory)
        system_set.register(system)

    def attach(self, av):
        av.add_or_attach_component("q_intro_s3_active", {})








