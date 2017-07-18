from pynlg.realizer import NounPhrase, VerbPhrase, PrepositionalPhrase, Clause


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
        noun = obj['name']
        descriptors = []
        if obj['material']:
            descriptors.append(obj['material']['descriptor'])
        descriptors.extend(obj['descriptors'])
        return {
            'noun': noun,
            'descriptors': descriptors
        }

    def describe_object(self, obj):
        pp = self.preprocess(obj)
        ads = [self.lex.getWord(desc, 'ADJECTIVE')
               for desc in pp['descriptors']]
        noun = NounPhrase(self.lex.getWord(pp['noun'], 'NOUN'), adjectives=ads)
        noun.add_determiner(self.lex.getWord('a'))
        return noun
