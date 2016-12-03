import os
import re
from collections import Counter
import operator
import editdistance
from nltk.corpus import stopwords

stop = set(stopwords.words('english'))
punctuations = ['!', '"', '#', '$', '%', '&', '\'', ',', '(', ')', '*', '+', ',', '-', '.', '/', ':', ';', '<', '=',
                '>', '?', '@', '[', '\\', ']', '^', '_', '`', '{', '|', '}', '~']


class Node:

    def __init__(self,word,tag):
        self.word = word
        self.score = 0
        self.tag = tag


class Graph:

    def __init__(self):
        self.graph = {}
        self.nodes = {}

    def add_node(self,word,tag):
        if word in self.nodes:
            node = self.nodes[word]
        else:
            node = Node(word,tag)
            self.nodes[word] = node

        return node

    def set_graph(self,words):

        graph = self.graph
        c =0

        for i in words:
            c = c+1
            c_node = self.add_node(i,c)
            for j in range (len(words)):
                n_node = self.add_node(words[j],j+1)
                if c_node == n_node:
                    continue
                if c_node not in graph:
                    graph[c_node] = {}

                    sen1 = str(i)
                    sen2 = str(words[j])
                    graph[c_node][n_node] = self.get_similarity(sen1,sen2)
                else:
                    sen1 = str(i)
                    sen2 = str(words[j])
                    graph[c_node][n_node] = self.get_similarity(sen1,sen2)



    def get_similarity(self,s1,s2):
        num = editdistance.eval(s1, s2)
        return num


    def pageRank(self,max_iter=100):

        for i in range(0,max_iter):

            current_PR = {}

            for k in self.graph:
                if k in current_PR:
                    current_PR[k] = k.score
                else:
                    current_PR[k] = {}
                    current_PR[k] = k.score

            for j in self.graph:
                in_edges = []
                for k in self.graph:
                    for key in self.graph[k]:
                        if key.word == j.word:
                            in_edges.append(key)

                innerScore = 0
                for q in in_edges:
                    weightTot = 0
                    for r in self.graph[q]:
                        # print r.name.encode('utf-8')
                        weightTot += self.graph[q][r]
                    innerScore += (self.graph[q][j] * q.score) / weightTot
                j.score = 0.15 + (0.85 * (innerScore))
                delta = 0
                for key in self.graph:
                    delta += abs(current_PR[key] - key.score)
                if delta <= 0:
                    return

        def sort_nodes(self, num_lines):
            newsent = []
            global sorted_PR, sorted_tag

            sorted_PR = sorted(self.graph.keys(), key=operator.attrgetter('score'), reverse=True)[:num_lines]
            # print(sorted_PR)
            sorted_tag = []
            for i in range(0, len(sorted_PR)):
                # print(str(sorted_PR[i].sentence)+''+str(sorted_PR[i].score))
                sorted_tag.append(sorted_PR[i].word)

            for i in sorted_tag:
                newsent = ' '.join(sorted_tag)

            # print(newsent)
            return newsent

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

def summary_main(filename):
    global data, finalD, count

    finalD, count = processDoc(filename)
        # print(finalD)
    g = Graph()
    g.set_graph(finalD)
    g.pageRank()
    g.sort_nodes(5)

    sumsent = g.sort_nodes(5)
    return sumsent

for root, dirs, files in os.walk('data'):
    for i in range(0, len(files)):
        filename = root + '/' + files[i]
        summary_main(filename)




#summary_main()


