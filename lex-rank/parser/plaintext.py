from __future__ import absolute_import
from utils import to_unicode
from nltk.tokenize.treebank import TreebankWordTokenizer

class PlaintextParser(object):
    def __init__(self,data,tokenizer):
        print("parser.__init__")
        self._text = to_unicode(data).strip()
        self._tokenizer = tokenizer
        self._treebank_word_tokenize = TreebankWordTokenizer().tokenize
        self.formdocument()
        self.extractsentences()
        self.extractwords()

    def formdocument(self):
        self.document = self._text
        return

    def extractsentences(self):
        sentences = self._tokenizer.tokenize(self._text.strip())
        self.sentences = sentences
        return


    def extractwords(self):
        words = [token for sent in self._tokenizer.tokenize(self._text.strip())
         for token in self._treebank_word_tokenize(sent)]
        self.words = words
        return

    def to_words(self, sentence):
        words = [token for sent in self._tokenizer.tokenize(sentence)
         for token in self._treebank_word_tokenize(sent)]
        return words

    def to_sentences(self, document):
        sentences = self._tokenizer.tokenize(document)
        return sentences