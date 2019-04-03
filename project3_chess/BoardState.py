#Seungjae Jason Lee
#Cosc 76 Project 3
#Jan 24 2019
class BoardState():
    #takes the board object and saves its string
    def __init__(self, board):
        self.board_str = str(board)

    #returns the hash of board string
    def __hash__(self):
        return hash(self.board_str)
