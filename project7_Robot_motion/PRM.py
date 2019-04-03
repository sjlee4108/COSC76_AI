#Seungjae Jason Lee
#COSC 76
#Project 7

import graphics as gr
import numpy as np
import time
import random
from sklearn.neighbors import NearestNeighbors
from math import sin, cos, radians
from shapely.geometry.polygon import LinearRing, Polygon
from robot_arm_display import RobotDisplay
from heapq import heappush, heappop

class Solution:
    #class to store information for astar_search
    def __init__(self):
        self.path = []
        self.nodes_visited = 0
        self.cost = 0

    def get_cost(self):
        #gets cost of the path
        return self.cost

    def get_path(self):
        #gets path
        return self.path

    def set_path(self,path):
        #assigns a path
        self.path = path

    def set_cost(self,cost):
        #sets the cost
        self.cost = cost

class AstarNode:
    # each search node except the root has a parent node
    # and all search nodes wrap a state object

    def __init__(self, state, heuristic, parent=None, transition_cost=0):
        # init method
        self.parent = parent
        self.state = state
        self.heuristic = heuristic
        self.transition_cost = transition_cost

    def priority(self):
        # computes cost + heuristic
        return self.heuristic + self.transition_cost

    def get_cost(self):
        #gets the cost to reach the state
        return self.transition_cost

    def get_state(self):
        #getter for state
        return self.state
    # comparison operator,
    # needed for heappush and heappop to work with AstarNodes:
    def __lt__(self, other):
        return self.priority() < other.priority()


