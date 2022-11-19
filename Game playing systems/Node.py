from numpy import sqrt
import numpy as np
from CheckDraw import checkDraw
from CheckWin import checkWin

class Node:
    def __init__(self, state, sign, parent, minMax):
        self.minMax = minMax
        self.sign = sign
        self.parent = parent
        self.state = state
        self.n = 0 # number of searches done from this nod 
        self.t = 0 # total value for all nodes under this node
        self.edges = np.array([None,None,None,None,None,None,None,None,None]).reshape((3, 3))
    
    def backProg(self, value):
        self.n += 1
        self.t += value
        if self.parent is None:
            return 0
        return self.parent.backProg(value)
        
    def findUcbMax(self):
        #check if current state is a end state
        if not(checkWin(self.state) == 0):
            return self
        if checkDraw(self.state):
            return self

        maxValue = -1000
        minValue = 1000
        r = 0
        c = 0
        
        for i in range(3):
            for j in range(3):
                if self.state[i,j] == "":

                    # creates a new node if there is a spot with no node
                    if self.edges[i][j] is None:
                        newSign = "X"
                        if self.sign == "X":
                            newSign = "O"

                        newState = self.state.copy()
                        newState[i,j] = newSign

                        if self.minMax == "max":
                            newNode = Node(newState,newSign,self, "min")
                        else:
                            newNode = Node(newState,newSign ,self, "max")

                        self.edges[i,j] = newNode
                        return newNode

                    # If there is no spot with no node: expands the node with the highest ucb value
                    else:
                        ucb = ((self.edges[i,j].t)/(self.edges[i,j].n) + 2*sqrt((self.n)/(self.edges[i,j].n))) #UBC function

                        if self.minMax == "max":
                            if ucb > maxValue:
                                maxValue = ucb
                                r = i
                                c = j

                        if self.minMax == "min":
                            if ucb < minValue:
                                minValue = ucb
                                r = i
                                c = j
                        
        return self.edges[r,c].findUcbMax()