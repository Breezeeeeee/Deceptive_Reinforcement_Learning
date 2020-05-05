# coding=utf-8
ACTIONS = [(-1, -1), (0, -1), (1, -1), (1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0)]
import math
import copy

class Q_Function():
    def __init__(self, goal, mapref, start ):
       
        self.goal = goal
        self.real_goal = (0, 0)
        self.fake_goals = []
        for g in self.goal.keys():
            if self.goal[g] == 1000:
                self.real_goal = g
            else:
                self.fake_goals.append(g)
        self.mapref = mapref
        self.goal_total = [self.real_goal] + self.fake_goals
        print('height',mapref.height)
        print('width',mapref.width)
        print('rq:',self.real_goal)
        print('fgs,',self.fake_goals)
        print('start:',start)
        self.bound_reward = [1000 for i in range(len(self.goal_total))]
        self.radius = self.get_radius(start,self.real_goal,self.fake_goals)
        #generate a Q table according to width*length*action,the initial Q is 0.0.
        self.q_table = [[[0.0 for action in range(len(ACTIONS))]
                   for row in range(mapref.height)]
                  for col in range(mapref.width)]

    #Return q_value in one point
    def q_value(self, state, action):
        x, y = state
        action_number = ACTIONS.index(action) #revised
     
        return self.q_table[x][y][action_number] #revised


    #Return max Q(s',a')
    def max_next_q_value(self, state):
        x, y = state
        return max(self.q_table[x][y])

    def get_dist(self,a,b):
        dist = math.sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2)
        return dist

    def get_radius(self,start,rg,fgs):
        g0 = [rg] + fgs
        print('g0:',g0)
        radius = []
        for goal in g0:
            g1 = copy.deepcopy(g0)
            print('g1',g1)
            temp = []
            g1.remove(goal)
            for r in g1:
                a = self.get_dist(start, goal)
                b = self.get_dist(start, r)
                c = self.get_dist(goal, r)
                beta = (c + a - b) / 2
                temp.append(beta)
            radius.append(round(min(temp)))
        return radius



    def update_q_value(self, discount, learning_rate, goals,decpt_map, dprob,entro_reward): #added goal as a parameter
        history_q_table = self.deepcopy_q_table()

        #Updating Q-value for every point.
        for x in range(len(self.q_table)):
            for y in range(len(self.q_table[0])):
                current_state = (x, y)

                #If this is a goal, stop traing this point.
                if current_state in goals.keys():
                    continue

                #Updating for every Q(s,a)
                for action in ACTIONS:

                    #Record the old Q and move to the next step
                    action_number = ACTIONS.index(action)
                    # print('action num:', action_number)
                    q_history = self.q_table[x][y][action_number]

                    new_state = (x + action[0], y + action[1])
                    cost = self.mapref.getCost(new_state, previous = current_state)

                    #It is a easy reward function, if get goal, then reward 10000,
                    #but - cost for all steps

                    # for idx,g in enumerate(self.goal_total):
                    #     d = self.get_dist(g,new_state)
                    #     if round(d) in self.radius:
                    #         reward = self.bound_reward[idx]
                    #         self.bound_reward[idx] = -2*cost
                    #
                    #         break
                    #
                    #     elif d<self.radius[idx] and idx!=0:
                    #         reward = -300
                    #         break
                    #     elif d < self.radius[idx] and idx == 0:
                    #         reward = 10
                    #         break


                    # else:
                    #     reward =  -cost
                    if cost < float('inf'):
                        reward = -cost  # revised
                        if new_state in decpt_map:
                            x = new_state[0]
                            y = new_state[1]
                            reward = entro_reward[x][y]
                        if new_state in goals.keys():
                            reward = goals[new_state] - cost
                        #Q Value formula
                        q_new_value = q_history + \
                                      learning_rate *\
                                      (reward + discount * self.max_next_q_value(new_state) - q_history)
                        self.q_table[x][y][action_number] = q_new_value #added to update the q_new_history_q_table
        #if updating is finished, return true
        return self.q_table == history_q_table


    

    def deepcopy_q_table(self):
        new_q_table = [[[self.q_table[col][row][action] for action in range(len(ACTIONS))]
                    for row in range(self.mapref.height)]
                   for col in range(self.mapref.width)]
        return new_q_table

    #Print the total Q table
    def print_q_table(self):
        out = ""
        for y in range(self.mapref.height):
            for x in range(self.mapref.width):
                v = max(self.q_table[x][y])
                out += "{:5.0f} ".format(v)
            out += "\n"
        print out



#Traing Q Table
def train(q_function, mapref, goals,  decpt_map,dprob, entro_reward,discount = 0.9, learning_rate = 0.9):
    episode = 0 #added
    while True:
        if episode % 100 == 0:
            print(episode)
        if q_function.update_q_value(discount,learning_rate,goals,decpt_map, dprob,entro_reward): #added a goal as a parameter
            print(episode)
            break
        episode += 1

        #restrict training times
        if episode > 100:
            break
            
    print episode, 'times have been trained.\n'
    
