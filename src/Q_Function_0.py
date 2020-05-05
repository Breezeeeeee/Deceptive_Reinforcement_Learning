# coding=utf-8
ACTIONS = [(-1, -1), (0, -1), (1, -1), (1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0)]

class Q_Function():
    def __init__(self, goal, mapref):
       
        self.goal = goal
        self.mapref = mapref
        print('height',mapref.height)
        print('width',mapref.width)

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


    def update_q_value(self, discount, learning_rate, goal): #added goal as a parameter
        
        history_q_table = self.deepcopy_q_table()

        #Updating Q-value for every point.
        for x in range(len(self.q_table)):
            for y in range(len(self.q_table[0])):
                current_state = (x, y)

                #If this is a goal, stop traing this point.
                if current_state == goal:
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
                    if new_state == goal:
                        reward = 10000 - cost
                    else:
                        reward =  - cost
                    if cost < float('inf'):
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
def train(q_function, mapref, goal,  discount = 0.9, learning_rate = 0.9):
    episode = 0 #added
    while True:
        if q_function.update_q_value(discount,learning_rate,goal): #added a goal as a parameter
            print(episode)
            break
        episode += 1
        
        #restrict training times
        if episode > 1000:
            break
            
    print episode, 'times have been trained.\n'
    
