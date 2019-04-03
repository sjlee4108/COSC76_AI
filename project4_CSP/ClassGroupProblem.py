#Seungjae Jason Lee
#Cosc 76 Project 4
#Jan 31 2018
from ConstraintSatisfactionProblem import ConstraintSatisfactionProblem
from backtracking import backtracking, MRV_Group
import random
class ClassGroupProblem(ConstraintSatisfactionProblem):
    def __init__(self,time_list, ta_list, student_list):
        #solves CS10 Problem
        ConstraintSatisfactionProblem.__init__(self, len(ta_list+student_list),len(time_list))
        self.time_list = time_list
        self.ta_list = ta_list
        self.student_list = student_list
        self.build_domain(ta_list+student_list)
        self.build_binary_constraint(ta_list)

    def build_domain(self,student_list):
        #builds domain based on ta_list + student_list
        for i in range(len(student_list)):
            domain = []
            for j in range(len(student_list[i])):
                if student_list[i][j] == 'O':
                    domain.append(j-1)
            self.domain.append(domain)

    def build_binary_constraint(self,ta_list):
        #builds binary constraints for TA
        for i in range(len(ta_list)):
            for j in range(i+1, len(ta_list)):
                self.constraints[(i,j)] = self.build_one_constraint(i,j)

    def build_one_constraint(self, index1, index2):
        #helper for previous method
        constraint = set()
        for value1 in self.domain[index1]:
            for value2 in self.domain[index2]:
                if value1 != value2:
                    constraint.add((value1,value2))
        return constraint

    def check_constraint(self, variable, value):
        #overrides check_constraint method
        #need to check "local constraint" and global constraint
        if self.check_global_constraint(variable,value) and super(ClassGroupProblem,self).check_constraint(variable, value):
            return True
        return False

    def check_global_constraint(self,variable,value):
        # TAs do not have global constraint but just binary constraint
        if variable < len(self.ta_list):
            return True

        #make a set of group sessions with assigned students
        group_list = []
        for i in range(len(self.time_list)):
            group_list.append(set())

        assigned = 0
        for i in range(len(self.assignment)):
            if self.assignment[i] != None:
                group_list[self.assignment[i]].add(i)
                assigned += 1

        if len(group_list[value]) == 0:
            #No TA in this session
            return False

        lower_limit = int(len(self.assignment)/len(self.ta_list)) - 1
        upper_limit = int(len(self.assignment)/len(self.ta_list)) + 1
        #checks lower bound at the last assignment
        if assigned == len(self.assignment)-1:
            for i in range(len(group_list)):
                if len(group_list[i]) < lower_limit and len(group_list[i]) != 0:
                    return False
        #checks upper bound at every assignment
        if len(group_list[value]) < upper_limit:
            return True
        return False

    def __str__(self):
        #nice display of the problem
        string = "Classroom Group Problem with " + str(len(self.time_list)) + " sessions, " + str(len(self.ta_list)) + " TAs, " + str(len(self.student_list)) + " students\ntime  "
        for i in range(len(self.time_list)):
            string += self.time_list[i] + "  "
        string += "\n"
        everyone = self.ta_list+self.student_list
        for person in everyone:
            for j in person:
                string += "  " + j + "  "
            string += '\n'
        if self.goal_test():
            stu_list = []
            for i in range(len(self.time_list)):
                stu_list.append([])
            for i in range(len(self.ta_list),len(self.assignment)):
                stu_list[self.assignment[i]].append(i)
            for j in range(len(self.ta_list)):
                time = self.assignment[j]
                string += self.time_list[time] +": "
                string += self.ta_list[j][0]
                for stu in stu_list[time]:
                    string += ", "+ self.student_list[stu-len(self.ta_list)][0]
                string += "\n"
        return string

if __name__ == "__main__":
    # ta = [['t1', 'O','X','O','X','O'],['t2', 'X','X','O','O','O'],['t3', 'O','X','X','O','O'],['t4', 'X','O','X','X','O']]
    # student = [['s1', 'O','X','O','X','O'],['s2', 'X','X','O','O','O'],['s3', 'O','O','X','O','O'],['s4', 'X','O','X','X','X'],['s5', 'O','O','O','O','O'],['s6', 'X','X','X','O','O'],['s7', 'O','X','X','X','O'],['s8', 'O','O','O','X','O'],['s9', 'O','X','O','X','X'],['s10', 'O','X','O','X','O'],['s11', 'O','X','O','O','O'],['s12', 'X','X','X','X','O'],['s13', 'O','X','O','X','X'],['s14', 'O','X','O','O','X'],['s15', 'O','O','X','X','O'],['s16', 'X','X','O','O','O'],['s17', 'X','O','O','X','O'],['s18', 'O','X','X','X','X'],['s19', 'O','O','X','X','O']]
    # classroom = ClassGroupProblem(['10AM','11AM','12AM','1PM','2PM'], ta, student)
    # print(classroom.domain)
    # #print(classroom.constraints)
    # print(backtracking(classroom,variable_heu = MRV_Group ))

    #test for simple case
    ta = [['t1', 'O','X','O','X'],['t2', 'X','O','X','O'],['t3', 'O','X','O','X']]
    student = [['s1', 'O','X','O','X'],['s2', 'X','O','X','O'],['s3', 'O','X','O','O'],['s4', 'O','O','X','X'],['s5', 'O','O','O','O'],['s6', 'O','X','O','O'],['s7', 'O','X','O','X']]
    random.shuffle(student)
    classroom = ClassGroupProblem(['10AM','11AM','12AM','1PM'], ta, student)
    print(backtracking(classroom))
