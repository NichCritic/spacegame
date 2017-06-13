'''
Created on 2014-03-26

@author: Nich
'''
from parsimonious.grammar import Grammar
#from parsimonious.exceptions import ParseError
from parsimonious.nodes import NodeVisitor




command_grammar = Grammar("""
        command = (verb s preposition s coords) / (verb s noun s preposition s noun text) / (verb s preposition s noun text) / (verb s noun text) / (verb text)
        coords = (num s num s num) / (num s num)
        verb = "say" / "move" / "look"
        noun = {nouns}
        preposition = "to" / "through" / "at"
        text = ~"[A-Z 0-9]*"i
        num = ~"[0-9]+"i
        s = " "
""")




        
        
    
    




