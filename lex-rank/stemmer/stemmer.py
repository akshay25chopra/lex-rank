# Created by Shivalik
#
# Usage :
# s = Stemmer()
# print(s.stem_word("Stemming"))
# or
# print(s("Stemming"))


from nltk.stem.porter import PorterStemmer

class Stemmer(object):
    def __init__(self):
        self._ps = PorterStemmer()

    def __call__(self, word):
        return self._ps.stem(word)

    def stem_word(self, word):
        return self._ps.stem(word)