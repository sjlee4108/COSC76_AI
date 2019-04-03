#Seungjae Jason Lee
#Cosc 76 Project 4
#Jan 31 2018
from collections import deque
import time
def backtracking(CSP, AC_3 = False, MAC_3 = False, value_heu = None, variable_heu = None):
    #backtracking solver
    #takes CSP problem as required input
    #rest are optional input for heuristcs and inference
    assignment_order = []
    for i in range(len(CSP.assignment)):
        assignment_order.append(i)
    if AC_3 == True:
        if inference_AC_3(CSP) == False:
            print("has no solution")
            return CSP
    return backtracking_recursive(CSP, assignment_order, value_heu = value_heu, variable_heu = variable_heu, MAC_3 = MAC_3 )

def backtracking_recursive(CSP, assignment_order, value_heu = None, variable_heu = None, MAC_3 = False):
    #recursive part of backtracking method
    #needs assignment_order, which is a list of indices of CSP.assignment(equivalent to variables)
    CSP.counter += 1 # check number of recursion
    if CSP.goal_test():
        return CSP

    #variable heuristic
    if variable_heu != None:
        assignment_order = variable_heu(CSP, assignment_order)
    assignment_ind = assignment_order.pop(0)

    #inference
    if MAC_3:
        if inference_MAC_3(CSP, assignment_ind) == False:
            return CSP

    #value heuristic
    if value_heu != None:
        domain = value_heu(CSP, assignment_ind, CSP.domain[assignment_ind])
    else:
        domain = CSP.domain[assignment_ind]

    #tests for different values in the domain
    for i in domain:
        if CSP.check_constraint(assignment_ind,i):
            CSP.assignment[assignment_ind] = i
            #print(assignment_order)
            CSP = backtracking_recursive(CSP,assignment_order, value_heu = value_heu, variable_heu = variable_heu, MAC_3 = MAC_3 )

        if CSP.goal_test():
            return CSP
    assignment_order.insert(0,assignment_ind)
    CSP.assignment[assignment_ind] = None
    return CSP

def inference_AC_3(CSP):
    #extension: inference for all arcs
    #updates all domains so that all arcs(binary constraints) are consistent and returns True if possible
    #returns False if not possible.
    queue = deque(CSP.constraints.keys())
    while(len(queue) != 0):
        arc = queue.popleft()
        if revise_AC_3(CSP, arc):
            if len(CSP.domain[arc[0]] ) == 0:
                return False
            for variable in CSP.neighbor[arc[0]]:
                queue.append((variable, arc[0]))
    return True

def revise_AC_3(CSP, arc):
    #helper function, updates domains for consistency
    revised =  False
    length = len(CSP.domain[arc[0]])
    for i in range(length):
        index = length - i -1
        value1 = CSP.domain[arc[0]][index]
        consistent = False
        for j in range(len(CSP.domain[arc[1]])):
            value2 = CSP.domain[arc[1]][j]
            if CSP.check_constraint_arc(arc,(value1, value2)) ==  True:
                consistent = True
                break
        if consistent == False:
            CSP.domain[arc[0]].pop(index)
            revised = True

    return revised

def inference_MAC_3(CSP,variable):
    #finds if neighbors can be consistent for given variable and updates domain if posible
    #return False if not
    domain_before_mod = CSP.domain
    queue = deque()
    for v in CSP.neighbor[variable]:
        if CSP.assignment[v] == None:
            queue.append((variable,v))
    while(len(queue) != 0):
        arc = queue.popleft()
        if revise_AC_3(CSP, arc):
            if len(CSP.domain[arc[0]]) == 0:
                CSP.domain = domain_before_mod
                return False
            for v in CSP.neighbor[arc[0]]:
                if CSP.assignment[v] == None:
                    queue.append((v, arc[0]))
    return True

def MRV(CSP,assignment_order):
    #sorts assignment_order based on number of values in the domain
    #least first
    sorting = assignment_order[:]
    for i in range(len(assignment_order)):
        sorting[i] = (assignment_order[i], len(CSP.domain[assignment_order[i]]))
    sorting.sort(key = return_second)
    for i in range(len(assignment_order)):
        assignment_order[i] = sorting[i][0]
    #print(sorting)
    return assignment_order

def MRV_Group(CSP,assignment_order):
    #Extension: MRV for CS10 Problem
    #modified to fit the problem

    ta_index = len(assignment_order) - len(CSP.student_list)
    ta_order = []
    if ta_index >= 0:
        #divide ta and student
        ta_order = MRV(CSP, assignment_order[:ta_index])
        student_order = MRV(CSP, assignment_order[ta_index:])
    else:
        #no tas are left in assignmet_order. Just order students
        student_order = MRV(CSP, assignment_order)
    return ta_order+student_order

def LCV(CSP, assignment_ind, domain):
    #LCV, orders domain based on least constrained values first.
    sorting = domain[:]
    for i in range(len(domain)):
        count = 0
        for neighbor in CSP.neighbor[assignment_ind]:
            for value in CSP.domain[neighbor]:
                if CSP.check_constraint_arc((assignment_ind,neighbor),(domain[i],value)) == False:
                    count += 1
        sorting[i] = (domain[i], count)
    sorting.sort(key = return_second)
    for i in range(len(domain)):
        domain[i] = sorting[i][0]
    return domain

def return_second(list):
    #helper function for sorting
    return list[1]
