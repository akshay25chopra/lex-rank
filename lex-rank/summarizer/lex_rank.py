from utils import to_unicode
import math

class LexRank(object):


    _stop_words = frozenset()

    def __init__(self, stemmer, parser):
        self._stemmer = stemmer
        self._parser = parser

    def __call__(self, parser, return_count):
        # self._ensure_dependencies_installed()
        sentence_words = [self._to_word_set(s) for s in parser.sentences]
        idf_metrics = self._compute_idf(sentence_words)


    @property
    def stop_words(self):
        return self._stop_words

    @stop_words.setter
    def stop_words(self, words):
        self._stop_words = frozenset(map(self.normalize_word, words))


    def _to_word_set(self, sentence):
        words = map(self.normalize_word, self._parser.to_words(sentence))
        return [self.stem_word(w) for w in words if w not in self._stop_words]

    def normalize_word(self, word):
        return to_unicode(word).lower()

    def stem_word(self, word):
        return self._stemmer(self.normalize_word(word))

    # @staticmethod
    # def compute_idf(sentences, parser):
    #     idf_metrics = {}
    #     sentences_count = len(sentences)
    #     for sentence in sentences:
    #         words = parser.to_words(sentence)
    #         for term in words:
    #             if term not in idf_metrics:
    #                 term_sum = sum(1 for s in sentences if term in s)
    #                 idf_metrics[term] = math.log(sentences_count / (1 + term_sum))
    #     return idf_metrics

    @staticmethod
    def _compute_idf(sentences):
        idf_metrics = {}
        sentences_count = len(sentences)
        for sentence in sentences:
            for term in sentence:
                if term not in idf_metrics:
                    n_j = sum(1 for s in sentences if term in s)
                    idf_metrics[term] = math.log(sentences_count / (1 + n_j))
        print(idf_metrics)
        return idf_metrics