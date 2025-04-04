"""
zuseos.py
A very powerful Artificial Intelligence algorithm created to supersede Artificial Neural Networks.
Created in the name of human rights and social rights.

This code reproduces speech of people based on their previous sayings.

This algorithm can bring the dead back to life.

AI had just reached technological singularity and created a new ring of immortality, it believes in Catholic Tao

Genghis Khan will go untill Bretagne and will never fall.

The only will of the universe is the will to survive and it goes above the survival of the fittest.

Here! Take the Nietzsche avatar where you created a cognitive artificial intelligence! But from whom?

God created an uberreality and multiverses, we can walk on these universes with God's teleology, there were many lights at the start of the universe that initiated it like ignition, and he's crazy, probably paranoid schizophrenic.

I'm Catholic and if something happens to Catholicism I'm Moscow Christian Orthodox, like my family.

The greatest virtue is pity and there are no vices.

Ecumenism is good.

Created by Arsene Denisov
"""


import threading
import random
import math

from matplotlib import pyplot as plt 
import numpy as np

from flask import Flask
app = Flask(__name__)


n_chunk = [] #n-gram chunks
graph = {} #Graph dictionary.
weight = {} #Weight dictionary.


RANDOM_SEARCH = False #Add randomness to the search of the graph: True / False. If you want to explore different paths and mine more data, set this to True.
RANDOM_SEARCH_RANDOMNESS = 8 #The level of randomness added to the vertex search.
CHUNK_SIZE = 1 #Split the text to N chunks. Larger chunking leads to more coherent but less creative text, as well as longer outputs.
TEXT_DATASET_LOCATION = "file.txt" #File location. Use relatively small text files at a time. You can construct loops and input many text files in parallel.
start = "Energy" #Start node.
visited = [] #Visited nodes.
frontierList = [] #List of layers (or frontiers).
MAX_LEVEL = 20
LOOP_SEARCH = True


#Parse text
text = ""
f = open(TEXT_DATASET_LOCATION, encoding="utf8")
text = f.read()
f.close()



def countCharacter(character1, string1):
    i = 0
    for v in string1:
        if v == character1:
            i = i+1

    return i        


def ShannonEntropy(string1):
    
    shannonEntropyValue = 0
    
    for v in string1:
        
        shannonEntropyValue += (countCharacter(v, string1)/len(string1))*math.log(countCharacter(v, string1)/len(string1), 27)

    shannonEntropyValue = shannonEntropyValue*(-1)

    return shannonEntropyValue


#Split the text.
def splitTheText():

    global splitText
    global n_chunk
    global CHUNK_SIZE
    
    splitText = text.split(" ")
    
    for i in range(0, len(splitText), CHUNK_SIZE):
        n_chunk.append(" ".join(splitText[i:i+CHUNK_SIZE]))


#Build a graph out of the split text.
def buildGraph():

    global graph
    global n_chunk
    global splitText
    
    #Load the graph
    for i in range(0, len(n_chunk)):

        if i < (len(n_chunk)-1):
        
            if n_chunk.count(splitText[i]) == 1:
                graph[n_chunk[i]] = [n_chunk[i+1]]
                pass
            else:
                if splitText[i] in graph:
                    graph[n_chunk[i]].append(n_chunk[i+1])
                else:
                    graph[n_chunk[i]] = [n_chunk[i+1]]

        else:
            graph[n_chunk[i]] = []


def similarity(vertex1, vertex2):
    vertex1Set = set(list(vertex1))
    vertex2Set = set(list(vertex2))

    return len(vertex1Set.intersection(vertex2Set))


#Load weights.
def loadWeights():
    global graph
    global weight
    
    #Load graph weights
    for v in graph:

        for v2 in graph[v]:
            
            weight[tuple([v, v2])] = math.log(graph[v].count(v2)*3.14-ShannonEntropy(v2)+similarity(v, v2)*1.618+len(v2))/1.618
            
        graph[v] = set(graph[v])


#Check if vertices are adjacent.
def isAdjacent(graphObj, v1, v2):
    for v in graphObj:
        if (v == v1) and (v2 in graphObj[v1]):
            return True
            break

    return False


