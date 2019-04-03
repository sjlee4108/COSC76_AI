#Seungjae Jason Lee
#COSC 76
#Project 1

from puzzle import PuzzleProblem
from uninformed_search import bfs_search, dfs_search, ids_search
import graphics as gr
import time

class PuzzleDisplay:
    #displays puzzle
    def __init__(self, game_path):
        self.window = gr.GraphWin( "Puzzle Demo", 300, 300, False)
        self.rectangles = []
        self.text = []
        self.game_path = game_path
        start_state = game_path[0]
        count = 0
        for j in range(3):
            for i in range(3):
                if start_state[count] != 'x':
                    r = gr.Rectangle(gr.Point(i*100+5,j*100+5), gr.Point((i+1)*100-5,(j+1)*100-5))
                    r.draw(self.window)
                    r.setFill("light grey")
                    r.setOutline("light grey")
                    t = gr.Text(r.getCenter(), str(start_state[count]))
                    t.draw(self.window)
                else:
                    r = gr.Rectangle(gr.Point(i*100+5,j*100+5), gr.Point((i+1)*100-5,(j+1)*100-5))
                    r.setFill("light grey")
                    r.setOutline("light grey")
                    t = gr.Text(r.getCenter(), str(start_state[count]))
                self.text.append(t)
                self.rectangles.append(r)
                count += 1

    #runs the simulation
    def start_simulation(self):
        self.window.update()
        time.sleep(1)
        for i in range(len(self.game_path)-1):
            state = self.game_path[i+1]
            for j in range(9):
                if self.text[j].getText() != str(state[j]):
                    self.text[j].setText(str(state[j]))
                    if self.text[j].getText() == 'x':
                        self.text[j].undraw()
                        self.rectangles[j].undraw()
                    else:
                        self.rectangles[j].draw(self.window)
                        self.text[j].draw(self.window)
            self.window.update()
            time.sleep(1)

# Create a few test problems:
puzzle_prob_1 = PuzzleProblem((1,8,'x',4,2,7,6,5,3))



print(bfs_search(puzzle_prob_1))
print(dfs_search(puzzle_prob_1))
print(ids_search(puzzle_prob_1))
d2 = PuzzleDisplay(bfs_search(puzzle_prob_1))
d2.start_simulation()
