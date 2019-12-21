import logging
class QuestData():
	def __init__(self):
		self.stage = 0

class Quest():
	def __init__(self, node_factory, name):
		self.node_factory = node_factory
		self.stages = []
		self.name = name

	def add_stage(self, stage):
		self.stages.append(stage)

	def next(self, av, stage=None):
		av.add_or_attach_component("active_quests", {})
		quest_data = av.active_quests.quests[self.name]
		if stage:
			quest_data.stage = stage
		else:
			quest_data.stage += 1

		av.add_or_attach_component("quests", {})
		quest = av.quests.quests[self.name]
		quest['stage'] = quest_data.stage

		av.add_or_update_component("quest_status_updated", {
			"quest":self.name, 
			"stage":quest_data.stage
		})
		if quest_data.stage <= len(self.stages):
			self.stages[quest_data.stage-1].attach(av)
		else:
			quest['status'] = "complete"


	def start(self, av, stage = None):
		av.add_or_attach_component("active_quests", {})
		quests = av.active_quests.quests
		quests[self.name] = QuestData()

		av.add_or_attach_component("quests", {})
		quest = av.quests.quests[self.name]

		if quest['status'] != "complete":
			quest['status'] = 'active'
			self.next(av, stage)

	def available(self, av):
		return True

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
		

class QuestManager():

	def __init__(self):
		self.quests = []

	def add(self, quest):
		self.quests.append(quest)

	def attach_available(self, av):
		av.add_or_attach_component("quests", {})
		av.add_or_attach_component("active_quests", {})
		av_quests = av.quests.quests
		actv_quests = av.active_quests.quests

		for quest in self.quests:
			if quest.name in actv_quests or quest.name in av_quests and av_quests[quest.name]['status'] == "complete":
				continue
			if quest.name in av_quests:
				#already have it. Need to check status and reinit?
				q = av_quests[quest.name]
				logging.info(q)
				stage = q["stage"] if "stage" in q else None
				if stage is None:
					quest.start(av)
				else:
					quest.start(av, stage)
				continue

			#If the quest is available to the player add it to the list
			if quest.available(av):
				av_quests[quest.name] = {"status":"available"}
				quest.start(av)