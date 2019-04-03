from Maze import Maze
from time import sleep
from RobotDisplay import RobotDisplay

class SensorlessProblem:

    ## You write the good stuff here:
    def __init__(self, maze):
        self.maze = maze
        self.start_state = self.build_start_state()
        self.maze.robotloc = []
        self.direction_dict = {
            0:"East",
            1:"West",
            2:"North",
            3:"South"
        }
    def build_start_state(self):
        start_state = set()
        for i in range(self.maze.width):
            for j in range(self.maze.height):
                if self.maze.is_floor(i,j):
                    start_state.add((i,j))
        return tuple([tuple(start_state), "start"])

    def get_successors(self,state):
        successors = []
        for i in range(4):
            new_state = self.build_successor(state[0], i)
            if new_state != state[0]:
                successors.append(tuple([new_state,self.direction_dict[i]]))
        return successors

    def build_successor(self,state,direction):
        delta_x = 0
        delta_y = 0
        if direction == 0:
            #print("right")
            delta_x += 1
        elif direction == 1:
            #print("left")
            delta_x -= 1
        elif direction == 2:
            #print("up")
            delta_y += 1
        else:
            #print("down")
            delta_y -= 1

        successor = set()
        for location in state:
            if self.maze.is_floor(location[0]+delta_x, location[1]+delta_y):
                successor.add((location[0]+delta_x, location[1]+delta_y))
            else:
                successor.add((location[0], location[1]))
        return tuple(successor)

    def __str__(self):
        string =  "Blind robot problem: "
        return string


        # given a sequence of states (including robot turn), modify the maze and print it out.
        #  (Be careful, this does modify the maze!)
    def animate_path_extension(self, path):
        display = RobotDisplay(self, path,1)
        display.start_simulation()

    def animate_path(self, path):
        # reset the robot locations in the maze
        for state in path:
            possible_loc = state[0]
            print("Move: "+state[1])
            for j in range(self.maze.height):
                index = self.maze.height - j -1
                str = ""
                for i in range(self.maze.width):
                    if (i,index) in possible_loc:
                        str += "A"
                    elif self.maze.is_floor(i,index) == False:
                        str+="x"
                    else:
                        str+=" "
                print(str)
            print()
            sleep(1)

    def get_cost(self,state1, state2):
        return 1
    def goal_test(self,state):
        if len(state[0]) == 1:
            return True
        return False

    def sensorless_heuristic(self,state):
        loc_set = set(state[0])
        xmax = -1
        xmin = 100000000
        ymax = -1
        ymin = 100000000
        for location in loc_set:
            if location[0] > xmax:
                xmax = location[0]
            if location[0] < xmin:
                xmin = location[0]
            if location[1] > ymax:
                ymax = location[1]
            if location[1] < ymin:
                ymin = location[1]
        return abs(ymax - ymin) + abs(xmax-xmin)

## A bit of test code

if __name__ == "__main__":
    test_maze3 = Maze("maze3.maz")
    print(test_maze3)
    test_problem = SensorlessProblem(test_maze3)
    print(test_problem.get_successors(test_problem.start_state))
