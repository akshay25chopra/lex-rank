import nltk.data

from parser.plaintext import PlaintextParser
from summarizer.lex_rank import LexRank
from utils import to_unicode, ItemsCount
from stemmer.stemmer import Stemmer

def getLexRankSummary(fpath, return_count):
    # Get the input data/text
    myfile = open(fpath, 'r')
    data = myfile.read()

    # Tokenizer for english text
    tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
    # Parser for english text
    parser = PlaintextParser(data,tokenizer) # for data from file above

    # print("document - ", parser.document)
    # print("sentences - ", parser.sentences)
    # for s in parser.to_sentences(text):
    #     print(parser.to_words(s))

    # Stop words for english text
    stop_words_path = "stop-words.txt"
    stopwords_file = open(stop_words_path, 'r')
    stopwords_data = stopwords_file.read()
    stop_words = frozenset(w.rstrip() for w in to_unicode(stopwords_data).splitlines() if w)
    stemmer = Stemmer()
    summarizer = LexRank(stemmer, parser)
    summarizer.stop_words = stop_words
    if len(parser.sentences) == 0:
        print(fpath)
        return 'empty'
    summary = summarizer.summarize(parser, return_count)

    final = ' '.join(summary)
    return final

# fpath = "data/para2.txt"
# return_count = "10%"
# print(getLexRankSummary(fpath, return_count))

