import nltk.data

from parser.plaintext import PlaintextParser
from summarizer.lex_rank import LexRank
from utils import to_unicode, ItemsCount
from stemmer.stemmer import Stemmer

# Get the input data/text
fpath = "para1.txt"
myfile = open(fpath, 'r')
data = myfile.read()

text = '''
Punkt knows that the periods in Mr. Smith and Johann S. Bach do not mark sentence boundaries. And sometimes sentences can start with non-capitalized words.  i is a good variable name.
'''
# Tokenizer for english text
tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
# Parser for english text
# parser = PlaintextParser(text,tokenizer) # for english text above

parser = PlaintextParser(data,tokenizer) # for data from file above
# print("document - ", parser.document)
# print("sentences - ", parser.sentences)
# for s in parser.to_sentences(text):
#     print(parser.to_words(s))


# Stop words for english text
fpath = "stop-words.txt"
stopwords_file = open(fpath, 'r')
stopwords_data = stopwords_file.read()
stop_words = frozenset(w.rstrip() for w in to_unicode(stopwords_data).splitlines() if w)

# return_count
return_count = 5

stemmer = Stemmer()
summarizer = LexRank(stemmer, parser)
summarizer.stop_words = stop_words
summarizer(parser, return_count)


items_count = ItemsCount("10%")
print("items_count ", items_count("test"))

