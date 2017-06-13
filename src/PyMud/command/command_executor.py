'''
Created on 2013-11-18

@author: Nich
'''
class CommandExecutor(object):
    
    
        
    
    def execute(self, command_package):
        command, args = command_package
        command(**args)