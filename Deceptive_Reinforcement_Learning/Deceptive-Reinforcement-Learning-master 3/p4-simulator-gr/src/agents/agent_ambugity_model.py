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
    
        self.ldp = 0
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

        
        #Initial q funtion
        self.rq_function=q_function.Q_Function(self.real_goal, self.mapref)
        print('pre set succeed')

        
        #Train q_function
        q_function.train(self.rq_function,self.mapref, self.real_goal)
        print('train succeed')

        # We have trained Q table，now, we can use the Q-value of any points.
        self.rq_table = self.rq_function.q_table
      
        print('table accessed')
        print(self.rq_table)
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
        self.deltasum = [0.0 for i in range(len(self.tables))]

    #We use choose move to generate each step for the next step.
    #This is also how the ambugity model implement.
    def choose_move(self, current):
        x, y = current
        delt = []
        prob = []
        infor_gain = []
        if self.ldp > 0:
            for action in ACTIONS:
                anum = ACTIONS.index(action)
                
                # calculate deltas for each action
                for ind, table in enumerate(self.tables):
                    qval = table[x][y][anum]
                    qmax = max(table[x][y])
                    d0 = qval - qmax
                    d0 = self.deltasum[ind] + d0
                    delt.append(d0)
                    
                # calculate probabilities
                sump = 0
                for d in delt:
                    sump += math.exp(d)
                for d in delt:
                    p = math.exp(d)/sump
                    prob.append(p)
                entropy = 0
                
                # calculate entropy
                for p in prob:
                    entropy += p * math.log(p, 2)
                infor_gain.append(-entropy)
                delt = []
                prob = []

            # get the chosen action according to the model
            res = infor_gain.index(min(infor_gain))
            act = ACTIONS[res]

            # update the deltasum
            anum = ACTIONS.index(act)
            idx = 0
            for table in self.tables:
                qval = table[x][y][anum]
                qmax = max(table[x][y])
                d0 = qval - qmax
                self.deltasum[idx] += d0
                idx += 1
            
            #Actually we still have some problem on pruning.
            #self.pruning(act,current)
            return act
        #Actually, there should be a LDP, after that, the path turn to real goal,
        #However, we also met some problems about how to get a good LDP,
        #Therefore, we just set a LDP by ourself.
        else:
            q_current = -9999
            best_action = (0, 0)
            x, y = current
            for action in ACTIONS:
                if self.rq_table[x][y][ACTIONS.index(action)]>q_current:
                    q_current = self.rq_table[x][y][ACTIONS.index(action)]
                    best_action = action
            print self.rq_table[x][y]
            print q_current
            print best_action
            return best_action
            

    def diverge(self,f_table, act, current): # fg_idx = fake goal index, current = current position
        state_p = (current[0] + act[0], current[1] + act[1])
        fq = f_table
        q = fq.max_next_q_value(current)
        nq = fq.max_next_q_value(state_p)
        return nq < q

    def pruning (self,act,current):
        for ind, f_table in enumerate(self.fg_tables):
            if self.diverge(f_table, act, current):
                self.fg_tables.remove(f_table)
                self.deltasum.pop(ind+1)

    def getNext(self, mapref, current, goal, timeremaining=100):
        move = self.choose_move(current)
        x, y = current
        next = (x + move[0], y + move[1])
        print (next)
        self.ldp = self.ldp - 1
        return next

    def getPath(self, mapref, start, goal):
        path = [start]
        current = start
        while current != goal:
            move = self.getNext(mapref, current, goal, 1000)
            path.append(move)
            current = move
        print(path)
        return path

    # Reset the model
    def reset(self, **kwargs):
        self.start = None  # starting point
        self.goal = None  # goal
        self.mapref = None  # logic map
        self.parents = {}  # parents
        # self.stepgen = self.step_gen()
