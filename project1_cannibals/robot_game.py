#Seungjae Jason Lee
#COSC 76
#Project 1

import random

class RobotProblem:
    def __init__(self, dimension):
        #creates robot problem of given size
        self.dimension = dimension
        self.board_state = self.create_board(dimension, 0.4)
        self.start_state, self.goal_state = self.create_robots_and_goal()

    def create_board(self, dimension, wall_prob):
        #creates walls in the board using random probability.
        board = []
        for i in range(dimension):
            list = []
            for j in range(dimension):
                if random.random() < wall_prob:
                    list.append('x')
                else:
                    list.append('o')
            board.append(tuple(list))
        return tuple(board)

    def create_robots_and_goal(self):
        #randomly assigns start and final state with created board
        start_state = None
        final_state = None
        while(True):
            index1 = random.randint(0,self.dimension-1)
            index2 = random.randint(0,self.dimension-1)
            if self.board_state[index1][index2] != 'x':
                if start_state == None:
                    start_state = (index1,index2)
                elif final_state == None:
                    final_state = (index1, index2)

            if start_state != None and final_state != None:
                break
        return start_state, final_state

    def get_successors(self, state):
        #returns successors of given state
        successor_states = []
        for i in range(4):
            if i == 0 and state[1] != self.dimension-1 and self.board_state[state[0]][state[1]+1] != 'x':
                #move right
                new_state = (state[0], state[1]+1)
            elif i == 1 and state[1] != 0 and self.board_state[state[0]][state[1]-1] != 'x':
                #move left
                new_state = (state[0], state[1]-1)
            elif i == 2 and state[0] != self.dimension-1 and self.board_state[state[0]+1][state[1]] != 'x':
                #move down
                new_state = (state[0]+1, state[1])
            elif i == 3 and state[0] != 0 and self.board_state[state[0]-1][state[1]] != 'x':
                #move up
                new_state = (state[0]-1, state[1])
            else:
                #failed to make a new node
                continue
            successor_states.append(new_state)
        return successor_states

    #checks if goal is reached
    def goal_test(self,test_state):
        return test_state == self.goal_state

    #returns the board(2D list)
    def get_board(self):
        return self.board_state

    #prints static information of the problem
    def print_game_state(self):
        for i in range(len(self.board_state)):
            print(self.board_state[i])
        print("robot start: ",self.start_state)
        print("goal state: ",self.goal_state)

    def __str__(self):
        string =  "Robot Problem: " + str(self.start_state)
        return string


## A bit of test code

if __name__ == "__main__":
    test = RobotProblem(6)
    print(test.get_successors((4,4)))
