class Quest():
	def __init__(self, node_factory):
		self.node_factory = node_factory
		self.state = "inactive"
		


class QuestStage():

	def __init__(self, node_factory):
		self.node_factory = node_factory
		self.next_stage = None

	def register_next(self, stage):
		self.next_stage = stage

	def attach(self, av):
		pass

	def next(self, av):
		pass

	def initialize_world(self, av):
		pass

	def register_systems(self, system_set):
		pass