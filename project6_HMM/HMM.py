#Seungjae Jason Lee
#COSC 76 Project 6: hmm
#02/24/2019
from Maze import Maze
from time import sleep
import numpy as np
import random
import copy
class HMM:
    #initalize HMM model for mazeworld problem
    def __init__(self, maze, move_sequence, sensor_sequence):
        self.maze = maze
        self.index_to_loc_dict = {}
        self.loc_to_index_dict = {}
        self.start_state = self.build_start_state()
        self.index_to_color = {
            0:"g",
            1:"r",
            2:"y",
            3:"b"
        }
        self.color_to_index = {
            "g":0,
            "r":1,
            "y":2,
            "b":3
        }
        self.sensor_sequence = sensor_sequence
        self.move_sequence = move_sequence #sequence of moves
        self.transition = [] #transition matrix
        self.forward = [] #result of filtering
        self.backward = [] #backward
        self.smoothing = [] #result of combining forward and backward
        self.observation = [] #probability distribution for color sensors

        #calling helper methods to finish building matrices
        self.build_transition_matrix()
        self.build_observation()

    def build_observation(self):
        #helper method that builds observation matrices
        self.observation = []
        for i in range(4):
            observation = copy.copy(self.start_state)
            sensor_color = self.index_to_color[i]
            for location in self.loc_to_index_dict.keys():
                color = self.maze.get_color(location[0],location[1])
                if sensor_color == color:
                    observation[self.loc_to_index_dict[location]] = 0.88
                else:
                    observation[self.loc_to_index_dict[location]] = 0.04
            self.observation.append(observation)
        self.observation = np.array(self.observation).transpose()

    def build_start_state(self):
        #builds start state and defines variables in a state
        count = 0
        start_state = []
        for i in range(self.maze.width):
            for j in range(self.maze.height):
                if self.maze.is_floor(i,j):
                    self.index_to_loc_dict[count] = (i,j)
                    self.loc_to_index_dict[(i,j)] = count
                    start_state.append(None)
                    count += 1

        for i in range(len(start_state)):
            start_state[i] = 1/len(start_state)

        return start_state

    def build_transition_matrix(self):
        #builds transition matrix based on observing neighbors of each floor location
        pred_matrix = np.zeros((len(self.start_state),len(self.start_state)))
        for location in self.loc_to_index_dict.keys():
            count = 0
            for direction in range(4):
                dx = 0
                dy = 0
                if direction == 0:
                    dx = 1
                elif direction == 1:
                    dx = -1
                elif direction == 2:
                    dy = -1
                else:
                    dy = 1

                if self.maze.is_floor(location[0]+dx, location[1]+dy):
                    pred_matrix[self.loc_to_index_dict[location],self.loc_to_index_dict[(location[0]+dx,location[1]+dy)]] = 0.25
                else:
                    count += 1
            pred_matrix[self.loc_to_index_dict[location],self.loc_to_index_dict[location]] = count*0.25
        self.transition = pred_matrix

    def filtering(self):
        #filtering algorithm, main task of the project
        state = np.array([self.start_state]).transpose()
        self.forward.append(state)
        sensor_sequence = copy.copy(self.sensor_sequence)
        for direction in self.move_sequence:
            #running for each time step
            sensor_color = sensor_sequence.pop(0) #user given color input
            obs_matrix = np.diag(self.observation[:,self.color_to_index[sensor_color]])
            state = obs_matrix.dot(self.transition.transpose().dot(state)) # probability distribution calculation using matrix multiplication
            alpha = np.sum(state)
            state = (1/alpha)*state #normalize
            self.forward.append(state) #save
        return state


    def viterbi(self):
        #extension: find the optimal path using viterbi
        best_path = [] #keeps track of best path for each time step
        distribution = [] #keeps the score of each best path during each time step
        distribution.append(self.start_state)
        best_path.append(list(range(len(self.start_state))))
        for i in range(len(self.sensor_sequence)): # time step
            new_distribution = []
            new_path = []
            for j in range(len(self.loc_to_index_dict.keys())):
                #look at each block at given t and find a path with max probability.
                location = self.index_to_loc_dict[j]
                color = self.maze.get_color(location[0],location[1])
                if color == self.sensor_sequence[i]:
                    color_prob = 0.88
                else:
                    color_prob = 0.04
                max_val = -0.00001
                max_location = None
                for direction in range(5):
                    dx = 0
                    dy = 0
                    if direction == 0:
                        dx = 1
                    elif direction == 1:
                        dx = -1
                    elif direction == 2:
                        dy = -1
                    elif direction == 3:
                        dy = 1

                    if self.maze.is_floor(location[0]+dx, location[1]+dy):
                        trans_p = self.transition[self.loc_to_index_dict[(location[0]+dx, location[1]+dy)],self.loc_to_index_dict[location]]
                        prob = distribution[-1][self.loc_to_index_dict[(location[0]+dx, location[1]+dy)]]*trans_p*color_prob
                        if prob > max_val:
                            max_val = prob
                            max_location = (location[0]+dx, location[1]+dy)
                new_distribution.append(max_val)
                new_path.append(self.loc_to_index_dict[max_location])
            best_path.append(new_path)
            distribution.append(new_distribution)

        #backtracking
        best_path_final = []
        for i in range(len(distribution)):
            index = len(distribution) - 1- i
            if i == 0:
                best_path_final.append(np.argmax(distribution[index]))
            else:
                best_path_final.append(best_path[index+1][best_path_final[-1]])

        #converting index to location
        index_path = best_path_final[::-1]
        coordinate_path = []
        for index in index_path:
            coordinate_path.append(self.index_to_loc_dict[index])

        return coordinate_path

    def forward_backward(self):
        #extension: use forward-bacward algo to smooth the distribution
        if len(self.forward) == 0:
            #compute forward if not done
            self.filtering()
        state = np.ones((len(self.start_state),1))
        self.backward.append(state)
        sensor_sequence = copy.copy(self.sensor_sequence)
        for i in range(len(self.move_sequence)):
            #computing backward
            sensor_color = sensor_sequence.pop(-1)
            obs_matrix = np.diag(self.observation[:,self.color_to_index[sensor_color]])
            state = self.transition.transpose().dot(obs_matrix.dot(state))
            alpha = np.sum(state)
            state = (1/alpha)*state
            self.backward.append(state)

        for i in range(len(self.forward)):
            #combining forward and backward and updating at self.smoothing
            smooth_state = np.multiply(self.backward[len(self.forward)-1-i],self.forward[i])
            alpha = np.sum(smooth_state)
            self.smoothing.append((1/alpha)*smooth_state)

    def print_output(self,smooth = False):
        #prints output of running filtering
        #if smooth is true, also prints the result of smoothing
        print(self.maze)
        if len(self.forward) != 0:
            for i in range(len(self.forward)):
                print()
                print("-------------time: ",i," -------------")
                print("filtering result:")
                for j in range(len(self.forward[i])):
                    print(self.index_to_loc_dict[j],": ",self.forward[i][j])

                if smooth == True:
                    print()
                    print("smoothing result:")
                    for j in range(len(self.smoothing[i])):
                        print(self.index_to_loc_dict[j],": ",self.smoothing[i][j])

## A bit of test code

if __name__ == "__main__":
    #testing 1
    #runs without any walls(all floors)
    #interesting observation: Initially, I though of robot at (2,2) and moving with given sequence of direction
    #however, my viterbi algorithm found a different path that is as good as my initial one.
    test_maze1 = Maze("maze1.maz")
    hmm = HMM(test_maze1,['N','S','S','S','W'],['y','r','g','b','r'])
    hmm.filtering()
    hmm.forward_backward()
    hmm.print_output(smooth = True)
    print()
    print("----testing viterbi------")
    print(test_maze1)
    print("color sequence: ",hmm.sensor_sequence )
    print("result of viterbi: ",hmm.viterbi())

    #testing 2
    #runs with 3 walls
    #initial robot location: (2,1)
    #this time, there was only one optimal path for viterbi: shows that my viterbi works fine
    test_maze2 = Maze("maze2.maz")
    hmm = HMM(test_maze2,['W','N','N','E','E'],['y','b','g','y','b'])
    hmm.filtering()
    hmm.forward_backward()
    hmm.print_output(smooth = True)
    print()
    print("----testing viterbi------")
    print(test_maze2)
    print("color sequence: ",hmm.sensor_sequence )
    print("result of viterbi: ",hmm.viterbi())
