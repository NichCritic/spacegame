'''
Created on 2013-11-06

@author: Nich
'''

from parsimonious.grammar import Grammar
#from parsimonious.exceptions import ParseError
from parsimonious.nodes import NodeVisitor
import logging

#TODO: make grammar dynamic based on the objects in the room


#print(grammar.parse('((bold stuff))'))
"""
        command = (verb to_player text+) / (verb to_object text+) / (verb text+)
        verb = "say" / "go"
        to_player = signifier player
        to_object = signifier object
        text        = ~"[A-Z 0-9]*"i
        player = "julie" / "alex" / "alice" / "bob" / "judy" 
        object = "chair" / "couch" / "door"
        signifier = " to "
"""


def surround(surrounding_text, text):
    return surrounding_text+text+surrounding_text

def format_objects(object_name_list):
    if len(object_name_list) > 0:
        return " / ".join([surround('"', text) for text in object_name_list])
    else:
        return '"nothing"'

def build_grammar(names, spells, verbs):
    nouns_format = format_objects(names)
    spells_format = format_objects(spells)
    verbs_format = format_objects(verbs)

    print(spells_format)
    
    command_grammar = Grammar(
        """
            command = isa / vpn
            isa = (noun s "is" s text)
            vpn = (say s preposition s noun s text) / (say s text) / (create s text) / (cast s spell s preposition s noun) / (cast s spell) / (verb s noun s preposition s noun) / (verb s preposition s noun) / (verb s noun) / (verb)
            say = "say"
            create = "create"
            cast = "cast"
            verb = (adverb s verb) / {verbs_format}
            noun = {nouns_format}
            preposition = "to" / "through" / "at" / "on"
            adverb = "quickly"
            text = ~".*"
            spell = {spells_format}
            s = " "
        """.format(nouns_format=nouns_format, spells_format = spells_format, verbs_format = verbs_format))
    return command_grammar

class CommandTokenMatcher():
    def __init__(self, command_context = None):
        self.command_context = {}
        
    
    def map_command(self, command, command_context):
        names = command_context["names"].names
        spells = command_context["spells"]
        verbs = command_context["verbs"]
        command_grammar = build_grammar(names, spells, verbs)
        ast = command_grammar.parse(command)
        import pdb; pdb.set_trace()
        mapping = CommandVisitor().visit(ast)
        return mapping


#command_grammar = build_grammar(["julie", "alex", "alice", "bob", "judy"], ["couch", "chair",], ["door"])
#command_grammar.parse("say to alice hello world")


class CommandVisitor(NodeVisitor):
    def __init__(self):
        
        self.matched_dict = {}
        
    def visit_command(self, node, visited_children):
        #print(node)
        #print(visited_children)
        
        
        return self.matched_dict

    def visit_isa(self, node, visited_children):
        self.matched_dict["command_type"]  = 'isa'

    def visit_vpn(self, node, visited_children):
        self.matched_dict["command_type"]  = 'vpn'
    
    def visit_verb(self, node, visited_children):
        
        self.matched_dict["verb"] = node.text
        
        return node

    def visit_say(self, node, visited_children):
        self.matched_dict["verb"] = node.text

        return node

    def visit_create(self, node, visited_children):
        self.matched_dict["verb"] = node.text

        return node

    def visit_cast(self, node, visited_children):
        self.matched_dict["verb"] = node.text

        return node
    
    def visit_text(self, node, visited_children):
        if node.text != '':
            self.matched_dict["text"] = node.text
        
        return node

    def visit_spell(self, node, visited_children):
        self.matched_dict["spell"] = node.text
        return node
        
    def visit_noun(self, node, visited_children):
        if not "targets" in self.matched_dict:
            self.matched_dict["targets"] = []
        self.matched_dict["targets"].append(node.text)
        return node
    
    def visit_preposition(self, node, visited_children):
        self.matched_dict["p_type"] = node.text
        
        return node
    
    def generic_visit(self, node, visited_children):
        #print("do visit generic")
        # print(visited_children)
        
        return node


'''
class CommandVisitor(NodeVisitor):
    def __init__(self, command_context):
        self.command_context = command_context
        
    def visit_command(self, node, visited_children):
        
        flat_children = flatten(visited_children, ltypes = list)
        #print(flat_children)
        results = {}
        for ch in flat_children:
            if ch[0] in results:
                results[ch[0]] += ch[1]
            else:
                results[ch[0]] = ch[1]
        return results
    
    def visit_verb(self, node, visited_children):
        #print("do visit verb")
        return (node.expr_name, node.text)
    
    
    def visit_to_player(self, node, visited_children):
        to, player = visited_children
        player_object = self.command_context["players"][player[1]]
        
        return ("target", player_object)    
    
        
    
    def visit_num(self, node, visited_children):
        
        
        return (node.expr_name, node.text+" ")
         
    
    
        
    def visit_player(self, node, visited_children):
        #print("do visit player")
        return (node.expr_name, node.text)
    
    def visit_object(self, node, visited_children):
        #print("do visit object")
        return (node.expr_name, node.text)
    
    
    def visit_text(self, node, visited_children):
        """Return the text verbatim."""
        #print("do visit text")
        return (node.expr_name, node.text)
    
    
    def generic_visit(self, node, visited_children):
        #print("do visit generic")
       # print(visited_children)
        
        return visited_children

    
    
def flatten(l, ltypes=(list, tuple)):
    ltype = type(l)
    l = list(l)
    i = 0
    while i < len(l):
        while isinstance(l[i], ltypes):
            if not l[i]:
                l.pop(i)
                i -= 1
                break
            else:
                l[i:i + 1] = l[i]
        i += 1
    return ltype(l)   
    
    
    '''  
    
    
    
    
    
    
            
    
    
    
    