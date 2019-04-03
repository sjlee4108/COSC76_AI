#Seungjae Jason Lee (Written by Professor Devin)
#COSC 76 Project 5
#Propositional Logic
#Feb 11 2019
from Sudoku import Sudoku
import sys

if __name__ == "__main__":
    test_sudoku = Sudoku()

    test_sudoku.load(sys.argv[1])
    print(test_sudoku)

    puzzle_name = sys.argv[1][:-4]
    cnf_filename = puzzle_name + ".cnf"

    test_sudoku.generate_cnf(cnf_filename)
    print("Output file: " + cnf_filename)
