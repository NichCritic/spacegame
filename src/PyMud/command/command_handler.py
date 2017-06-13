'''
Created on 2011-08-13

@author: Nich
'''

import logging    
#import PyMud.command.command_token_matcher as command_token_matcher
from parsimonious.exceptions import ParseError

class CommandHandler():
    
    def __init__(self, command_token_matcher, command_packager, command_executor, command_context_builder):
        self.command_token_matcher = command_token_matcher
        self.command_packager = command_packager
        self.command_executor = command_executor
        self.command_context_builder = command_context_builder
        
    def handle_command(self, source, command):               
        logging.info("handler got "+command+" from "+str(source.id))
        try: 
            command_context = self.command_context_builder.build_command_context(source)
            
            
            command_mapping = self.command_token_matcher.map_command(command, command_context)
            
            
            command_package = self.command_packager.find_command(command_mapping, command_context)
            
            self.command_executor.execute(command_package)
            
            return ("success",)
        except ParseError as e:
            print(e)
            return ("error", "the input wasn't recognized as a command")
        
        
    