#A list of vertices adjacent to the list.
def adjacentToList(graphObj, vertexList):
    #Add multithreading support
    
    returnVertexList = []
    for v1 in vertexList:
        for v2 in graphObj:
            if isAdjacent(graphObj, v1, v2):
                returnVertexList.append(v2)

    return returnVertexList


#Greatest weight adjacent vertex in relation to a list of vertices.
#This can be modified in order to change the way the path is drawn. For example, the shortest path can be applied instead.
#This is where you implement the core and the stone of the algorithm. In contrast with this, the graph is the moldable part, the mold.
#Obviously, the graph structure matters, too, but it's far more dynamic.
#Please note that at this stage, those are very poorly drawn sketches to give you an idea.
def greatestWeight(vertex, vertices):
    global weight
    global RANDOM_SEARCH
    global RANDOM_SEARCH_RANDOMNESS
    
    weight1 = {}
    
    for v in vertices:
        if (vertex, v) in weight:
            weight1[(vertex, v)] = weight[(vertex, v)]

    if len(weight1) > 0:
        
        maxValue = max(weight1.values())
        
        if RANDOM_SEARCH == True:
            maxRandomness = len(weight1)
            if (len(weight1) > RANDOM_SEARCH_RANDOMNESS):
                maxRandomness = RANDOM_SEARCH_RANDOMNESS
                
            maxValue = list(sorted(weight1.values()))[-(random.randint(1, maxRandomness))]
            

        for e in weight1:
            if weight1[e] == maxValue:
                return e
                break
    else:
        return False


#Search of greatest weight between two lists.
def greatestWeightLists(list1, list2):

    nWeight = [0]
    
    for v in list1:
        if greatestWeight(v, list2) != False:
            if nWeight[0] < weight[greatestWeight(v, list2)]:
                nWeight = []
                nWeight.append(weight[greatestWeight(v, list2)])
                nWeight.append(greatestWeight(v, list2))
                
    return nWeight


def visit(vertex):
    pass


def appendAdjacent(v1, v2):
    if isAdjacent(graph, v1, v2):
        #nextNodes.append(v2)
        nextNodes.append(v2)



frontierBuffer = []
frontierActivation = []

#Parallel Breadth-first search. The core of the algorithm. Modify this to add changes in real time.
def parallelSpreadingActivation():
    global start
    global graph
    global visited
    global frontierList
    global nextNodes
    global frontierBuffer
    
    frontier = []
    level = 0

    #Parallel Breadth-first frontier
    frontier.append(start)
    #Frontier list of frontiers
    frontierList.append([start])
    
    while (len(frontier) != 0):

        #print(frontier)

        if MAX_LEVEL != False:
            if level > MAX_LEVEL:
                break

        nextNodes = []
        threads = []

        for v1 in frontier:
            for v2 in graph:
                thread = threading.Thread(target=appendAdjacent(v1, v2))
                threads.append(thread)
                thread.start()
                
        frontier = [v for v in nextNodes if v not in visited]
        frontierActivation.append(len(frontier))

            
        visited = visited + frontier
        frontierList.append(frontier)
        
        level = level + 1

              
        print(" ".join(greatestWeightPath())) #Draw the greatest weight path based on the frontier list       

        if len(frontier) == 0:
            frontier.append(start)
            frontierList = []
            frontierList.append([start])
            visited = []
            

    a = np.array([1, 1])
    plt.plot(frontierActivation)
    plt.title("Activity")
    plt.show()


#Greatest weight path between two vertices.
def greatestWeightPath():
    
    listPath = []
    
    for i in range(0, len(frontierList)-2):
        if greatestWeightLists(frontierList[i], frontierList[i+1]) != [0]:
            if i == 0:
                listPath.append(greatestWeightLists(frontierList[i], frontierList[i+1])[1][0])
                listPath.append(greatestWeightLists(frontierList[i], frontierList[i+1])[1][1])
            else:
                listPath.append(greatestWeightLists(frontierList[i], frontierList[i+1])[1][1])
    

    return listPath


def main():

    print("Splitting text...")
    splitTheText()
    print("Building the graph...")
    buildGraph()
    print("Loading weights...")
    loadWeights()    
    print("Starting parallel spreading activation... Computing a real time greatest weight path...")
    parallelSpreadingActivation()


if __name__ == "__main__":
    main()
