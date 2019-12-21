from functools import partial
from gamedata.quests import QuestStage, Quest
from objects.components import components
import logging

class QBreakoutS1Active():
    def __init__(self, entity_id):
        self.entity_id = entity_id



quest_components = {
    "q_breakout_s1_active": QBreakoutS1Active,
}

components.update(quest_components)

class Breakout(Quest):

	def available(self, av):
		logging.info("Checking if breakout is available")
		av.add_or_attach_component("quests", {})
		quests = av.quests.quests
		if "intro" in quests and quests['intro']['status'] == "complete":
			logging.info("It is!")
			return True
		logging.info("It is not!")
		return False

def check_condition(quest, trigger_area, av):
    if not av.entity_has("q_breakout_s1_active"):
        return

    av.remove_component("q_breakout_s1_active")
    quest.next(av)

class Stage1(QuestStage):
    def __init__(self, quest, node_factory):
        super().__init__(quest, node_factory)

    def attach(self, av):
        av.add_or_attach_component("q_breakout_s1_active", {})

    

    def initialize_world(self):
        

        condition = partial(check_condition, self.quest)

        self.node_factory.create_new_node({
            "area": {"radius": 400},
            "position": {"x": 20000, "y": 0},
            # "type": {"type": "bolfenn"},
            "velocity": {"x": 0, "y": 0},  # Needed to pick up proximity
            "event": {"script": condition, "cooldown": 3600, "initial_cooldown": 0},
            "event_proximity_trigger": {}
        })