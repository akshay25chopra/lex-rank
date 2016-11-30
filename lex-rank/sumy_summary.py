from sumy.sumy.nlp.tokenizers import Tokenizer
from sumy.sumy.parsers.plaintext import PlaintextParser
from sumy.sumy.nlp.stemmers import Stemmer
from sumy.sumy.summarizers.lex_rank import LexRankSummarizer
from sumy.sumy.utils import get_stop_words

def getSumySummary(fpath, return_count):
    LANGUAGE = "english"
    sentencesList = []
    parser = PlaintextParser.from_file(fpath, Tokenizer(LANGUAGE))
    stemmer = Stemmer(LANGUAGE)
    summarizer = LexRankSummarizer(stemmer)
    summarizer.stop_words = get_stop_words(LANGUAGE)

    for sentence in summarizer(parser.document, return_count):
        sentencesList.append(sentence._text)

    final_summary = ' '.join(sentencesList)
    return final_summary


# mytxt = getSumySummary(fpath, return_count)
# print(mytxt)