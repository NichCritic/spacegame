'''
Created on 2014-03-23

@author: Nich
'''

class SystemSet(object):
    '''
    classdocs
    '''


    def __init__(self):
        self.systems = []
        
    def register(self, system):
        self.systems.append(system)
        
    def process(self):
        for sys in self.systems:
            sys.process()
            
class DBSystemSet(SystemSet):
    def __init__(self, db_components, sessionmaker):
        super().__init__()
        self.db_components = db_components
        self.sessionmaker = sessionmaker
    
    def process(self):
        with self.sessionmaker.get_session() as session:
            self.db_components.set_session(session)
            super().process()
        
            
        