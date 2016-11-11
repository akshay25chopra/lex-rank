import nltk.data

from parser.plaintext import PlaintextParser
from utils import to_unicode

fpath = "para1.txt"
myfile = open(fpath, 'r')
data = myfile.read()

text = '''
Punkt knows that the periods in Mr. Smith and Johann S. Bach do not mark sentence boundaries.  And sometimes sentences can start with non-capitalized words.  i is a good variable name.
'''
tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')

parser = PlaintextParser(text,tokenizer)
print("document - ", parser.document)
print("sentences - ", parser.sentences)

for s in parser.to_sentences(text):
    print(parser.to_words(s))


