#Seungjae Jason Lee
#COSC 76
#Project 1

from robot_game import RobotProblem
from uninformed_search import bfs_search, dfs_search, ids_search
import graphics as gr
import time

class RobotDisplay:
    def __init__(self, robot_game, robot_path):
        #settting up the background of the board
        self.window = gr.GraphWin( "Puzzle Demo", 300, 300, False)
        self.game_path = robot_path
        self.board = robot_game.get_board()
        self.dimension = len(self.board)
        if (self.game_path == []):
            return None
        start_state = self.game_path[0]
        goal_state = self.game_path[-1]
        self.size = 300 / self.dimension
        for i in range(self.dimension):
            for j in range(self.dimension):
                if self.board[i][j] == 'x':
                    r = gr.Rectangle(gr.Point(j*self.size,i*self.size), gr.Point((j+1)*self.size,(i+1)*self.size))
                    r.draw(self.window)
                    r.setFill("black")

        i = goal_state[0]
        j = goal_state[1]
        self.goal_graphics = gr.Rectangle(gr.Point(j*self.size,i*self.size), gr.Point((j+1)*self.size,(i+1)*self.size))
        self.goal_graphics.draw(self.window)
        self.goal_graphics.setFill("orange")

        self.robot_graphics = gr.Circle(gr.Point((2*start_state[1]+1)/2*self.size,(2*start_state[0]+1)/2*self.size),self.size/2)
        self.robot_graphics.draw(self.window)
        self.robot_graphics.setFill("yellow")
        self.window.update()
        time.sleep(4)

    def start_simulation(self):
        #runs simulation
        if (self.game_path == []):
            return None
        self.window.update()
        time.sleep(1)
        for i in range(len(self.game_path)-1):
            state = self.game_path[i+1]
            self.robot_graphics.move((2*state[1]+1)*self.size/2 - self.robot_graphics.getCenter().getX(), (2*state[0]+1)*self.size/2-self.robot_graphics.getCenter().getY())
            self.window.update()
            time.sleep(1)

# Create a few test problems:
robot_prob = RobotProblem(10)
robot_prob.print_game_state()
result = bfs_search(robot_prob)
print("bfs:", result)
print("dfs: ",dfs_search(robot_prob))
print("ids: ",ids_search(robot_prob))
d2 = RobotDisplay(robot_prob, result)
d2.start_simulation()
