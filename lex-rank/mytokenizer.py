import nltk.data

# text = '''
# Punkt knows that the periods in Mr. Smith and Johann S. Bach do not mark sentence boundaries.  And sometimes sentences can start with non-capitalized words.  i is a good variable name.
# '''

fpath = "para1.txt"
myfile = open(fpath, 'r')
text = myfile.read()

tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
print("tokenized:")
print(tokenizer.tokenize(text.strip()))
