__author__ = 'avik'

import sys
import operator
import heapq

class Stack:
    def __init__(self):
        self.list = []

    def isEmpty(self):
        return len(self.list) == 0

    def push(self,item):
        self.list.append(item)

    def pop(self):
        return self.list.pop()

    def sort(self):
        sorted(self.list)


class Queue:
    def __init__(self):
        self.list = []

    def isEmpty(self):
        return len(self.list) == 0

    def enqueue(self,item):
        self.list.insert(0,item)

    def dequeue(self):
        return self.list.pop()


class PriorityQueue:
    def  __init__(self):
        self.list = []

    def push(self, item, priority):
        entry = (priority, item)
        heapq.heappush(self.list, entry)

    def pop(self):
        (_,item) = heapq.heappop(self.list)
        return item

    def display(self):
        print self.list

    def isEmpty(self):
        return len(self.list) == 0

    def removeItem(self,item):
        size = len(self.list)
        found = False
        for index in range(0,size):
            if item == self.list[index][1][0]:
                discarded = self.list[index]
                found = True
                break
        if found == True:
            self.list.remove(discarded )

    def getTotalCost(self,item):
        size = len(self.list)
        found = False
        for index in range(0,size):
            #print "index:",index,item
            if item == self.list[index][1][0]:
                cost,x = self.list[index]
                found = True
                break
        if found == True:
            return cost


def getStartNode(graph,sourceNode):
    return sourceNode


def removeDuplicates(list):

    newList = []
    for item in list:
        if item not in newList:
            newList.append(item)

    newList = sorted(newList)

    return newList


def isGoalNode(graph,destinationNodes,node):

    for goalNode in destinationNodes:
        if node == goalNode:
            return True

    return False


def getSuccessors(graph,node):
    return graph[node]


def printOutput(goal,time):

    with open('output.txt','a+') as outputFile:
        if goal == 'None':
            outputFile.write(goal + '\n')
            return
        outputFile.write(goal+' '+str(time) + '\n')


def ParseGraphLine(graph,offPeriod,line):

    graphLine = line.strip().split(' ')
    graph[graphLine[0]][graphLine[1]] = graphLine[2]
    offPeriod[graphLine[0]][graphLine[1]] = []
    offPeriodCount = graphLine[3]
    temp = []

    for index in range(4,4+int(offPeriodCount)):
        start,stop = graphLine[index].split('-')
        temp.append(range(int(start),int(stop)+1))

    if len(temp)!=0:
        temp = reduce(operator.add,temp)
        temp = removeDuplicates(temp)
        offPeriod[graphLine[0]][graphLine[1]] = temp

    return


def ReturnCost(graph,source,destination):
    return int(graph[source][destination])


def ParseInputFile(graph,offPeriod):

    count = 0

    with open(sys.argv[2],'r+') as inputFile:
        testCaseCount = inputFile.readline()

        while count < int(testCaseCount):
            count += 1

            line = inputFile.next()
            task = line.strip()

            line = inputFile.next()
            sourceNode = line.strip()
            graph[sourceNode] = {}
            offPeriod[sourceNode] = {}

            line = inputFile.next()
            destinationNodes = line.strip().split(' ')
            for nodes in destinationNodes:
                graph[nodes] = {}
                offPeriod[nodes] = {}

            line = inputFile.next()    #This can be empty which means no middle nodes
            middleNodes = line.strip().split(' ')
            for nodes in middleNodes:
                graph[nodes] = {}
                offPeriod[nodes] = {}

            line = inputFile.next()
            pipeCount = int(line.strip())
            i = 0
            while i < pipeCount:
                i+=1
                line = inputFile.next()
                ParseGraphLine(graph,offPeriod,line)

            line = inputFile.next()
            startTime = int(line.strip())

            if count < int(testCaseCount):
                line = inputFile.next()

            if task == 'DFS':
                goal,time = depthFirstSearch(graph,sourceNode,destinationNodes,startTime)

            elif task == 'BFS':
                goal,time = breadthFirstSearch(graph,sourceNode,destinationNodes,startTime)

            else:
                goal,time = uniformCostSearch(graph,offPeriod,sourceNode,destinationNodes,startTime)

            graph.clear()
            offPeriod.clear()

            printOutput(goal,time)

    return


def depthFirstSearch(graph,sourceNode,destinationNodes,startTime):

    frontier = Stack()
    frontier.push( (sourceNode,startTime,[]) )

    while frontier.isEmpty() == False:

        node,time,visited = frontier.pop()

        if isGoalNode(graph,destinationNodes,node):
            finalTime = time % 24
            return node,finalTime

        for nextNode in sorted(getSuccessors(graph,node),reverse=True):
            #print "nextNode:",nextNode
            if not nextNode in visited:
                frontier.push( (nextNode,time+1,visited + [node]) )

    return 'None',''


def breadthFirstSearch(graph,sourceNode,destinationNodes,startTime):

    frontier = Queue()
    frontier.enqueue( (sourceNode,startTime,[]) )

    while frontier.isEmpty() == False:
        node,time,visited = frontier.dequeue()

        for nextNode in sorted(getSuccessors(graph,node)):
            if not nextNode in visited:
                if isGoalNode(graph,destinationNodes,nextNode):
                    finalTime = (time+1) % 24
                    return nextNode,finalTime
                frontier.enqueue( (nextNode,time+1,visited + [node]) )

    return 'None',''


def uniformCostSearch(graph,offPeriod,sourceNode,destinationNodes,startTime):

    frontier = PriorityQueue()
    frontier.push((sourceNode,'',startTime),startTime)
    frontierList = [sourceNode]
    visited = []
    count = 0

    while frontier.isEmpty() == False:

        count += 1

        if count == 1:
            node,par,time = frontier.pop()
            frontierList.remove(node)

        else:
            node,par,time = frontier.pop()
            frontierList.remove(node)

        if isGoalNode(graph,destinationNodes,node):
            finalTime = time % 24
            return node,finalTime

        visited.append(node)

        for nextNode in sorted(getSuccessors(graph,node)):
            newTime = time + ReturnCost(graph,node,nextNode)

            hours = time % 24
            if hours in offPeriod[node][nextNode]:
                continue

            if not nextNode in visited and not nextNode in frontierList:
                frontier.push( (nextNode,node,newTime),newTime )
                frontierList.append(nextNode)

            elif nextNode in frontierList:
                if newTime < frontier.getTotalCost(nextNode):
                    frontier.removeItem(nextNode)
                    frontier.push( (nextNode,node,newTime),newTime )


    return 'None',''


def main():

    graph = {}
    offPeriod = {}
    ParseInputFile(graph,offPeriod)


if __name__ == '__main__':
    main()




