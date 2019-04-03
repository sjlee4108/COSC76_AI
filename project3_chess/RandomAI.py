#Seungjae Jason Lee
#Cosc 76 Project 3
#Jan 24 2019
#import chess
import random
from time import sleep

class RandomAI():
    def __init__(self):
        pass

    def choose_move(self, board):
        moves = list(board.legal_moves)
        if len(moves)==0:
            return None
        move = random.choice(moves)
        sleep(1)   # I'm thinking so hard.
        print("Random AI recommending move " + str(move))
        return move
