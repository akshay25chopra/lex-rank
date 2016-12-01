
opfile = r"/Users/arorai/projects/text-summarization/lex-rank/output.txt"
# opfile = "/home/shivalik/Documents/GitHub Projects/NLP_text_summarization/lex-rank/output.txt"

def get_bigram(text):
    n = 2
    ngram_set = set()
    text_length = len(text)
    max_index_ngram_start = text_length - n
    for i in range (max_index_ngram_start + 1):
        ngram_set.add(tuple(text[i:i+n]))
    return ngram_set


def get_word_bigrams(sentences):
    sentences = sentences.split()
    words = []
    for s in sentences:
        words.extend(s)
    # print(words)
    return get_bigram(words)


def rouge_bigrams(our_summary, ref_summary):

    our_sum_bigram = get_word_bigrams(our_summary)
    ref_sum_bigram = get_word_bigrams(ref_summary)
    total_ref_sum_bigrams = len(ref_sum_bigram)

    matching_bigrams = our_sum_bigram.intersection(ref_sum_bigram)
    total_matching_bigrams = len(matching_bigrams)

    # print(our_sum_bigram)
    # print("---------------")
    # print(ref_sum_bigram)
    # print(total_ref_sum_bigrams)
    # print(total_matching_bigrams)

    if total_ref_sum_bigrams == 0:
        return 0

    return total_matching_bigrams / total_ref_sum_bigrams


ourSummary = []
refSummary = []
fileNameList = []
f = open(opfile, 'r')

for line in f:
    if 'Filename' in line:
        fileNameList.append(line)

    if 'Our Summary' in line:
        ourSummary.append(str(f.__next__()))

    if 'Reference Summary' in line:
        refSummary.append(str(f.__next__()))

f.close()


evaluation = "evaluation.csv"
evaluation_file = open(evaluation, 'w')
count = 0
total = 0
evaluation_file.write("Filename, Similarity" + '\n')
for i in range(0, len(fileNameList)):
    fileName = fileNameList[i].strip('\n')[9:]
    similarity = round((rouge_bigrams(ourSummary[i], refSummary[i]) * 100),2)
    count += similarity
    data = fileName + ", " + str(similarity)
    evaluation_file.write(data + '\n')
    total += 1

evaluation_file.write("Average: " + str(round((count/total),2)))
evaluation_file.close()