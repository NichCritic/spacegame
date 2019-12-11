from functools import partial

class Stage1():

	def __init__(self, session_manager, node_factory):
		self.session_manager = session_manager
		self.node_factory = node_factory
		self.next_stage = None

	def register_next(self, stage):
		self.next_stage = stage

	def attach(self, av):
		av.add_or_update_component("quest_status_updated", {"quest":"intro", "stage":1})

	def next(self, av):
		av.add_or_attach_component("active_quests")
		av.active_quests.quests['intro'].stage = 2
		av.add_or_update_component("quest_status_updated", {"quest":"intro", "stage":2})
		if self.next_stage:
			self.next_stage.attach(av)



class Stage2():
	def __init__(self, session_manager, node_factory):
		self.session_manager = session_manager
		self.node_factory = node_factory
		self.next_stage

	def attach(self, av):
		pass

	def next(self, av):
		av.add_or_attach_component("active_quests")
		av.active_quests.quests['intro'].stage = 3
		av.add_or_update_component("quest_status_updated", {"quest":"intro", "stage":3})

	def check_condition(quest, iron_ore_id, av):
		av.add_or_attach_component("active_quests", {})
		if "intro" not in av.active_quests.quests:
			return
		if av.active_quests.quests['intro'].stage != 2:
			return

		av.add_or_attach_component("inventory", {})
		inv = av.inventory.inv
		if iron_ore_id in inv and inv[iron_ore_id]['qty'] >= 10:
			quest.next(av)

	def initialize_world(self):
		with self.session_manager.get_session() as session:
			iron_ore = objects.item.get_item_by_name(session, 'iron ore').static_copy()

		condition = partial(check_condition, self, iron_ore.id)

		self.node_factory.create_new_node({
            "area": {"radius": 200},
            "position": {"x": 0, "y": 0},
            # "type": {"type": "bolfenn"},
            "velocity": {"x": 0, "y": 0},  # Needed to pick up proximity
            "event": {"script": condition, "cooldown": 3600, "initial_cooldown": initial_cooldown},
            "event_proximity_trigger": {}
        })

class Stage3System():




