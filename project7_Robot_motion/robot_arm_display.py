#Seungjae Jason Lee
#COSC 76
#Project 1

import graphics as gr
import time
from math import sin, cos, radians

class RobotDisplay:
    #displays puzzle
    def __init__(self, width, height, arm_lengths, obstacles, init_config):
        #initializing the display screen with grid and default shapes such as arms and joints
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

        for i in range(len(obstacles)):
            point_list = []
            for j in range(len(obstacles[i])):
                point_list.append(gr.Point(obstacles[i][j][0]*self.ratio, self.coord_to_pix(obstacles[i][j][1])*self.ratio))
            obstacle = gr.Polygon(point_list)
            obstacle.draw(self.window)
        self.window.update()
        time.sleep(2)

    def coord_to_pix(self, y):
        #converts y coordinate to pixel coordinate
        return self.height - y

    def config_to_coord(self,config):
        #converts config into a list of points for joints
        points = []
        point = [0,0]
        points.append(point)
        for i in range(len(self.arm)):
            new_point = [point[0]+self.arm[i]*cos(radians(config[i])), point[1]+self.arm[i]*sin(radians(config[i]))]
            points.append(tuple(new_point))
            point = new_point
        return points

    #runs the simulation based on givenn sequence
    def show_simulation(self,sequence):
        for i in range(len(sequence)):
            points = self.config_to_coord(sequence[i])
            for j in range(len(self.arm)):
                dx = points[j][0]*self.ratio - self.joint_graphics[j].getCenter().getX()
                dy = self.coord_to_pix(points[j][1])*self.ratio - self.joint_graphics[j].getCenter().getY()
                self.joint_graphics[j].move(dx, dy)
                self.arm_graphics[j].undraw()
                self.arm_graphics[j] = gr.Line(gr.Point(points[j][0]*self.ratio, self.coord_to_pix(points[j][1])*self.ratio), gr.Point(points[j+1][0]*self.ratio, self.coord_to_pix(points[j+1][1])*self.ratio))
                self.arm_graphics[j].draw(self.window)
            self.window.update()
            time.sleep(2)
