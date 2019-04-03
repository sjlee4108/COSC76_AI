#Seungjae Jason Lee
#Cosc 76 Project 4
#Jan 31 2018
from ConstraintSatisfactionProblem import ConstraintSatisfactionProblem
from backtracking import backtracking
import time
class MapColoringCSP(ConstraintSatisfactionProblem):
    def __init__(self,locations, colors):
        #assigns colors to a given map without having overlapping colors for neighboring regions
        #location = list of locations(string)
        #colors = list of colors(string)
        ConstraintSatisfactionProblem.__init__(self, len(locations),len(colors))
        self.colors = colors
        self.locations = locations
        self.domain = []
        self.locations_index_dict = {}

        #building domain
        for i in range(len(locations)):
            self.locations_index_dict[locations[i]] = i
            location_domain = []
            for j in range(len(self.colors)):
                location_domain.append(j)
            self.domain.append(location_domain)


    def set_neighbor(self,list):
        #builds binary constraints and completes constraint dictionary
        for neighbor in list:
            location1 = neighbor[0]
            location2 = neighbor[1]
            if location1 in self.locations_index_dict.keys() and location2 in self.locations_index_dict.keys():
                constraint = set()
                for i in range(len(self.colors)):
                    for j in range(len(self.colors)):
                        if i != j:
                            constraint.add((i,j))
                self.constraints[(self.locations_index_dict[location1], self.locations_index_dict[location2])] = constraint
        self.build_neighbor()

    def __str__(self):
        #print the result nicely
        string = "Map Problem with "+ str(len(self.colors))+ " colors and "+ str(len(self.locations)) + " locations\n"
        if self.goal_test():
            for i in range(len(self.assignment)):
                string += self.locations[i] +": " + self.colors[self.assignment[i]]+"\n"
        return string

if __name__ == "__main__":
    #simple test
    aust_map = MapColoringCSP(["WA","NT","SA","Q","NSW","V","T"],['r','g','b'])
    aust_map.set_neighbor([("WA","NT"),("WA","SA"),("SA","Q"),("SA","NSW"),("SA","V"),("NT","Q"),("Q","NSW"),("NSW","V"),("SA","NT")])
    print(backtracking(aust_map))
