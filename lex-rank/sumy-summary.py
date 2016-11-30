from sumy.sumy.nlp.tokenizers import Tokenizer
from sumy.sumy.parsers.plaintext import PlaintextParser
from sumy.sumy.nlp.stemmers import Stemmer
from sumy.sumy.summarizers.lex_rank import LexRankSummarizer
from sumy.sumy.utils import get_stop_words

LANGUAGE = "english"
SENTENCES_COUNT = "10%"

fpath = "para2.txt"
sentencesList = []
parser = PlaintextParser.from_file(fpath, Tokenizer(LANGUAGE))
stemmer = Stemmer(LANGUAGE)
summarizer = LexRankSummarizer(stemmer)
summarizer.stop_words = get_stop_words(LANGUAGE)

for sentence in summarizer(parser.document, SENTENCES_COUNT):
    sentencesList.append(sentence._text)

for sentence in sentencesList:
    print((sentence))
