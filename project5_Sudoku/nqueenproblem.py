#Seungjae Jason Lee
#COSC 76 Project 5
#Propositional Logic
#Feb 11 2019
from SAT import SAT
class nqueenproblem:
    def __init__(self, dimension):
        self.dimension = dimension

    def generate_cnf(self,filename):
        #generates cnf for n queen problem
        f = open(filename, "w")
        string = ""

        for i in range(self.dimension):
            for j in range(self.dimension):
                string += str(i)+str(j)+" "
            string += "\n"

            for j in range(self.dimension):
                string += str(j)+str(i)+" "
            string += "\n"

        #deals with rows and columns
        for i in range(self.dimension):
            for j in range(self.dimension):
                for k in range(j+1, self.dimension):
                    string += "-"+str(i)+str(j)+" -"+str(i)+str(k)+"\n"
                    string += "-"+str(j)+str(i)+" -"+str(k)+str(i)+"\n"

        #diagonal moves
        for i in range(self.dimension): # x coordinate
            for j in range(self.dimension): # y coordinate
                for k in range(self.dimension-1): # k+1: number of diagonal moves 1,2,3 ...
                    if i < self.dimension-1-k and j > k: #checks if moving to right bottom is valid
                        string +=  "-"+str(i)+str(j)+" -"+str(i+k+1)+str(j-k-1)+"\n"
                    if j < self.dimension-1-k and i < self.dimension-1-k: #checks if moving to right top is valid
                        string +=  "-"+str(i)+str(j)+" -"+str(i+k+1)+str(j+k+1)+"\n"
        f.write(string)
        f.close()

    def display_solution(self,filename):
        #displays the result
        f = open(filename,"r")
        queen_location = set()
        for line in f:
            if line[0] != '-':
                queen_location.add((int(line[0]),int(line[1])))

        string = ""
        for j in range(self.dimension):
            j_index = self.dimension - 1- j
            for i in range(self.dimension):
                if (i, j_index) in queen_location:
                    string += "Q"
                else:
                    string += "."
            string += "\n"
        print(string)
        f.close()
if __name__ == "__main__":
    #demonstration for 10*10 board with 10 queens
    q_test = nqueenproblem(10)
    q_test.generate_cnf("test_2.cnf")
    s = SAT("test_2.cnf")
    if s.walksat():
        s.write_solution("test_2.sol")
        #print(len(s.clauses))
        q_test.display_solution("test_2.sol")
