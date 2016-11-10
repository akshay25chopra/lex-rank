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

parser = PlaintextParser(data,tokenizer)
print(parser.document)

print(to_unicode("café"))
print(to_unicode("Hello there... ☃!"))
print("Hello there... ☃!")
