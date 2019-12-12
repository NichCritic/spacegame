class Quest():
	def __init__(self, node_factory, name):
		self.node_factory = node_factory
		self.stages = []
		self.name = name

	def add_stage(self, stage):
		self.stages.append(stage)

	def next(self, av):
		av.add_or_attach_component("active_quests")
		quest_data = av.active_quests.quests[self.name]
		quest_data.stage += 1
		av.add_or_update_component("quest_status_updated", {
			"quest":self.name, 
			"stage":quest_data.stage
		})
		if quest_data.stage < len(self.stages):
			self.stages[quest_data.stage-1].attach(av)

	def available(self, av):
		pass

	def finalize(self, system_set):
		for stage in self.stages:
			stage.initialize_world()
			stage.register_systems(system_set)


class QuestStage():

	def __init__(self, quest, node_factory):
		self.node_factory = node_factory
		self.quest = quest

	def attach(self, av):
		pass

	def initialize_world(self):
		pass

	def register_systems(self, system_set):
		pass