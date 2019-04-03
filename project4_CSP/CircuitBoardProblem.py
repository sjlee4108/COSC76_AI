#Seungjae Jason Lee
#Cosc 76 Project 4
#Jan 31 2018
from ConstraintSatisfactionProblem import ConstraintSatisfactionProblem
import backtracking
import time
class CircuitBoardProblem(ConstraintSatisfactionProblem):
    def __init__(self,components, dimension):
        #dimension is a tuple that consists of width and height.
        #components must be a list of tuple of character, width, and height ex) ('a', 3, 2)
        ConstraintSatisfactionProblem.__init__(self, len(components),dimension[0]*dimension[1])
        self.components = components
        self.domain = []
        self.dimension = dimension
        self.location_to_number = {}
        self.number_to_location = {}

        count = 0
        for i in range(self.dimension[0]):
            for j in range(self.dimension[1]):
                self.location_to_number[(i,j)] = count
                self.number_to_location[count] = (i,j)
                count += 1

        self.build_domain()
        self.build_all_constraint()
        self.build_neighbor()

    def build_domain(self):
        #builds domain with given components
        #add locations where the component would fit on the board
        for component in self.components:
            component_domain = []
            for i in range(self.dimension[0]-component[1]+1):
                for j in range(self.dimension[1] - component[2]+1):
                    component_domain.append(self.location_to_number[(i,j)])
            self.domain.append(component_domain)

    def build_all_constraint(self):
        #builds constraint for components
        for i in range(len(self.components)):
           for j in range(i+1, len(self.components)):
               constraint = self.build_one_constraint(i,j)
               self.constraints[(i,j)] = constraint

    def build_one_constraint(self,index1, index2):
        #builds constraint set for given index1, index2 and returns it
        #indices represent variables
        constraint1 = set()
        for i in range(len(self.domain[index1])):
            left_bottom_i = self.number_to_location[self.domain[index1][i]]
            for j in range(len(self.domain[index2])):
                left_bottom_j = self.number_to_location[self.domain[index2][j]]

                #checks x-axis and sees if two components overlap
                #if not, add the location to the constraint
                #if so, check y-axis later in the 'else' part
                if left_bottom_j[0]+ self.components[index2][1]-1 < left_bottom_i[0] or left_bottom_i[0]+ self.components[index1][1]-1 < left_bottom_j[0]:
                    constraint1.add((self.location_to_number[left_bottom_i],self.location_to_number[left_bottom_j]))
                else:
                    #checks y-axis and sees if two component overlaps
                    if left_bottom_j[1]+ self.components[index2][2]-1 < left_bottom_i[1] or left_bottom_i[1]+ self.components[index1][2]-1 < left_bottom_j[1]:
                        constraint1.add((self.location_to_number[left_bottom_i],self.location_to_number[left_bottom_j]))
        return constraint1

    def __str__(self):
        #override __str__ for nice display of the problem
        string = "Circuit Board Problem with "+ str(len(self.components))+ " components and "+ str(self.dimension[0])+"*" + str(self.dimension[1])+ " dimensions\n"
        if self.goal_test():
            for j in range(self.dimension[1]):
                for i in range(self.dimension[0]):
                    x = i
                    y = self.dimension[1] - j-1
                    filled = False
                    for k in range(len(self.components)):
                        component = self.components[k]
                        if x >= self.number_to_location[self.assignment[k]][0] and x<= component[1]+ self.number_to_location[self.assignment[k]][0] -1 and y >= self.number_to_location[self.assignment[k]][1] and y<= component[2]+ self.number_to_location[self.assignment[k]][1] -1:
                            string += component[0]
                            filled = True
                            break
                    if filled == False:
                        string += '.'
                string += '\n'
        else:
            string += "No Solution Found"
        return string
if __name__ == "__main__":
    #test
    circuit = CircuitBoardProblem([('a',3,2),('b',5,2),('c',2,3),('e',7,1)],(10,3))
    s = time.time()
    print(backtracking.backtracking(circuit))
    e = time.time()
    print(e-s)
