#Seungjae Jason Lee
#COSC 76
#Project 1

import graphics as gr
import time
from math import sin, cos, radians

class RobotDisplay:
    #displays puzzle
    def __init__(self, width, height, arm_lengths, obstacles, init_config):
        self.ratio = 30
        self.window = gr.GraphWin( "Robot Demo", (width+1)*self.ratio, (height+1)*self.ratio, False)
        for i in range(height+1):
            line = gr.Line(gr.Point(0,i*self.ratio),gr.Point(width*self.ratio,i*self.ratio))
            line.setFill("grey")
            line.draw(self.window)
        for j in range(width+1):
            line = gr.Line(gr.Point(j*self.ratio,0),gr.Point(j*self.ratio,height*self.ratio))
            line.setFill("grey")
            line.draw(self.window)
        self.width = width
        self.height = height
        self.arm = arm_lengths
        self.arm_graphics = []
        self.joint_graphics = []

        point = [0,0]
        for i in range(len(self.arm)):
            new_point = [point[0]+self.arm[i]*cos(radians(init_config[i])), point[1]+self.arm[i]*sin(radians(init_config[i]))]
            self.arm_graphics.append(gr.Line(gr.Point(point[0]*self.ratio, (self.coord_to_pix(point[1]))*self.ratio),gr.Point(new_point[0]*self.ratio, self.coord_to_pix(new_point[1])*self.ratio  )))
            self.arm_graphics[-1].draw(self.window)
            self.joint_graphics.append(gr.Circle(gr.Point(point[0]*self.ratio, self.coord_to_pix(point[1])*self.ratio), self.ratio/4))
            self.joint_graphics[-1].setFill('red')
            self.joint_graphics[-1].draw(self.window)
            #print(point)
            point = new_point
        self.window.update()
        time.sleep(10)

    def coord_to_pix(self, y):
        return self.height - y
    #runs the simulation

# Create a few test problems:
RD = RobotDisplay(20,20,[4,4,5,5], [],[0,90,30,150])
