from utils import to_unicode

class LexRank(object):


    _stop_words = frozenset()

    def __init__(self, stemmer, parser):
        self._stemmer = stemmer
        self._parser = parser

    def __call__(self, parser, return_count):
        # self._ensure_dependencies_installed()
        sentence_words = [self._to_word_set(s) for s in parser.sentences]
        print(sentence_words)


    @property
    def stop_words(self):
        return self._stop_words

    @stop_words.setter
    def stop_words(self, words):
        self._stop_words = frozenset(map(self.normalize_word, words))


    def _to_word_set(self, sentence):
        words = map(self.normalize_word, self._parser.to_words(sentence))
        wdset = [self.stem_word(w) for w in words if w not in self._stop_words]
        # wdset = [w for w in words if w not in self._stop_words]
        return wdset


    def normalize_word(self, word):
        return to_unicode(word).lower()

    def stem_word(self, word):
        return self._stemmer(self.normalize_word(word))