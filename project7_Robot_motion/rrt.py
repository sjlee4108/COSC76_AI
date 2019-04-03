#Seungjae Jason Lee
#COSC 76
#Project 7
# using shapely for collision detection

from shapely.geometry import Polygon, Point

import numpy as np
import time
import random
from sklearn.neighbors import NearestNeighbors
from shapely.geometry.polygon import LinearRing, Polygon, LineString
from planar_trajectory import *
from planar_display import *

class Node:
    #node stores vertex
    def __init__(self, q, parent_q, path, move = []):
        self.state = q
        self.parent = parent_q
        self.path = path
        self.move = move

class RRT:
    #RRT is used to solve car problem
    def __init__(self, delta_t, border, obstacles):
        #init
        self.delta_t = delta_t
        self.boundary = [[0, border[0]], [0,border[1]]]
        point1 = [self.boundary[0][0], self.boundary[1][0]]
        point2 = [self.boundary[0][1], self.boundary[1][1]]
        dx = self.boundary[0][1] - self.boundary[0][0]
        dy = self.boundary[1][1] - self.boundary[1][0]
        self.borders = []
        for i in range(4):
            if i == 0:
                self.borders.append(LineString([point1,[point1[0]+dx, point1[1]]]))
            elif i == 1:
                self.borders.append(LineString([point1,[point1[0], point1[1]+dy]]))
            elif i == 2:
                self.borders.append(LineString([point2,[point2[0]-dx, point2[1]]]))
            else:
                self.borders.append(LineString([point2,[point2[0], point2[1]-dy]]))
        self.obstacles = []
        for o in obstacles:
            self.obstacles.append(Polygon(o))





    def Run_RRT(self, init,goal, k):
        #runs RRT and returns a path if exists
        vertex = []
        edge = []
        vertex.append(Node(init, None,[init]))
        for i in range(k):
            rand_q =  self.random_config()
            near_q_node = self.nearest_vertex(rand_q, vertex)
            for j in range(6):
                #print(i)
                new_q = self.child_config(near_q_node, j)
                if new_q != near_q_node.state and self.check_collision(new_q):
                    vertex.append(Node(new_q, near_q_node,near_q_node.path+[new_q], move = near_q_node.move+[j]))
                    edge.append((near_q_node,new_q))
                    if self.check_goal_state(new_q, goal):
                        return vertex[-1].path, vertex[-1].move

        return None,None

    def child_config(self, q_node, move_index):
        #returns the next configuration after making move based on move_index
        x = q_node.state[0]
        y = q_node.state[1]
        theta = q_node.state[2]
        plane_traj = PlanarTrajectory(controls_rs,x,y,theta, [move_index], [self.delta_t] )
        return plane_traj.config_at_t(self.delta_t-0.000001)

    def convert_list(self, vertex):
        #converts a list of vertex nodes to a list of points
        v_list = []
        for v in vertex:
            v_list.append(v.state)
        return v_list

    def check_goal_state(self, q1, goal):
        #checks if the goal state is reached with q1
        for i in range(len(goal)):
            if i == 2:
                # pass
                if abs(goal[i]- q1[i]) > 0.6:
                    return False
            else:
                if abs(goal[i]- q1[i]) > 1:
                    return False
        return True

    def random_config(self):
        #returns a random configuration within the bound
        x = random.uniform(self.boundary[0][0], self.boundary[0][1])
        y = random.uniform(self.boundary[1][0], self.boundary[1][1])
        theta = random.random()*2*np.pi
        return (x,y,theta)

    def check_collision(self, q):
        #checks collison with walls and obstacles
        for obstacle in self.obstacles:
            if obstacle.disjoint(Point(q[0],q[1]).buffer(0.25)) == False:
                return False
        for line in self.borders:
            if line.disjoint(Point(q[0],q[1]).buffer(0.25)) == False:
                return False

        return True

    def nearest_vertex(self,q,V):
        #finds nearest vertex, extension: use scikit
        X = np.array(self.convert_list(V))
        nbrs = NearestNeighbors(n_neighbors=1, algorithm='ball_tree').fit(X)
        distances, indices = nbrs.kneighbors(np.array([q]))
        return V[indices[0][0]]

    def nearest_vertex_extension(self,q,V):
        #extension: normalized before finding nearest
        X = np.array(self.convert_list(V))
        X[:,0] = X[:,0]/self.boundary[0][1]
        X[:,1] = X[:,1]/self.boundary[1][1]
        X[:,2] = X[:,2]/(2*np.pi)
        nbrs = NearestNeighbors(n_neighbors=1, algorithm='ball_tree').fit(X)
        distances, indices = nbrs.kneighbors(np.array([[q[0]/self.boundary[0][1],q[1]/self.boundary[1][1],q[2]/(2*np.pi)]]))
        return V[indices[0][0]]

def draw1(q, move, duration, obstacles):
    #draws the final result
    traj = PlanarTrajectory(controls_rs, q[0], q[1], q[2], move, duration)

    tview = TrajectoryView(traj, obstacles)

    ax = plt.axes()

    tview.draw(ax, sum(duration)-0.01)


if __name__ == '__main__':
    #demonstration of RRT
    #car robot has to go through two rectangle blocks to reach the destination position.
    rrt = RRT(2, [50,50], [[[20,30],[50,30],[50,20],[20,20]], [[0,40],[30,40],[30,35],[0,35]]])
    vertex, move = rrt.Run_RRT((25, 50, .5), (50, 20 , .5),5000)
    if vertex != None:
        time_list = []
        for i in range(len(move)):
            time_list.append(rrt.delta_t)
        draw1((25, 50, .5), move, time_list,[[[20,30],[50,30],[50,20],[20,20]], [[0,40],[30,40],[30,35],[0,35]]])
        plt.show()
    else:
        print("Result not found")

    #testing different "delta_t"
    #testing with delta_t = 2
    rrt = RRT(2, [50,50], [[[0,0],[0,10],[10,10],[10,0]], [[12,12],[30,12],[30,30],[12,30]]])
    vertex, move = rrt.Run_RRT((11, 8, .5), (8, 14 , .5),1000)
    if vertex != None:
        time_list = []
        for i in range(len(move)):
            time_list.append(rrt.delta_t)
        draw1((11, 8, .5), move, time_list,[[[0,0],[0,10],[10,10],[10,0]], [[12,12],[30,12],[30,30],[12,30]]])
        plt.show()
    else:
        print("Result not found")

    #testing different "delta_t"
    #testing with delta_t = 5
    #could not find an answer as delta_t is too big for this map
    rrt = RRT(5, [50,50], [[[0,0],[0,10],[10,10],[10,0]], [[12,12],[30,12],[30,30],[12,30]]])
    vertex, move = rrt.Run_RRT((11, 8, .5), (8, 14 , .5),1000)
    if vertex != None:
        time_list = []
        for i in range(len(move)):
            time_list.append(rrt.delta_t)
        draw1((11, 8, .5), move, time_list,[[[0,0],[0,10],[10,10],[10,0]], [[12,12],[30,12],[30,30],[12,30]]])
        plt.show()
    else:
        print("Result not found")
