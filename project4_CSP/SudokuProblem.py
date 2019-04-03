#Seungjae Jason Lee
#Cosc 76 Project 4
#Jan 31 2018
from ConstraintSatisfactionProblem import ConstraintSatisfactionProblem
from backtracking import backtracking
import random
class SudokuProblem(ConstraintSatisfactionProblem):
    def __init__(self,fixed_slots, enable_reduce = True):
        #fixed slot is a list of tuple that has number and its x, y coordinates.
        #ex: [(5,3,4)] ==> there is 5 at (3,4) where (0,0) is the left bottom
        ConstraintSatisfactionProblem.__init__(self, 81, 9)
        self.location_to_number = {}
        self.number_to_location = {}
        self.square_blocks = {
            (0,0) : set([0,1,2,9,10,11,18,19,20]),
            (0,1) : set([27,28,29,36,37,38,45,46,47]),
            (0,2) : set([54,55,56,63,64,65,72,73,74]),
            (1,0) : set([3,4,5,12,13,14,21,22,23]),
            (1,1) : set([30,31,32,39,40,41,48,49,50]),
            (1,2) : set([57,58,59,66,67,68,75,76,77]),
            (2,0) : set([6,7,8,15,16,17,24,25,26]),
            (2,1) : set([33,34,35,42,43,44,51,52,53]),
            (2,2) : set([60,61,62,69,70,71,78,79,80])
        }
        count = 0
        for j in range(9):
            for i in range(9):
                self.location_to_number[(i,j)] =  count
                self.number_to_location[count] = (i,j)
                count += 1
        self.build_domain(fixed_slots)
        if enable_reduce:
            self.reduce_domain()


    def build_domain(self,fixed_slots):
        #builds domain:[value] for fixed slot and [1,2,3,4,5,6,7,8,9] for non-fixed slots
        self.fixed_dictionary = {}
        for i in range(len(fixed_slots)):
            self.fixed_dictionary[(fixed_slots[i][1],fixed_slots[i][2])] = fixed_slots[i][0]
        for j in range(9):
            for i in range(9):
                if (i,j) in self.fixed_dictionary.keys():
                    self.domain.append(set([self.fixed_dictionary[(i,j)]]))
                else:
                    self.domain.append(set([1,2,3,4,5,6,7,8,9]))

    def reduce_domain(self):
        #reduce domains based on information from fixed slots
        #extension
        for key in self.fixed_dictionary.keys():
            value = self.fixed_dictionary[key]
            for i in range(9):
                #checks horizontally and vertically
                if value in self.domain[self.location_to_number[(key[0],i)]] and (key[0],i) != key:
                    self.domain[self.location_to_number[(key[0],i)]].remove(value)
                if value in self.domain[self.location_to_number[(i,key[1])]] and (i,key[1]) != key:
                    self.domain[self.location_to_number[(i,key[1])]].remove(value)
            variable = self.location_to_number[key]

            #checks within 3*3 square block
            for location_num in self.square_blocks[(int((variable % 9)/3),int(variable/27))]:
                if value in self.domain[location_num] and location_num != variable:
                    self.domain[location_num].remove(value)

    def check_constraint(self, variable, value):
        if self.check_global_constraint(variable,value):
            return True
        return False

    def check_global_constraint(self,variable,value):
        # checks alldiff for given variable and given value
        location = self.number_to_location[variable]
        for i in range(9):
            if ((location[0],i) != location and self.assignment[self.location_to_number[(location[0],i)]] == value) or ((i, location[1]) != location and self.assignment[self.location_to_number[(i,location[1])]] == value):
                return False
        for location_index in self.square_blocks[(int((variable % 9)/3),int(variable/27))]:
            if self.assignment[location_index] == value and location_index != variable:
                return False
        return True

    def __str__(self):
        #nice string display
        string = "Sudoku Problem: \n"
        for j in range(9):
            for i in range(9):
                j_index = 8 - j
                if (i, j_index) in self.fixed_dictionary.keys():
                    string += str(self.fixed_dictionary[(i,j_index)])
                else:
                    string += "."
            string += "\n"

        string += "\nSolved Sudoku Problem: \n"
        for j in range(9):
            for i in range(9):
                j_index = 8 - j
                if self.assignment[self.location_to_number[(i,j_index)]] != None:
                    string += str(self.assignment[self.location_to_number[(i,j_index)]])
                else:
                    string += "."
            string += "\n"
        return string

if __name__ == "__main__":
    #test
    sudoku = SudokuProblem([(8,4,0),(7,7,0),(9,8,0),(4,3,1),(1,4,1),(9,5,1),(5,8,1),(6,1,2),(2,6,2),(8,7,2),(7,0,3),(2,4,3),(6,8,3),(4,0,4),(8,3,4),(3,5,4),(1,8,4),(8,0,5),(6,4,5),(3,8,5),
(9,1,6),(8,2,6),(6,7,6),(6,0,7),(1,3,7),(9,4,7),(5,5,7),(5,0,8),(3,1,8),(7,4,8)])
    print(backtracking(sudoku))
