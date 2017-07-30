from object.baseobject import Entity
from objects.components import *

class ObjectFinder(object):

	def __init__(self, session_manager):
		self.session_manager = session_manager

	def find_object(name, room_id = None):
		with self.session_manager.get_session() as session:
			q = session.query(Entity).join(Names)
			if room_id:
				q.join(Location)
				q.filter(Location.room == room_id)
			q.filter(Names.name.contains(name))
			return q.value(Entity.id)
