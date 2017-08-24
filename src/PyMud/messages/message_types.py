'''
Created on 2013-11-21

@author: Nich
'''

class AVMessage(object):
    '''
    classdocs
    '''


    def __init__(self, msg_type, text, location, source_id, message_templates, target_id = None, **kwargs):
        self.msg_type = msg_type
        self.text = text
        self.location = location
        self.source_id = source_id
        self.message_templates = message_templates
        self.target_id = target_id
        self.kwargs = kwargs