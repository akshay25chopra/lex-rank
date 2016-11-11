from utils import to_unicode

fpath = "stop-words.txt"
stopwords_file = open(fpath, 'r')
stopwords_data = stopwords_file.read()
stop_words = frozenset(w.rstrip() for w in to_unicode(stopwords_data).splitlines() if w)
print(stop_words)