class PRM:
    #PRM for robot arm sensor
    def __init__(self, arm_lengths, obstacles):
        #initialize
        self.arm = arm_lengths
        self.obstacles = obstacles


    def config_to_coord(self,config):
        #converts configuration(angles) to coordinates of joints
        points = []
        point = [0,0]
        points.append(point)
        for i in range(len(self.arm)):
            new_point = [point[0]+self.arm[i]*cos(radians(config[i])), point[1]+self.arm[i]*sin(radians(config[i]))]
            points.append(tuple(new_point))
            point = new_point
        return points

    def PRM_setup(self,n,k):
        #building vertical and edge for PRM and returns them
        V = []
        E = []
        while len(V) < n:
            while True:
                q = []
                for i in range(len(self.arm)):
                    q.append(random.random()*360)
                q = tuple(q)
                if self.check_collision_free(q) and self.check_on_plane(q):
                    V.append(q)
                    break

        for q in V:
            N = self.KNN(q,V,k)
            for neighbor_q in N:
                if (q,neighbor_q) not in N and self.delta(q, neighbor_q) != False:
                    E.append((q,neighbor_q))
        return V,E

    def PRM_query(self, init_config, final_config, k, V, E):
        #finds a path that is shortest from init to final with given vertex and edge
        neigh_init = self.KNN(init_config, V, k)
        neigh_final = self.KNN(final_config, V, k)
        V += init_config + final_config
        connected_init = False
        for config in neigh_init:
            if self.delta(init_config, config) != False:
                connected_init = True
                E.append((init_config, config))
                break

        connected_final = False
        for config in neigh_final:
            if self.delta(final_config, config) != False:
                connected_final = True
                E.append((final_config, config))
                break

        if connected_init == False or connected_final == False:
            return None
        P = self.astar_search(init_config, final_config, V, E)
        if P != []:
            return P
        else:
            return None

    def KNN(self,q,V,k):
        #k nearest neighbor using scikit-learn/ extension
        X = np.array(V)
        nbrs = NearestNeighbors(n_neighbors=k+1, algorithm='ball_tree').fit(X)
        distances, indices = nbrs.kneighbors(np.array([q]))
        neighbors = []
        for i in range(len(indices[0])):
            if distances[0][i] != 0:
                neighbors.append(V[indices[0][i]])
        return neighbors

    def delta(self, q, neighbor_q):
        #returns true if the distance between two q is small enough
        return self.euclidean(q, neighbor_q) < 50

    def euclidean(self, v1, v2):
        #computer euclidean distancec of two vectors
        sum = 0
        for i in range(len(v1)):
            sum += (v1[i]-v2[i])**(2)
        return sum**(0.5)

    def check_collision_free(self, q):
        #checks if q is collision free
        arm = LinearRing(self.config_to_coord(q))
        for object in self.obstacles:
            obstacle = Polygon(object)
            if obstacle.disjoint(arm) == False:
                return False
        return True

    def check_on_plane(self,q):
        #checks if the joints are on the plane
        points = self.config_to_coord(q)
        for point in points:
            if point[0] < 0 or point[1] < 0:
                return False
        return True

    def get_successors(self,q,E):
        #returns connected config to q
        successors = []
        for edge in E:
            for i in range(2):
                if i == 0 and edge[0] == q:
                    successors.append(edge[1])
                    break
                if i == 1 and edge[1] == q:
                    successors.append(edge[0])
        return successors

    def backchain(self,node):
        #backchaining for astar
        result = []
        current = node
        while current:
            result.append(current.state)
            current = current.parent

        result.reverse()
        return result


    def astar_search(self, init, final, V, E):
        # astar search for this specific problem
        start_node = AstarNode(init, self.euclidean(init, final))
        pqueue = []
        heappush(pqueue, start_node)

        solution = Solution()

        visited_cost = {}
        visited_cost[start_node.state] = 0
        while(pqueue != []):
            node = heappop(pqueue)
            solution.nodes_visited += 1
            successors = self.get_successors(node.get_state(), E)

            if node.get_state() == final:
                if solution.get_cost() == 0 or (solution.get_cost() != 0 and solution.get_cost() > visited_cost[node.get_state()]):
                    solution.set_path(self.backchain(node))
                    solution.set_cost(visited_cost[node.get_state()])
            if solution.get_cost() < visited_cost[node.get_state()] and len(solution.get_path()) != 0:
                break
            for i in range(len(successors)):
                successor_cost = self.euclidean(node.get_state(), successors[i]) + node.get_cost()
                n = AstarNode(successors[i], self.euclidean(node.get_state(), final), parent = node, transition_cost = successor_cost)
                if successors[i] in visited_cost.keys() and successor_cost >= visited_cost[successors[i]]:
                    continue
                visited_cost[successors[i]] = successor_cost
                heappush(pqueue, n)
        return solution.path


if __name__ == '__main__':
    # #testing with k = 5
    start = time.time()
    model = PRM([4,4,5,5], [[(0,4),(4,4),(4,8),(0,8)]])
    vertex, edge = model.PRM_setup(5000,5)
    init = (0,90,30,150)
    final = (0,90,0,315)
    path = model.PRM_query(init, final, 5, vertex, edge)
    end = time.time()
    print("time taken for k = 5: ",end-start )
    print("number of edge for k = 5: ", len(edge))
    print("number of vertex for k = 5: ", len(vertex))
    if path != None:
        RD = RobotDisplay(20,20,[4,4,5,5], [[(0,4),(4,4),(4,8),(0,8)]],init)
        RD.show_simulation(path)
    else:
        print("no solution found")

    # Analysis of testing different k value k = 3
    start = time.time()
    model = PRM([4,4,5,5], [[(0,4),(4,4),(4,8),(0,8)]])
    vertex, edge = model.PRM_setup(5000,3)
    init = (0,90,30,150)
    final = (0,90,0,315)
    path = model.PRM_query(init, final, 3, vertex, edge)
    end = time.time()
    print("time taken for k = 3: ",end-start )
    print("number of edge for k = 3: ", len(edge))
    print("number of vertex for k = 3: ", len(vertex))
    if path != None and False:
        RD = RobotDisplay(20,20,[4,4,5,5], [[(0,4),(4,4),(4,8),(0,8)]],init)
        RD.show_simulation(path)
    else:
        print("no solution found")
