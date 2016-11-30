from utils import to_unicode, ItemsCount
import math
import collections
import numpy
from collections import namedtuple
from operator import attrgetter


SentenceInfo = namedtuple("SentenceInfo", ("sentence", "order", "rating",))

class LexRank(object):


    stop_words_set = frozenset()
    threshold = 0.1
    epsilon = 0.1

    def __init__(self, stemmer, parser):
        self._stemmer = stemmer
        self._parser = parser

    def summarize(self, parser, return_count):
        sentence_words = [self.sentence_to_words(s) for s in parser.sentences]
        # print(sentence_words)
        tf_metrics = self.calculate_term_frequency(sentence_words)
        # print(tf_metrics)
        idf_metrics = self.calculate_idf(sentence_words)
        # print(idf_metrics)

        matrix = self.create_matrix(sentence_words, self.threshold, tf_metrics, idf_metrics)
        scores = self.power_method(matrix, self.epsilon)
        ratings = dict(zip(parser.sentences, scores))

        return self.get_summary_sentences(parser.sentences, return_count, ratings)


    @property
    def stop_words(self):
        return self.stop_words_set

    def stop_words(self, words):
        self.stop_words_set = frozenset(map(self.normalize_word, words))

    def sentence_to_words(self, sentence):
        words = map(self.normalize_word, self._parser.to_words(sentence))
        return [self.stem_word(w) for w in words if w not in self.stop_words_set]

    def normalize_word(self, word):
        return to_unicode(word).lower()

    def stem_word(self, word):
        return self._stemmer(self.normalize_word(word))

    # term frequency in each sentence
    def calculate_term_frequency(self, sentences):
        tf_values = map(collections.Counter, sentences)
        tf_metrics = []
        for sentence in tf_values:
            metrics = {}
            max_tf = max(sentence.values()) if sentence else 1

            for term, tf in sentence.items():
                metrics[term] = tf / max_tf

            tf_metrics.append(metrics)
        # print(tf_metrics)
        return tf_metrics


    # term popularity in all sentences combined
    @staticmethod
    def calculate_idf(sentences):
        idf_metrics = {}
        sentences_count = len(sentences)
        for sentence in sentences:
            for term in sentence:
                if term not in idf_metrics:
                    term_count = sum(1 for s in sentences if term in s)
                    idf_metrics[term] = math.log(sentences_count / (1 + term_count))
        # print(idf_metrics)
        return idf_metrics


    def create_matrix(self, sentences, threshold, tf_metrics, idf_metrics):

        # create matrix |sentences|×|sentences| filled with zeroes
        sentences_count = len(sentences)
        matrix = numpy.zeros((sentences_count, sentences_count))
        degrees = numpy.zeros((sentences_count,))

        for row, (sentence1, tf1) in enumerate(zip(sentences, tf_metrics)):
            # print("sentence1:", sentence1)
            # print("tf1:", tf1)
            for col, (sentence2, tf2) in enumerate(zip(sentences, tf_metrics)):
                matrix[row, col] = self.sentence_cosine(sentence1, sentence2, tf1, tf2, idf_metrics)

                if matrix[row, col] > threshold:
                    matrix[row, col] = 1.0
                    degrees[row] += 1
                else:
                    matrix[row, col] = 0

        for row in range(sentences_count):
            for col in range(sentences_count):
                if degrees[row] == 0:
                    degrees[row] = 1

                matrix[row][col] = matrix[row][col] / degrees[row]

        return matrix

    @staticmethod
    def sentence_cosine(sentence1, sentence2, tf1, tf2, idf_metrics):
        common_words = frozenset(sentence1) & frozenset(sentence2)

        numerator = 0.0
        for term in common_words:
            numerator += tf1[term] * tf2[term] * idf_metrics[term] ** 2

        denominator1 = sum((tf1[t] * idf_metrics[t]) ** 2 for t in sentence1)
        denominator2 = sum((tf2[t] * idf_metrics[t]) ** 2 for t in sentence2)

        if denominator1 > 0 and denominator2 > 0:
            return numerator / (math.sqrt(denominator1) * math.sqrt(denominator2))
        else:
            return 0.0

    @staticmethod
    def power_method(matrix, epsilon):
        transposed_matrix = matrix.T
        sentences_count = len(matrix)
        p_vector = numpy.array([1.0 / sentences_count] * sentences_count)
        lambda_val = 1.0

        while lambda_val > epsilon:
            next_p = numpy.dot(transposed_matrix, p_vector)
            lambda_val = numpy.linalg.norm(numpy.subtract(next_p, p_vector))
            p_vector = next_p

        return p_vector

    def get_summary_sentences(self, sentences, count, rating, *args, **kwargs):
        rate = rating
        if isinstance(rating, dict):
            assert not args and not kwargs
            rate = lambda s: rating[s]

        infos = (SentenceInfo(s, o, rate(s, *args, **kwargs))
                 for o, s in enumerate(sentences))

        # sort sentences in descending order
        infos = sorted(infos, key=attrgetter("rating"), reverse=True)
        if not isinstance(count, ItemsCount):
            count = ItemsCount(count)
        infos = count(infos)
        # sort sentences by their order in document
        infos = sorted(infos, key=attrgetter("order"))
        return tuple(i.sentence for i in infos)
