from heapq import heappush, heappop, heapify
from time import time
#encoding = utf-8

import Q_Function_0 as q_function

ACTIONS = [(-1, -1), (0, -1), (1, -1), (1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0)]

INF = float('inf')
X_POS = 0
Y_POS = 1


class Agent(object):
    """Weighted A* using Pohl's original definition - when weight = 1, algorithm returns greedy; when weight = 0, algorithm = Dijkstra"""

    def __init__(self, goal, mapref, start):

        #在init中就先train好q table
        #现在我不清楚这里agent初始化的时候是怎么获取我们需要的变量的
        self.goal =  goal
        self.mapref = mapref
        self.start = start



        #初始化q funtion
        self.q_function=q_function.Q_Function(goal, mapref)

        #训练q_function直到其中的q值不再更新，此时训练完成
        q_function.train(self.q_function, mapref, goal)

        #现在可以拉取训练好的Q table，至此我们就可以随意获得我们的Q值了
        self.q_table = self.q_function.q_table()



    def getPath(self, model, start, goal):
        self.reset()
        return self.q_learning_path(model, start, goal)

    def getCost(self, model, start, goal):
        self.reset()
        return self.q_learning_path(model, start, goal, True)

    #flag用来确定是返回路径和路径cost还是只返回cost
    def q_learning_path(self, mapref, start, goal, flag=False):
        #在这里实现我们的model，我先举个例子根据Q table找最优路径
        path = []
        cost = 0
        #从出发点出发，只要current state跟goal不一样，就要继续找下去
        current_state = self.start
        while current_state != self.goal:
            max_q_value = -9999
            best_action = None

            #在每个位置选最大的q值作为下一步
            for action in ACTIONS:
                if self.q_function.q_value(state,action)>max_q_value:
                    best_action = action

            #记录路径和cost
            path.append(best_action)
            cost += self.mapref.getCost(current_state + best_action, previous = current_state)

            #不确定这里是否能直接加哈哈哈，反正那意思你们懂得，move到下一个状态
            current_state = current_state + best_action

        #最后返回路径和cost
        return path, cost

    #举个例子完成我们的作业试试
    def ambiguity_model(self):
        #明天再举吧。。。我举不动了





    #不确定getNext是否必须，看所有的项目里都有，但个人感觉这里用不到
    def getNext(self, mapref, current, goal, timeremaining):
        self.start = current
        self.goal = goal
        self.mapref = mapref
        return next(self.stepgen)
    # reset应该是必须的，但比较简单实现，就重置一下，之后搞
    def reset(self, **kwargs):
        self.start = None  # starting point
        self.goal = None  # goal
        self.mapref = None  # logic map
        self.parents = {}  # parents
        self.stepgen = self.step_gen()














