"""
@author: fill in the blank

This file implements the missionaries and cannibals problem using
the problem class specfied for the AIMA python search.py file

It then finds solutions to this problem using 2 different search algorithms:
Depth First and Breadth First
"""

from search import *

class MandC(Problem):
    ''' This is the Missionaries and Cannibals Problem
    it's inherited from the Problem class (see search.py).
    '''



    def __init__(self, initial, goal):

        self.action = [(1,1),(1,0),(0,1),(2,0),(0,2)]
        self.test = [0, 1, 2, 3, 4]

        #call ths parent class's constructor
        Problem.__init__(self,initial,goal)

    def actions(self,state):

        # This method should return a set of legal actions from
        # the current state

        stemp = list(state)
        atemp = [list(x) for x in self.action]

        legal2 = []

        for item in self.test:
            if state[2] == "L":
                legal = atemp[item]
                an = [stemp - atemp[item] for stemp, atemp[item] in zip(stemp, atemp[item])]
                if (0 <= an[0] <= 3) and (0 <= an[1] <= 3) and (
                        an == [3, 2] or an == [3, 1] or an == [3, 0] or an == [2, 2] or an == [1, 1] or an == [0,
                                                                                                               2] or an == [
                            0, 1] or an == [0, 0]):
                    legal2.append(legal)

            if state[2] == "R":
                legal = atemp[item]
                an = [stemp + atemp[item] for stemp, atemp[item] in zip(stemp, atemp[item])]
                if (0 <= an[0] <= 3) and (0 <= an[1] <= 3) and (
                        an == [3, 3] or an == [3, 2] or an == [3, 1] or an == [2, 2] or an == [1, 1] or an == [0,
                                                                                                               3] or an == [
                            0, 2]):
                    legal2.append(legal)

        return legal2

    def result(self, state, action):
        # This method returns the new state after applying action
        # to state

        temp = list(state)

        newstate = []

        if state[2] == "L":

            newstate = [temp - action for temp, action in zip(temp, action)]
            newstate.append("R")
        if state[2] == "R":

            newstate = [temp + action for temp, action in zip(temp, action)]
            newstate.append("L")

        newstate = self.convert(newstate)

        return newstate


    def convert(self, list):
        return tuple(list)

    # are there additional methods you'd like to define to help solve this problem?

#Now you should test this:

def main():

    intial_state = (3,3,"L")
    goal_state = (0,0,"R")
    mc = MandC(intial_state,goal_state)

    soln = depth_first_graph_search(mc)
    print("Depth First Search")
    print("Solution Length: " + str(len(soln.path())))
    print("Nodes Traversed:")
    print(soln.path())
    print("Actions Taken:")
    print(soln.solution())

    soln = breadth_first_search(mc)
    print("Breadth First Search")
    print("Solution Length: " + str(len(soln.path())))
    print("Nodes Traversed:")
    print(soln.path())
    print("Actions Taken:")
    print(soln.solution())

if __name__ == "__main__":
    main()
