from __future__ import absolute_import
from __future__ import division, print_function, unicode_literals


def _get_ngrams(n, text):
	ngram_set = set()
	text_length = len(text)
	max_index_ngram_start = text_length - n
	for i in range (max_index_ngram_start + 1):
		ngram_set.add(tuple(text[i:i+n]))
	return ngram_set


def _split_into_words(sentences):
    sentences = sentences.split()
    fullTextWords = []
    for s in sentences:
        fullTextWords.extend(s)
    return fullTextWords


def _get_word_ngrams(n, sentences):
	assert (len(sentences) > 0)
	assert (n > 0)

	words = _split_into_words(sentences)
	return _get_ngrams(n, words)


def rouge_n(evaluated_sentences, reference_sentences, n):

    if len(evaluated_sentences) <= 0 or len(reference_sentences) <= 0:
        raise (ValueError("Collections must contain at least 1 sentence."))

    evaluated_ngrams = _get_word_ngrams(n, evaluated_sentences)
    reference_ngrams = _get_word_ngrams(n, reference_sentences)
    reference_count = len(reference_ngrams)

    # Gets the overlapping ngrams between evaluated and reference
    overlapping_ngrams = evaluated_ngrams.intersection(reference_ngrams)
    overlapping_count = len(overlapping_ngrams)

    return overlapping_count / reference_count


evalSenList = []
refSenList = []
fileNameList = []
f = open("/home/shivalik/Documents/GitHub Projects/NLP_text_summarization/lex-rank/output.txt", 'r')
for line in f:
    if 'Filename' in line:
        fileNameList.append(line)

    if 'Our Summary' in line:
        evalSenList.append(str(f.__next__()))

    if 'Reference Summary' in line:
        refSenList.append(str(f.__next__()))

f.close()

print("Filename, Similarity")
for i in range(0, len(fileNameList)):
    print(fileNameList[i].strip('\n')[9:], "," ,round((rouge_n(evalSenList[i], refSenList[i], 2) * 100),2))
