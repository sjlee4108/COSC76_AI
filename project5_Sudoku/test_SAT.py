#Seungjae Jason Lee
#COSC 76 Project 5
#Propositional Logic
#Feb 11 2019

from SAT import SAT
from display import display_sudoku_solution
import time

print("Testing gsat with one_cell")
s = SAT("one_cell.cnf")
start = time.time()
if s.gsat():
    end = time.time()
    print("Time taken: ",end-start,"(s)")
    s.write_solution("one_cell.sol")
    display_sudoku_solution("one_cell.sol")


# #Commented out because it took too long. GSAT is very expensive
# #It took about 6 minutes to find an answer.
# print("Testing gsat with all_cells")
# s = SAT("all_cells.cnf")
# start = time.time()
# if s.gsat():
#     end = time.time()
#     print("Time taken: ",end-start,"(s)")
#     s.write_solution("all_cells.sol")
#     display_sudoku_solution("all_cells.sol")


print("Testing walksat with one_cell")
s = SAT("one_cell.cnf")
start = time.time()
if s.walksat():
    end = time.time()
    print("Time taken: ",end-start,"(s)")
    s.write_solution("one_cell.sol")
    display_sudoku_solution("one_cell.sol")

print("Testing walksat with all_cells")
s = SAT("all_cells.cnf")
start = time.time()
if s.walksat():
    end = time.time()
    print("Time taken: ",end-start,"(s)")
    s.write_solution("all_cells.sol")
    display_sudoku_solution("all_cells.sol")

print("Testing walksat with rows")
s = SAT("rows.cnf")
start = time.time()
if s.walksat():
    end = time.time()
    print("Time taken: ",end-start,"(s)")
    s.write_solution("rows.sol")
    display_sudoku_solution("rows.sol")

#testing same thing twice to see the time taken
print("Testing walksat with rows_and_cols")
s = SAT("rows_and_cols.cnf")
start = time.time()
if s.walksat():
    end = time.time()
    print("Time taken: ",end-start,"(s)")
    s.write_solution("rows_and_cols.sol")
    display_sudoku_solution("rows_and_cols.sol")

#testing same thing twice to see the time taken
print("Testing walksat with rows_and_cols")
s = SAT("rows_and_cols.cnf")
start = time.time()
if s.walksat():
    end = time.time()
    print("Time taken: ",end-start,"(s)")
    s.write_solution("rows_and_cols.sol")
    display_sudoku_solution("rows_and_cols.sol")

print("Testing walksat with puzzle1")
s = SAT("puzzle1.cnf")
start = time.time()
if s.walksat():
    end = time.time()
    print("Time taken: ",end-start,"(s)")
    s.write_solution("puzzle1.sol")
    display_sudoku_solution("puzzle1.sol")

print("Testing walksat with puzzle2")
s = SAT("puzzle2.cnf")
start = time.time()
if s.walksat():
    end = time.time()
    print("Time taken: ",end-start,"(s)")
    s.write_solution("puzzle2.sol")
    display_sudoku_solution("puzzle2.sol")

print("Testing walksat with puzzle_bonus")
s = SAT("puzzle2.cnf")
start = time.time()
if s.walksat():
    end = time.time()
    print("Time taken: ",end-start,"(s)")
    s.write_solution("puzzle_bonus.sol")
    display_sudoku_solution("puzzle_bonus.sol")
else:
    end = time.time()
    print("Time taken(no solution): ",end-start,"(s)")

#extension: proving simple logic case
s = SAT("resolve.cnf")
print("Resolution Testing")
print("KnowledgeBase: P V Q, P -> R, Q -> R")
print("Prove: R is True")
print("Result of resolution with clause [R]: ",s.resolution(set(["R"])))

#extension: proving wumpus example
s = SAT("resolve_2.cnf")
print("Resolution Testing")
print("KnowledgeBase: B(1,1) <=> P(1,2) ∨ P(2,1) and -B(1,1)")
print("Prove: -P(1,2) is True")
print("Result of resolution with clause [-P12]: ",s.resolution(set(["-P12"])))
