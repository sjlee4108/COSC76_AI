#Seungjae Jason Lee
#Cosc 76 Project 4
#Jan 31 2018
from CircuitBoardProblem import CircuitBoardProblem
from ClassGroupProblem import ClassGroupProblem
from SudokuProblem import SudokuProblem
import backtracking
import time

# print problem
component = [('a',3,8),('b',10,2),('c',6,4),('e',1,8),('x',8,2),('z',4,2)]
circuit = CircuitBoardProblem(component,(10,10))
print(backtracking.backtracking(circuit))

# default: No heuristics
print('\nDefault----------------')
circuit = CircuitBoardProblem(component,(10,10))
start = time.time()
print("number of recursion:",backtracking.backtracking(circuit).counter)
end = time.time()
print("time taken without heuristics: ", end-start)


#Uses MAC-3
print('\nMAC-3------------------')
circuit = CircuitBoardProblem(component,(10,10))
start = time.time()
print("number of recursion:",backtracking.backtracking(circuit,MAC_3 = True).counter)
end = time.time()
print("time taken using MAC_3: ", end-start)

# Uses MRV
print('\nMRV--------------------')
circuit = CircuitBoardProblem(component,(10,10))
start = time.time()
print("number of recursion:",backtracking.backtracking(circuit, variable_heu = backtracking.MRV).counter)
end = time.time()
print("time taken: ", end-start)

#Uses LCV
print('\nLCV--------------------')
circuit = CircuitBoardProblem(component,(10,10))
start = time.time()
print("number of recursion:",backtracking.backtracking(circuit,value_heu = backtracking.LCV).counter)
end = time.time()
print("time taken using LCV: ", end-start)

#Uses AC-3
print('\nAC-3-------------------')
circuit = CircuitBoardProblem(component,(10,10))
start = time.time()
print("number of recursion:",backtracking.backtracking(circuit,AC_3 = True).counter)
end = time.time()
print("time taken using AC-3: ", end-start)
print("")


#For extension testing: testing MRV_Group
ta = [['t1', 'O','X','O','X','O'],['t2', 'X','X','O','O','O'],['t3', 'O','X','X','O','O'],['t4', 'X','O','X','X','O']]
student = [['s1', 'O','X','O','X','O'],['s2', 'X','X','O','O','O'],['s3', 'O','O','X','O','O'],['s4', 'X','O','X','X','X'],['s5', 'O','O','O','O','O'],['s6', 'X','X','X','O','O'],['s7', 'O','X','X','X','O'],['s8', 'O','O','O','X','O'],['s9', 'O','X','O','X','X'],['s10', 'O','X','O','X','O'],['s11', 'O','X','O','O','O'],['s12', 'X','X','X','X','O'],['s13', 'O','X','O','X','X'],['s14', 'O','X','O','O','X'],['s15', 'O','O','X','X','O'],['s16', 'X','X','O','O','O'],['s17', 'X','O','O','X','O'],['s18', 'O','X','X','X','X'],['s19', 'O','O','X','X','O']]
classroom = ClassGroupProblem(['10AM','11AM','12AM','1PM','2PM'], ta, student)
print(backtracking.backtracking(classroom,variable_heu = backtracking.MRV_Group ))

#testing with MRV-Group
print('\nMRV_Group--------------------')
classroom = ClassGroupProblem(['10AM','11AM','12AM','1PM','2PM'], ta, student)
start = time.time()
print("number of recursion:",backtracking.backtracking(classroom,variable_heu = backtracking.MRV_Group ).counter)
end = time.time()
print("time taken using MRV_Group: ", end-start)

#testing without MRV-group
print('\nDefault---------------------')
classroom = ClassGroupProblem(['10AM','11AM','12AM','1PM','2PM'], ta, student)
start = time.time()
print("number of recursion:",backtracking.backtracking(classroom).counter)
end = time.time()
print("time taken without MRV_Group: ", end-start)

#Extension: Testing reducing domain
print("")
sudoku = SudokuProblem([(8,4,0),(7,7,0),(9,8,0),(4,3,1),(1,4,1),(9,5,1),(5,8,1),(6,1,2),(2,6,2),(8,7,2),(7,0,3),(2,4,3),(6,8,3),(4,0,4),(8,3,4),(3,5,4),(1,8,4),(8,0,5),(6,4,5),(3,8,5),
(9,1,6),(8,2,6),(6,7,6),(6,0,7),(1,3,7),(9,4,7),(5,5,7),(5,0,8),(3,1,8),(7,4,8)])
print(backtracking.backtracking(sudoku))

#Sudoku with reduced domain
sudoku = SudokuProblem([(8,4,0),(7,7,0),(9,8,0),(4,3,1),(1,4,1),(9,5,1),(5,8,1),(6,1,2),(2,6,2),(8,7,2),(7,0,3),(2,4,3),(6,8,3),(4,0,4),(8,3,4),(3,5,4),(1,8,4),(8,0,5),(6,4,5),(3,8,5),
(9,1,6),(8,2,6),(6,7,6),(6,0,7),(1,3,7),(9,4,7),(5,5,7),(5,0,8),(3,1,8),(7,4,8)])
start = time.time()
print("number of recursion:",backtracking.backtracking(sudoku).counter)
end = time.time()
print("time taken with Reduced Domain: ", end-start)

#I just commented the part without reduced domain because it takes too long.
# sudoku = SudokuProblem([(8,4,0),(7,7,0),(9,8,0),(4,3,1),(1,4,1),(9,5,1),(5,8,1),(6,1,2),(2,6,2),(8,7,2),(7,0,3),(2,4,3),(6,8,3),(4,0,4),(8,3,4),(3,5,4),(1,8,4),(8,0,5),(6,4,5),(3,8,5),
# (9,1,6),(8,2,6),(6,7,6),(6,0,7),(1,3,7),(9,4,7),(5,5,7),(5,0,8),(3,1,8),(7,4,8)],enable_reduce = False)
# start = time.time()
# backtracking.backtracking(sudoku)
# end = time.time()
# print("time taken without Reduced Domain: ", end-start)
