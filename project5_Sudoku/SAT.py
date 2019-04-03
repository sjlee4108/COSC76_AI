#Seungjae Jason Lee
#COSC 76 Project 5
#Propositional Logic
#Feb 11 2019

import random
import time
import copy
class SAT:
    def __init__(self, filename):
        #initializes the problem by building necessary dictionaries, clauses and default assignment.
        self.clauses = []
        self.value_to_index = {}
        self.index_to_value = {}
        self.iteration = 100000
        self.assignment = []
        self.build_problem(filename)
        self.random_assignment()

    def build_problem(self, filename):
        #helper function for initialization, takes a filename for cnf.
        #builds dictionaries and clauses, and also initializes assignment.
        f = open(filename, "r")
        count = 1
        for line in f:
            clause = []
            for s in line.split():
                if s[0] == "-":
                    if s[1:] not in self.value_to_index.keys():
                        #read a new variable not defined before
                        self.value_to_index[s[1:]] = count
                        self.index_to_value[count] = s[1:]
                        count += 1
                        self.assignment.append(None)
                    clause.append(-self.value_to_index[s[1:]]) #adds the atom to clause
                else:
                    if s not in self.value_to_index.keys():
                        #read a bew variable not defined before
                        self.value_to_index[s] = count
                        self.index_to_value[count] = s
                        count += 1
                        self.assignment.append(None)
                    clause.append(self.value_to_index[s]) # adds the atom to clause
            self.clauses.append(set(clause)) #adds the whole clause into a list of clauses

    def random_assignment(self):
        #assigns random values (T or F) for each variable in self.assignment
        for i in range(len(self.assignment)):
            if random.random() < 0.5:
                self.assignment[i] = True
            else:
                self.assignment[i] =  False

    def check_clauses(self):
        #checks if all clauses are satisfied with current self.assignment
        for clause in self.clauses:
            bool = False # False if the clause is not satisfied. Else, True
            for atom in clause:
                if atom > 0:
                    if self.assignment[atom-1]:
                        #current atom is True -> so the whole clause is True
                        bool =  True
                        break
                else:
                    if self.assignment[abs(atom)-1] == False:
                        #current atom is True -> so the whole clause is True
                        bool = True
                        break
            if bool == False: # Current clause is not satisfied
                return False
        return True # All clauses were satisfied

    def count_sat_clauses(self,index):
        count = 0
        self.assignment[index] = not self.assignment[index] # flips the value at given index
        for clause in self.clauses:
            for atom in clause:
                if atom > 0: #positive
                    if self.assignment[atom-1]:
                        #clauses is satisfied if one of the atom is satisfied
                        count += 1
                        break
                else: #negate case
                    if self.assignment[abs(atom)-1] == False:
                        #clauses is satisfied if one of the atom is satisfied
                        count += 1
                        break
        self.assignment[index] = not self.assignment[index] # returns back to originial state
        return count

    def gsat(self):
        #uses GSAT random walk to solve the problem
        #returns True if the problem is solved within limited iterations
        #returns False if no solution is found.
        count = 0
        while count <= self.iteration:
            count += 1
            if self.check_clauses():
                #found the solution
                return True
            rand_index = random.randint(0,len(self.assignment)-1)
            if random.random() > 0.7:
                #if higher than threshold, flips random position
                self.assignment[rand_index] = not self.assignment[rand_index]
            else:
                #chooses the variable that has most clauses satisifed if flipped and flips that variable
                max = -1
                highest_list = []
                for i in range(len(self.assignment)):
                    clause_count = self.count_sat_clauses(i)
                    if clause_count > max:
                        max = clause_count
                        highest_list = [i]
                    elif clause_count == max:
                        highest_list.append(i)
                rand_index = random.choice(highest_list)
                self.assignment[rand_index] = not self.assignment[rand_index]
        return False

    def walksat(self):
        #modified version of GSAT
        #returns True if walksat finds a solution
        #returns False otherwise
        #instead of checking satisfied clauses for all variables like gsat,
        #choose randomly a variable from one of the unsatisfied clauses.
        count = 0
        while count <= self.iteration:
            count += 1
            if self.check_clauses(): #found an answer
                return True

            #For debugging --> shows how many iteration happened at some stage
            #if count % 10000 == 0:
            #    print("iteration: ",count)

            rand_index = random.randint(0,len(self.assignment)-1)
            if random.random() > 0.7:
                self.assignment[rand_index] = not self.assignment[rand_index]
            else:
                #finding all indices of clauses that are unsatisfied with current self.assignment
                unsat_clauses_indices = []
                for i in range(len(self.clauses)):
                    bool =  False
                    for atom in self.clauses[i]:
                        if atom > 0:
                            if self.assignment[atom-1]:
                                bool =  True
                                break
                        else:
                            if self.assignment[abs(atom)-1] == False:
                                bool = True
                                break
                    if bool == False:
                        unsat_clauses_indices.append(i)

                #choose random clause among unsatisfied clauses
                rand_clause_index = random.choice(unsat_clauses_indices)

                #find variables with highest number of satisfied clauses if flipped
                max = -1
                highest_list = []
                for i in self.clauses[rand_clause_index]:
                    clause_count = self.count_sat_clauses(abs(i)-1)
                    if clause_count > max:
                        max = clause_count
                        highest_list = [abs(i)-1]
                    elif clause_count == max:
                        highest_list.append(abs(i)-1)
                rand_index = random.choice(highest_list) #choose a variable randomly
                self.assignment[rand_index] = not self.assignment[rand_index] #flips the chosen one

    def resolution(self, clause):
        #Extension: checks if given clause is True with current self.clauses(knowledge base), returns True or False
        #Takes a clause in a set. Must be stored as a string format not index format.
        #Example: clause = set(["-R"])
        neg_clause = set()
        for atom in clause:
            if atom[0] == "-":
                neg_clause.add(self.value_to_index[atom[1:]])
            else:
                neg_clause.add(-self.value_to_index[atom])
        clauses = self.clauses + [neg_clause]
        new = []
        while True:
            #print(clauses)
            for i in range(len(clauses)):
                for j in range(i+1,len(clauses)):
                    #print("before",clauses[i], clauses[j])
                    resolvent = self.resolve(copy.copy(clauses[i]), copy.copy(clauses[j])) #finds resolution of two clauses
                    #print(resolvent)
                    #time.sleep(0.3)
                    if len(resolvent) == 0 and (clauses[i] == neg_clause or clauses[j] == neg_clause): #checks if the resolution is empty
                        return True

                    if resolvent not in new: #adds the new resolution clause
                        new =  new + [resolvent]

            #checks if "new" clause actually has new clauses
            #if so, updates the new clauses to existing clauses.
            #if not, returns False
            bool = True
            for clause in new:
                if clause not in clauses:
                    bool =  False
                    break
            if bool:
                return False

            clauses = clauses + new

    def resolve(self, clause1, clause2):
        #helper function for resolution method
        #takes two clauses and makes them into one using resolution rule.
        new_clause = clause1
        moved = False
        for atom in clause2:
            #print(new_clause)
            if atom < 0:
                if moved == False and abs(atom) in new_clause:
                    moved = True
                    new_clause.remove(abs(atom))
                elif moved == True and abs(atom) in new_clause:
                    return set()
                else:
                    new_clause.add(atom)
            else:
                if moved == False and -atom in new_clause:
                    moved = True
                    new_clause.remove(-atom)
                elif moved == True and -atom in new_clause:
                    return set()
                else:
                    new_clause.add(atom)
        return new_clause

    def write_solution(self, filename):
        #writes solution by reading given solution file.
        f = open(filename, "w")
        for i in range(len(self.assignment)):
            if self.assignment[i]:
                f.write(self.index_to_value[i+1]+"\n")
            else:
                f.write("-"+self.index_to_value[i+1]+"\n")

if __name__ == "__main__":
    pass
    # s = SAT("one_block.cnf")
    # print(s.resolution(set(["115"])))
    # if s.walksat():
    #     print(s.assignment)
    #     print(s.index_to_value)
    # print(s.resolution(set(["-R"])))
    #print(s.resolve(set([3, 4, 5, 6, 7, 8, 9]), set([-1, -2])))

    # s = SAT("resolve_2.cnf")
    # if s.walksat():
    #     print(s.assignment)
    #     print(s.index_to_value)
    # print(s.resolution(set(["-P12"])))

    # s = SAT("resolve.cnf")
    # if s.walksat():
    #     print(s.assignment)
    #     print(s.index_to_value)
    # print(s.resolution(set(["-R"])))
