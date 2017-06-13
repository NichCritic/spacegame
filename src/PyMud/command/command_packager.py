'''
Created on 2013-11-06

Not sure what I'm doing here yet. The packager needs to be able to find the resources a command needs to function



@author: Nich
'''

from collections import namedtuple

CommandPackage = namedtuple("CommandPackage", "verb_function reqs_dict")


class CommandPackager(object):

    def __init__(self, verbs):
        
        self.verbs = verbs
    
    
        

    def package_command(self, verb_def, reqs):
              
        return CommandPackage(verb_def["function"], reqs)
            
                
    def handle_verb(self, verb):
        return self.verbs[verb]    
        
    
    def find_command(self, parsed_elements, command_context):
        reqs = command_context
        #calling_player_object = self.data_cache.find_some_player(calling_player)
        #reqs["calling_player"] = calling_player_object
        print(parsed_elements)
        for elemtype, element in parsed_elements.items():
            if elemtype == "verb":
                verb_definition = self.handle_verb(element)
            if elemtype == "text":
                reqs["text"] = element
            if elemtype == "target":
                reqs["target"] = element
            if elemtype == "num":
                nums = element.strip().split(" ")
                reqs["x"] = int(nums[0])
                reqs["y"] = int(nums[1])
                if len(nums) == 3:
                    reqs["z"] = int(nums[2])
                else:
                    reqs["z"] = None
            
            #handle more elemtypes
        
        command_package = self.package_command(verb_definition, reqs)
        return command_package
    

    
        
        


        
        
            
            
            
            


