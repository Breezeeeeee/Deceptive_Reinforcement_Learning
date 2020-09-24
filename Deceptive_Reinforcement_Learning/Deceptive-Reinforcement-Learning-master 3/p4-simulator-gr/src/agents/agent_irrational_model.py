# coding=utf-8
from heapq import heappush, heappop, heapify
from time import time
#encoding = utf-8

import Q_Function_0 as q_function
import math

ACTIONS = [(-1, -1), (0, -1), (1, -1), (1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0)]

INF = float('inf')
X_POS = 0
Y_POS = 1


class Agent(object):
    """Weighted A* using Pohl's original definition - when weight = 1, algorithm returns greedy; when weight = 0, algorithm = Dijkstra"""

    def __init__(self, **kwargs):
        if 'fake_goals' in kwargs:
            self.fake_goals = kwargs['fake_goals']
            print('Fake goal set...', self.fake_goals)

        if 'real_goal' in kwargs:
            self.real_goal = kwargs['real_goal']
            print('real goal set...', self.real_goal)

        if 'start_position' in kwargs:
            self.start_position = kwargs['start_position']
            print('start_position set...', self.start_position)

        if 'mapref' in kwargs:
            self.mapref = kwargs['mapref']
            print('mapref set...', self.mapref)



        #initial Q function
        self.rq_function=q_function.Q_Function(self.real_goal, self.mapref)
        print('pre set succeed')

        #
        #train q_table until the table stops changing
        q_function.train(self.rq_function,self.mapref, self.real_goal)
        print('train succeed')

        # get the trained q_table for real goal
        self.old = []
        self.rq_table = self.rq_function.q_table
        # print(self.q_table[10][10])
        # print(self.q_table[20][10])
        # print(self.q_table[30][10])
        # print(self.q_table[35][10])
        # print(self.q_table[40][10])
        # print(self.q_table[45][10])
        print('table accessed')

        # get fake_goals tables
        self.fg_tables = []
        for fg in self.fake_goals:
            fq_function = q_function.Q_Function(fg, self.mapref)
            q_function.train(fq_function, self.mapref, fg)
            fq_table = fq_function.q_table
            self.fg_tables.append(fq_table)
            print('fake table accessed')
        print('fake tables accessed')
        # overall qtable including real and fake tables. (real table index at the first position)
        self.tables = []
        self.tables.append(self.rq_table)
        self.tables += self.fg_tables

        # store the sum delta from previous steps
        self.deltasum = [0.0]*len(self.fg_tables)
        self.old = []
    #irrational model algorithm that returns the next step
    def choose_move(self, current):
        print("hello")
        #alpha is the weight factor to define the importance of the Q-value versus the irrationality.
        alpha = 0.6
        x, y = current
        #initial icrement of delta r for each bogus reward
        delt = []
        #initial weight sum for each action
        wSum = []
        print("hello2")

        #calculating weighted sum for each action
        for action in ACTIONS:
            anum = ACTIONS.index(action)
            for ind, table in enumerate(self.fg_tables):
                qval = table[x][y][anum]
                qmax = max(table[x][y])
                d0 = qval / qmax
                #delta r for each action
                d0 = self.deltasum[ind] + d0
                delt.append(d0)
            #print("hello5")
            im =  1 - max(delt)
            print(im)
            opQ = max(self.rq_table[x][y])

            #weighted sum for each action
            next = (x + action[0], y + action[1])
            print(next)
            print(self.mapref.getCost(next,previous = current))
            #if next in self.old:
            if self.mapref.getCost(next,previous = current) == float('inf'):
                print("no!!!!!!!")
                wSum.append(float('-inf'))
            else:
                wSum.append( (1 - alpha) * self.rq_table[x][y][anum]/opQ + alpha * im)

            delt = []
        # get the chosen action that gives largest weighted sum
        res = wSum.index(max(wSum))
        act = ACTIONS[res]
        # update the deltasum by chosen action
        anum = ACTIONS.index(act)
        idx = 0
        for table in self.fg_tables:
            qval = table[x][y][anum]
            qmax = max(table[x][y])
            d0 = qval/qmax
            self.deltasum[idx] += d0
            idx += 1

        print(act)
        self.old.append((x + act[0], y + act[1]))
        return act

    #get the next step by choose_move
    def getNext(self, mapref, current, goal, timeremaining=100):
        move = self.choose_move(current)
        x, y = current
        next = (x + move[0], y + move[1])
        print (next)
        return next

    def reset(self, **kwargs):
        self.start = None  # starting point
        self.goal = None  # goal
        #self.mapref = None  # logic map
        self.parents = {}  # parents
        # self.stepgen = self.step_gen()
