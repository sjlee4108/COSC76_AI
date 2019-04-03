#Seungjae Jason Lee
#Cosc 76 Project 4
#Jan 31 2018
import time
class ConstraintSatisfactionProblem():
    def __init__(self, num_variable, num_value):
        #parent class for CSP
        self.constraints = {}
        self.assignment = []
        self.num_value = num_value
        self.num_variable = num_variable
        self.neighbor = []
        self.domain = []
        self.counter = 0
        for i in range(self.num_variable):
            self.assignment.append(None)
    def check_constraint_arc(self, key, value):
        #check constraint of binary constraints
        #key is a tuple of variables and value is a tuple of values
        if key in self.constraints.keys():
            if value not in self.constraints[key]:
                return False
        if (key[1],key[0]) in self.constraints.keys():
            if (value[1],value[0]) not in self.constraints[(key[1],key[0])]:
                return False
        return True

    def check_constraint(self,variable, value):
        #checks if assigning the given value to the given variable satisfies constraint

        #makes a set of assigned variables.
        assigned_var = set()
        for i in range(len(self.assignment)):
            if self.assignment[i] != None:
                assigned_var.add(i)
        if len(assigned_var) == 0:
            #no assignemnt made. Thus, returns true as there are no constraints
            return True

        #loops over every constraint
        for key in self.constraints.keys():
            #looks for constraints with given variable
            if variable in key:
                valid_key = True
                #checks if all of the variables in the constraint key are assigned
                for v in key:
                    if v != variable and v not in assigned_var:
                        valid_key = False
                        break
                #if all of them are assigned, make a value tuple with given value and existing assignments
                if valid_key:
                    value_tup = []
                    for v in key:
                        if v == variable:
                            value_tup.append(value)
                        else:
                            value_tup.append(self.assignment[v])
                    #checks constraint
                    if tuple(value_tup) not in self.constraints[key]:
                        return False
        return True

    def build_neighbor(self):
        #helper method for binary constraints, inference(AC) and LCV
        for i in range(self.num_variable):
            neighbors = []
            for key in self.constraints.keys():
                if key[0] == i and len(key)==2:
                    neighbors.append(key[1])
            self.neighbor.append(neighbors)

    def goal_test(self):
        #checks if all assignment is complete
        if None in self.assignment:
            return False
        return True
