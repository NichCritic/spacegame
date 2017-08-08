from pynlg.realizer import NounPhrase, VerbPhrase, PrepositionalPhrase, Clause
from pynlg.lexicon import Noun, Adjective, Verb


class ObjectDescriber(object):

    def __init__(self, lexicon):
        self.lex = lexicon

    '''
    Find the target in the provided tree, then splits the tree at that level, creating a list of objects to render
    '''

    def group_by_target(self, obj, target):
        pass

    def describe_graph(self, graph_node, target=None):
        if target is None:
            stack = [graph_node]
            there = NounPhrase(self.lex.getWord('there', 'NOUN'))
            
            while 'subject' in stack[0]:
                stack.insert(0, stack[0]['subject'])

            elem = stack[0]
            if 'action' in elem:
                vb = self.lex.getWord(elem['action']['verb'], 'VERB')
                adj = self.lex.getWord(
                    elem['action']['character'], 'ADJECTIVE')
                subject = NounPhrase(self.lex.getWord(
                    elem['action']['type'], 'NOUN'), adjectives=[adj])
                subject.add_determiner(self.lex.getWord('a'))
                vp = VerbPhrase(vb)
                pp = PrepositionalPhrase(self.lex.getWord('from'), noun_phrases=[
                                         self.describe_object(elem)])
                vp.add_prepositional_phrase(pp)
                clause = Clause(subject, vp)
            else:
                vp = VerbPhrase(self.lex.getWord(
                        'be'), direct_object=self.describe_object(elem))
                clause = Clause(there, vp)
            for elem in stack[1:]:
                pp = PrepositionalPhrase(self.lex.getWord(elem['location'], 'PREPOSITION'), noun_phrases=[
                    self.describe_object(elem['object'])])
                vp.add_prepositional_phrase(pp)
            

            return clause.realize()

    def preprocess(self, obj):
        noun = obj.names.name
        descriptors = []
        if obj.has('material'):
            descriptors.append(obj.material.get_material()['descriptor'])
        return {
            'noun': noun,
            'descriptors': descriptors
        }

    def get_noun(self, word, is_name):
        ret = None
        try:
            ret = self.lex.getWord(word, 'NOUN')
        except Exception:
            ret = Noun(word, features=['proper'] if is_name else [])
        return ret

    def get_adjective(self, word):
        ret = None
        try:
            ret = self.lex.get_word(word, 'ADJECTIVE')
        except Exception:
            ret = Adjective(word, category='ADJECTIVE')
        return ret


    def describe_object(self, obj):
        pp = self.preprocess(obj)
        ads = [self.get_adjective(desc)
               for desc in pp['descriptors']]
        subject = self.get_noun(pp['noun'], obj.has('avatar_type'))
        noun = NounPhrase(subject, adjectives=ads)
        if not 'proper' in subject.features:
            noun.add_determiner(self.lex.getWord('a'))
        return noun
