
'''
Created on 2014-03-14

@author: Nich
'''


class AVEvent(object):

    def __init__(self, msg_type, text, location, source_id, message_templates, target_id=None, **kwargs):
        self.msg_type = msg_type
        self.text = text
        self.location = location
        self.source_id = source_id
        self.message_templates = message_templates
        self.target_id = target_id
        self.kwargs = kwargs
        self.visited = []
        self.handled = False

    def mark_visited(self, e_id):
        self.visited.append(e_id)

    def has_visited(self, e_id):
        return e_id in self.visited

    def handle(self):
        self.handled = True
