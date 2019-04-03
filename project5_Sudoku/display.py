#Seungjae Jason Lee (Written by Professor Devin)
#COSC 76 Project 5
#Propositional Logic
#Feb 11 2019

from Sudoku import Sudoku
import sys

def display_sudoku_solution(filename):

    test_sudoku = Sudoku()
    test_sudoku.read_solution(filename)
    print(test_sudoku)

if __name__ == "__main__":
    display_sudoku_solution(sys.argv[1])
