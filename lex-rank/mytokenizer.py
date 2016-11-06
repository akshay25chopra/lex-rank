import nltk.data

text = '''
Punkt knows that the periods in Mr. Smith and Johann S. Bach do not mark sentence boundaries.  And sometimes sentences can start with non-capitalized words.  i is a good variable name.
'''

tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')

print(tokenizer.tokenize(text.strip()))