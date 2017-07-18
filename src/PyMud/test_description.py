import os
from description.description import ObjectDescriber
from objects.chair import chair, table, rel1, rell2

from pynlg.lexicon import XMLLexicon



if __name__ == '__main__':
	print(chair)
	lex = XMLLexicon(os.path.join(os.path.dirname(__file__), 'lexicon/default-lexicon.xml'))
	od = ObjectDescriber(lex)
	print(od.describe_object(chair).realize())

	print(table)
	print(od.describe_object(table).realize())

	print(od.describe_graph(rel1))
	print(od.describe_graph(rell2))