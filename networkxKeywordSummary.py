import editdistance
import networkx as nx
import itertools
import nltk
import os
from nltk.corpus import stopwords

stop = set(stopwords.words('english'))
punctuations = ['!', '"', '#', '$', '%', '&', '\'', ',', '(', ')', '*', '+', ',', '-', '.', '/', ':', ';', '<', '=',
                '>', '?', '@', '[', '\\', ']', '^', '_', '`', '{', '|', '}', '~']

tempwordlist = []
finalWords =  []





def processDoc(filename):
    f = open(filename, 'r')
    file1 = f.read()
    file1 = file1.lower()
    words = nltk.tokenize.word_tokenize(file1)
    #print(words)
    for i in words:
        if i not in punctuations and stop:
            tempwordlist.append(i)

    posTags = nltk.pos_tag(tempwordlist)
    #print(posTags)

    for i in posTags:
        if i[1] in ['NN','ADJ']:
            finalWords.append(i[0])

    #print(finalWords)
    return finalWords

def getWordList():
    f = open('1.txt', 'r')
    file1 = f.read()
    file1 = file1.lower()
    words = nltk.tokenize.word_tokenize(file1)
    # print(words)
    for i in words:
        if i not in punctuations:
            tempwordlist.append(i)

    return tempwordlist

#print(num)
def getDistance(node1,node2):
    num = editdistance.eval(node1, node2)
    return num

def getKeywordGraph(node1):
    pairs = list(itertools.combinations(node1,2))
    #print(node1)
    G = nx.Graph()
    for i in node1:
        G.add_node(i)

    for j in pairs:
        a = j[0]
        b = j[1]
        dist = getDistance(a,b)
        #print(a,b,dist)
        G.add_edge(a,b, weight = dist)

        #print(G.get_edge_data(a,b))
    #print(G['My']['Akshay']['weight'])
    return G

def getKeywords(filename):

    words = processDoc(filename)

    #g1 = nx.Graph()
    g1 = getKeywordGraph(words)
    page_rank_s = nx.pagerank(g1)
    page_rank_s = sorted(page_rank_s, reverse=True)
    #print(page_rank_s)

    finalKey = set([])
    tempKey = set([])
    total_words = getWordList()

    i =0
    j =1

    while j<len(total_words):
        one = total_words[i]
        two = total_words[j]

        if one in page_rank_s and two in page_rank_s:
            finalKey.add(one + ' ' + two)
            tempKey.add(one)
            tempKey.add(two)

        else:
            if one in page_rank_s and one not in tempKey:
                finalKey.add(one)
                tempKey.add(one)

            if j == len(total_words) - 1 and two in page_rank_s and two not in tempKey:
                finalKey.add(two)

        i = i + 1
        j = j + 1

    print(finalKey)



for root, dirs, files in os.walk('data'):
    for i in range(0, len(files)):
        filename = root + '/' + files[i]
        getKeywords(filename)

