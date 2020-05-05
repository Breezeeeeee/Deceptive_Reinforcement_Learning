# coding=utf-8
from heapq import heappush, heappop, heapify
from time import time
#encoding = utf-8

import Q_Function_02_Multi as q_function
import math
import random

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

        dprob = self.get_dprob()
        self.decept = self.get_decept(dprob)
        print(self.decept[:5])
        self.dec_location = []
        for ele in self.decept:
            self.dec_location.append(ele[0])
        self.sorted_dec = self.get_sorted_decept(self.decept)
        print(self.sorted_dec[:5])


        dist = []
        for p, prob in self.decept:
            d = math.sqrt((self.start_position[0] - p[0]) ** 2 + (self.start_position[1] - p[1]) ** 2)
            dist.append((d, p, prob))
        sorted_l = sorted(dist, key=lambda t: t[0])
        print('sorted_dec_start:')
        print(sorted_l[:10])

        self.path = self.astar()
        print(self.path)





        self.goals_dict = {}
        self.goals_dict[self.real_goal] = 1000
        # for fg in self.fake_goals:
        #     self.goals_dict[fg] = 200
        self.goals_dict[self.fake_goals[0]] = 240
        self.goals_dict[self.fake_goals[1]] = 240
        # self.goals_dict[self.fake_goals[2]] = 180
        self.qfunction = q_function.Q_Function(self.goals_dict, self.mapref,self.start_position)
        print(self.goals_dict)
        q_function.train(self.qfunction, self.mapref, self.goals_dict,self.dec_location)
        print('train succeed')

        self.last_move = (0,0)
        self.epi = 0



    #We use choose move to generate each step for the next step.
    #This is also how the ambugity model implement.
    def choose_move(self, current):
        # print('choose move')
        # print('length path:',len(self.path))
        # if len(self.path)==0 or len(self.path[0])==1:

        x, y = current
        q_current = -999999
        best_action = (0, 0)
        for act_idx, action in enumerate(ACTIONS):
            if self.qfunction.q_table[x][y][act_idx] > q_current and action!=(-self.last_move[0],-self.last_move[1]):
                q_current = self.qfunction.q_table[x][y][act_idx]
                best_action = action
        self.last_move = (-best_action[0],-best_action[1])
        print('Q-value:',q_current)

        return best_action
        # elif len(self.path[0])>1:
        #     print('astar')
        #     nstage = self.path[0].pop(1)
        #     best_action = ((nstage[0]-current[0]),(nstage[1]-current[1]))
        #     return best_action


    def get_dprob(self):
        h = self.mapref.height
        w = self.mapref.width
        dprob = [[[0,0,0] for i in range(h)] for wid in range(w)]
        fg_list = self.fake_goals
        rg = self.real_goal
        optc_f = []
        optc_r = math.sqrt((rg[0] - self.start_position[0])**2 + (rg[1]-self.start_position[1])**2)
        for fg in fg_list:
            optc_f.append(math.sqrt((fg[0] - self.start_position[0])**2 + (fg[1]-self.start_position[1])**2))
        for wid in range(w):
            for i in range(h):
                optc_nr = math.sqrt((rg[0] - wid)**2 + (rg[1]-i)**2)
                optc_nf = []
                for fg in fg_list:
                    optc_nf.append(math.sqrt((fg[0] - wid)**2 + (fg[1]-i)**2))
                costdif_r = (optc_r - optc_nr)/5
                costdif_f = []
                sumcost_f = 0
                for idx,fg in enumerate(fg_list):
                    costdif_f.append(optc_f[idx] - optc_nf[idx])
                    sumcost_f += math.exp((optc_f[idx] - optc_nf[idx])/5)

                sumcost = math.exp(costdif_r) + math.exp(sumcost_f)
                prob_r = math.exp(costdif_r)/sumcost
                prob_f = []
                for idx, fg in enumerate(fg_list):
                    prob_f.append(math.exp(costdif_f[idx])/sumcost)
                dprob[wid][i][0] = prob_r
                dprob[wid][i][1] = prob_f[0]
                dprob[wid][i][2] = prob_f[1]

        # print(dprob[25][5])
        # print(dprob[25][6])
        # print(dprob[25][4])
        # print(dprob[10][5])
        # print(dprob[15][4])
        # print(dprob[24][5])
        # print(dprob[26][5])
        return dprob

    def get_decept(self,dprob):
        ans = []
        for wid in range(len(dprob)):
            for i in range(len(dprob[0])):
                check_dec = False
                for idx,proba in enumerate(dprob[wid][i]):
                    if idx!=0 and dprob[wid][i][0] <= proba:
                        check_dec = True
                if check_dec:
                    ans.append(((wid,i),dprob[wid][i][0]))
        return ans

    def get_sorted_decept(self,decept):
        dist = []
        rg = self.real_goal
        for p,prob in decept:
            d = math.sqrt((rg[0] - p[0])**2 + (rg[1]-p[1])**2)
            dist.append((d,p,prob))
        sorted_l = sorted(dist, key=lambda t: t[0])
        return sorted_l

    def get_suc(self,current):
        x = current[0]
        y = current[1]
        ans = []
        for idx,action in enumerate(ACTIONS):
            nstage = (x+action[0],y+action[1])
            if self.mapref.isPassable(nstage, current) and (nstage in self.dec_location):
                ans.append((nstage,self.mapref.getCost(nstage, previous = current)))
        return ans

    def heuristic(self,a,b):
        h = math.sqrt((b[0] - a[0]) ** 2 + (b[1] - a[1]) ** 2)
        return h

    def astar(self):
        start = self.start_position

        for p in self.sorted_dec:
            suc = self.get_suc(start)
            open = []
            p = p[1]
            # print('p:',p)
            # print('start:',start)
            open.append((start, 0,[start],(0+self.heuristic(start,p)))) #open.append( (location,distance,path,mark) )
            closed = []
            if len(suc) == 0:
                print('None successors.')
                return []
            else:
                while len(open)!=0:
                    open = sorted(open, key=lambda t: t[3])
                    cur_node = open.pop(0)
                    cur_location, distance, path, mark = cur_node
                    if cur_location == p:
                        return [path,p]
                    mark = distance + self.heuristic(cur_location,p)
                    check_visited = False
                    for (location1, mark1) in closed:
                        if (cur_location == location1) and (mark >= mark1):
                            check_visited = True
                    if not check_visited:
                        closed.append((cur_location, mark))
                        suc = self.get_suc(cur_location)
                        for location, cost in suc:
                            open.append((location, distance+cost, path+[location], distance + cost + self.heuristic(location, p)))
        print('None')
        return []

    def getNext(self, mapref, current, goal, timeremaining=100):
        # print('getnext')
        move = self.choose_move(current)
        x, y = current
        next = (x + move[0], y + move[1])
        print (next)
        return next


    # def getPath(self, mapref, start, goal):
    #     path = [start]
    #     current = start
    #     while current != goal:
    #         move = self.getNext(mapref, current, goal, 1000)
    #         path.append(move)
    #         current = move
    #     print(path)
    #     return path

    # Reset the model
    def reset(self, **kwargs):
        self.start = None  # starting point
        self.goal = None  # goal
        self.mapref = None  # logic map
        self.parents = {}  # parents
        # self.stepgen = self.step_gen()
