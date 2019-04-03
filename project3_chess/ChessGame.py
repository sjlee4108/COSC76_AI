#Seungjae Jason Lee
#Cosc 76 Project 3
#Jan 24 2019
import chess


class ChessGame:
    def __init__(self, player1, player2):
        #self.board = chess.Board("6R1/8/8/7k/8/6Q1/8/K7 b KQkq - 0 4")
        self.board = chess.Board()
        self.players = [player1, player2]

    def make_move(self):

        player = self.players[1 - int(self.board.turn)]
        move = player.choose_move(self.board)
        if move == None:
            print("checkmate!! or game over?!?!")
            return False
        self.board.push(move)  # Make the move

    def is_game_over(self):
        return self.board.is_game_over()

    def __str__(self):

        column_labels = "\n----------------\na b c d e f g h\n"
        board_str =  str(self.board) + column_labels

        # did you know python had a ternary conditional operator?
        move_str = "White to move" if self.board.turn else "Black to move"

        return board_str + "\n" + move_str + "\n"
