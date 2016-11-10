from __future__ import absolute_import

class PlaintextParser(object):
    def __init__(self,data,tokenizer):
        print("hello parser")
        self._text = data.strip()
        self.formdocument()

    def formdocument(self):
        # initialize document, sentences and words here
        self.document = "wonderful" + self._text
        return