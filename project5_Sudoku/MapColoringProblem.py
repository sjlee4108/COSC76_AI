#Seungjae Jason Lee
#COSC 76 Project 5
#Propositional Logic
#Feb 11 2019
from SAT import SAT
class MapColoringProblem:
    def __init__(self,locations, neighbors, colors):
        #takes list of string of locations, list of tuples of neighbors and list of colors
        self.locations = locations
        self.neighbors = neighbors
        self.colors = colors

    def generate_cnf(self,filename):
        #generates cnf for the map problem and makes a cnf file.
        f = open(filename, "w")
        str = ""
        for i in range(len(self.locations)):
            for j in range(len(self.colors)):
                str += self.locations[i]+"_"+self.colors[j]+" "
            str += "\n"
        for location in self.locations:
            for i in range(len(self.colors)):
                for j in range(i+1, len(self.colors)):
                    str += "-"+location+"_"+self.colors[i]+" -"+location+"_"+self.colors[j]+"\n"

        for color in self.colors:
            for n in self.neighbors:
                str += "-"+n[0]+"_"+color+" -"+n[1]+"_"+color+"\n"
        f.write(str)
        f.close()

    def display_solution(self,filename):
        #displays solution based on the given solution file. 
        f = open(filename,"r")
        for line in f:
            if line[0] != '-':
                print(line)
        f.close()
if __name__ == "__main__":
    MCP_test = MapColoringProblem(["WA","NT","SA","Q","NSW","V","T"],[("WA","NT"),("WA","SA"),("SA","Q"),("SA","NSW"),("SA","V"),("NT","Q"),("Q","NSW"),("NSW","V"),("SA","NT")],['r','g','b'])
    MCP_test.generate_cnf("test.cnf")
    s = SAT("test.cnf")
    s.walksat()
    s.write_solution("test.sol")
    MCP_test.display_solution("test.sol")
