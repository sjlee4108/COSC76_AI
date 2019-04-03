from Maze import Maze
from time import sleep
from collections import deque
import math
from RobotDisplay import RobotDisplay

class MazeworldProblem:

    ## you write the constructor, and whatever methods your astar function needs

    def __init__(self, maze, goal_locations):
        self.maze = maze
        self.start_state = tuple([0]+self.maze.get_robotloc())
        self.goal_locations = goal_locations
        self.robot_turns = {
        }
        for i in range(int(len(self.maze.robotloc)/2)):
            if i == int(len(self.maze.robotloc)/2) - 1:
                self.robot_turns[i] = 0
            else:
                self.robot_turns[i] = i+1
        self.fuel = 1
        self.cost_dict = None
    def __str__(self):
        string =  "Mazeworld problem: "
        return string


        # given a sequence of states (including robot turn), modify the maze and print it out.
        #  (Be careful, this does modify the maze!)

    def animate_path_extension(self, path):
        display = RobotDisplay(self, path,0)
        display.start_simulation()

    def animate_path(self, path):
        # reset the robot locations in the maze
        self.maze.robotloc = tuple(self.start_state[1:])

        for state in path:
            print(str(self))
            self.maze.robotloc = tuple(state[1:])
            sleep(1)

            print(str(self.maze))

    def get_successors(self,state):
        xcoord = state[2*(state[0]+1)-1]
        ycoord = state[2*(state[0]+1)]
        self.maze.robotloc = tuple(state[1:])
        successors = []

        for i in range(5):
            new_state = list(state)
            if self.maze.is_floor(xcoord,ycoord+1) and self.maze.has_robot(xcoord,ycoord+1) == False and i == 0:
                x = xcoord
                y = ycoord+1
            elif self.maze.is_floor(xcoord+1,ycoord) and self.maze.has_robot(xcoord+1,ycoord) == False and i == 1:
                x = xcoord+1
                y = ycoord
            elif self.maze.is_floor(xcoord,ycoord-1) and self.maze.has_robot(xcoord,ycoord-1) == False and i == 2:
                x = xcoord
                y = ycoord-1
            elif self.maze.is_floor(xcoord-1,ycoord) and self.maze.has_robot(xcoord-1,ycoord) == False and i == 3:
                x = xcoord-1
                y = ycoord
            elif i == 4:
                x = xcoord
                y = ycoord
            else:
                continue
            new_state[0] =self.robot_turns[state[0]]
            new_state[2*(state[0]+1)-1] = x
            new_state[2*(state[0]+1)] = y
            successors.append(tuple(new_state))
        return successors
    def get_cost(self, state1, state2):
        step = 0
        for i in range(int(len(self.maze.robotloc))):
            step += abs(state1[i+1]-state2[i+1])
        if step*self.fuel == 0:
            return 0.001
        return step*self.fuel

    def goal_test(self,state):
        for i in range(int(len(self.maze.robotloc))):
            if self.goal_locations[i] != state[i+1]:
                return False
        return True

    def manhattan_heuristic(self, state):
        distance = 0
        num_robot = int(len(self.goal_locations)/2)
        for i in range(num_robot):
            distance += abs(state[2*(i+1)-1]-self.goal_locations[2*i]) + abs(state[2*(i+1)]-self.goal_locations[2*i+1])
        return distance

    def wavefront_successor(self,location):
        successors = []
        for i in range(4):
            dx = 0
            dy = 0
            if i == 0:
                dy += 1
            elif i == 1:
                dy -= 1
            elif i == 2:
                dx += 1
            else:
                dx -= 1
            if self.maze.is_floor(location[0]+dx, location[1]+dy) == True:
                successors.append((location[0]+dx, location[1]+dy))
        return successors

    def wavefront_bfs(self):
        start_location = self.start_state[1:]
        cost_dict_list = []
        for i in range(int(len(self.goal_locations)/2)):
            cost_dict = {}
            location = (self.goal_locations[2*i],self.goal_locations[2*i+1])
            frontier = deque([(location,0)])
            while(len(frontier) != 0):
                node = frontier.popleft()
                location = node[0]
                cost = node[1]
                cost_dict[location] = cost

                #if location == (start_location[i],start_location[i+1]):
                    #break

                successors = self.wavefront_successor(location)
                for i in range(len(successors)):
                    if successors[i] not in cost_dict.keys():
                        frontier.append((successors[i],cost+1))
            cost_dict_list.append(cost_dict)
        return cost_dict_list

    def wavefront_bfs_heuristic(self, state):
        if self.cost_dict == None:
            self.cost_dict = self.wavefront_bfs()
        cost = 0
        for robot_index in range(len(self.cost_dict)):
            cost += self.cost_dict[robot_index][(state[2*(robot_index+1)-1],state[2*(robot_index+1)])]
        return cost



## A bit of test code. You might want to add to it to verify that things
#  work as expected.


if __name__ == "__main__":
    test_maze3 = Maze("maze3.maz")
    print(test_maze3)
    test_mp = MazeworldProblem(test_maze3, (1, 4, 1, 3, 1, 2))
    print(test_mp.get_successors((1, 1, 0, 1, 1, 2, 1)))
