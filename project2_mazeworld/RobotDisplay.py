import graphics as gr
import time
class RobotDisplay:
    def __init__(self, robot_problem, robot_path, problem_type):
        #settting up the background of the board
        #problem type: 0 for mulit robot, 1 for sensorless
        self.robot_path = robot_path
        self.robot_problem = robot_problem
        self.problem_type = problem_type
        self.maze = robot_problem.maze
        self.size_ratio = 30
        self.window = gr.GraphWin( "Robot Demo", self.size_ratio*self.maze.width, self.size_ratio*(self.maze.height+1), False)
        if (self.robot_path == []):
            return None

        self.board = self.maze.create_render_list()
        text_box = gr.Rectangle(gr.Point(0,self.size_ratio*(self.maze.height+1)), gr.Point(self.size_ratio*self.maze.width,self.size_ratio*(self.maze.height)))
        text_box.setFill("lightblue")
        text_box.draw(self.window)
        self.action_text = gr.Text(gr.Point(self.size_ratio*self.maze.width/2,self.size_ratio*(self.maze.height+0.5)), "")
        self.action_text.setSize(self.size_ratio)
        self.action_text.draw(self.window)

        self.robot_graphics = []
        self.robot_drawn = []
        for y in range(self.maze.height - 1, -1, -1):
            ycoord = self.maze.height - y - 1
            for x in range(self.maze.width):
                if self.board[self.maze.index(x, y)] == '#':
                    r = gr.Rectangle(gr.Point(x*self.size_ratio,ycoord*self.size_ratio), gr.Point((x+1)*self.size_ratio,(ycoord+1)*self.size_ratio))
                    r.draw(self.window)
                    r.setFill("black")
                elif self.problem_type == 1 and self.board[self.maze.index(x, y)] == '.':
                    c = gr.Circle(gr.Point((2*x+1)*self.size_ratio/2,(2*ycoord+1)*self.size_ratio/2), self.size_ratio/3)
                    c.draw(self.window)
                    c.setFill("red")
                    self.robot_graphics.append(c)
                    self.robot_drawn.append(True)
        if self.problem_type == 0:
            start_state = self.robot_path[0][1:]
            for i in range(int(len(start_state)/2)):
                text = chr(ord("A") + i)
                xcoord = start_state[2*i]
                ycoord = self.maze.height - start_state[2*i+1]-1
                t = gr.Text(gr.Point((2*xcoord+1)*self.size_ratio/2,(2*ycoord+1)*self.size_ratio/2),text)
                t.draw(self.window)
                t.setFill("red")
                t.setSize(20)
                self.robot_graphics.append(t)

                x = self.robot_problem.goal_locations[2*i]
                y = self.maze.height - self.robot_problem.goal_locations[2*i+1] -1
                goal_text = gr.Text(gr.Point((2*x+1)*self.size_ratio/2,(2*y+1)*self.size_ratio/2),text)
                goal_text.setFill("grey")
                goal_text.setSize(15)
                goal_text.draw(self.window)
        self.window.update()
        time.sleep(2)

    def start_simulation(self):
        if self.problem_type == 0:
            prev_state = self.robot_path[0]
            for state in self.robot_path[1:]:
                self.action_text.setText("Turn: "+chr(ord("A") + prev_state[0]))
                dx = state[2*(prev_state[0]+1)-1] - prev_state[2*(prev_state[0]+1)-1]
                dy = state[2*(prev_state[0]+1)] - prev_state[2*(prev_state[0]+1)]
                self.robot_graphics[prev_state[0]].move(dx*self.size_ratio,-dy*self.size_ratio)
                self.window.update()
                time.sleep(1)
                prev_state = state

        elif self.problem_type == 1:
            for state in self.robot_path[1:]:
                location_set = set(state[0])
                self.action_text.setText(state[1])
                len_robot = len(self.robot_graphics)
                for i in range(len_robot):
                    robot_graph = self.robot_graphics[len_robot-i-1]
                    x = int((2*robot_graph.getCenter().getX()/self.size_ratio - 1)/2)
                    y = self.maze.height - 1 -int((2*robot_graph.getCenter().getY()/self.size_ratio - 1)/2)
                    location = (x,y)
                    if location not in location_set and self.robot_drawn[len_robot-i-1] == True:
                        robot_graph.undraw()
                        self.robot_drawn[len_robot-i-1] = False

                    elif location in location_set and self.robot_drawn[len_robot-i-1] == False:
                        robot_graph.draw(self.window)
                        self.robot_drawn[len_robot-i-1] = True
                self.window.update()
                time.sleep(1)
        self.window.close()



def zero(state):
    return 0

if __name__ == "__main__":
    #print(Maze("maze1.maz"))
    #test_maze3 = Maze("maze3.maz")
    #test_problem = SensorlessProblem(test_maze3)
    #display = RobotDisplay(test_problem, astar_search(test_problem, test_problem.sensorless_heuristic).path,1)
    #display.start_simulation()
    #display = RobotDisplay(test_problem, astar_search(test_problem, zero).path,1)
    #display.start_simulation()

    #print(test_problem2.get_successors(test_problem2.start_state))

    #test_maze3 = Maze("maze3.maz")
    #print(test_maze3)
    #test_problem2 = MazeworldProblem(test_maze3, (1, 4, 1, 3, 1, 2))
    #display = RobotDisplay(test_problem2, astar_search(test_problem2, test_problem2.wavefront_bfs_heuristic).path,0)
    #display.start_simulation()
    pass
