from utils import to_unicode
import math
import collections
import numpy

class LexRank(object):


    _stop_words = frozenset()
    threshold = 0.1

    def __init__(self, stemmer, parser):
        self._stemmer = stemmer
        self._parser = parser

    def __call__(self, parser, return_count):
        # self._ensure_dependencies_installed()
        sentence_words = [self._to_word_set(s) for s in parser.sentences]
        tf_metrics = self._compute_tf(sentence_words)
        idf_metrics = self._compute_idf(sentence_words)

        matrix = self._create_matrix(sentence_words, self.threshold, tf_metrics, idf_metrics)


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

    # term frequency in each sentence
    def _compute_tf(self, sentences):
        tf_values = map(collections.Counter, sentences)
        tf_metrics = []
        for sentence in tf_values:
            metrics = {}
            max_tf = max(sentence.values()) if sentence else 1

            for term, tf in sentence.items():
                metrics[term] = tf / max_tf

            tf_metrics.append(metrics)
        print(tf_metrics)
        return tf_metrics


    # term popularity in all sentences combined
    @staticmethod
    def _compute_idf(sentences):
        idf_metrics = {}
        sentences_count = len(sentences)
        for sentence in sentences:
            for term in sentence:
                if term not in idf_metrics:
                    term_count = sum(1 for s in sentences if term in s)
                    idf_metrics[term] = math.log(sentences_count / (1 + term_count))
        print(idf_metrics)
        return idf_metrics


    def _create_matrix(self, sentences, threshold, tf_metrics, idf_metrics):
        """
        Creates matrix of shape |sentences|×|sentences|.
        """
        # create matrix |sentences|×|sentences| filled with zeroes
        sentences_count = len(sentences)
        matrix = numpy.zeros((sentences_count, sentences_count))
        degrees = numpy.zeros((sentences_count,))

        # for row, (sentence1, tf1) in enumerate(zip(sentences, tf_metrics)):
        #     for col, (sentence2, tf2) in enumerate(zip(sentences, tf_metrics)):
        #         matrix[row, col] = self._compute_cosine(sentence1, sentence2, tf1, tf2, idf_metrics)
        #
        #         if matrix[row, col] > threshold:
        #             matrix[row, col] = 1.0
        #             degrees[row] += 1
        #         else:
        #             matrix[row, col] = 0
        #
        # for row in range(sentences_count):
        #     for col in range(sentences_count):
        #         if degrees[row] == 0:
        #             degrees[row] = 1
        #
        #         matrix[row][col] = matrix[row][col] / degrees[row]

        print("matrix:", matrix)
        print("degrees:", degrees)

        return matrix
