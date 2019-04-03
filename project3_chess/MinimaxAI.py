#Seungjae Jason Lee
#Cosc 76 Project 3
#Jan 24 2019
import chess
import math
from BoardState import BoardState
class MinimaxAI():
    def __init__(self,depth):
        self.depth = depth
        self.pieces_weight = {
            1:1,
            2:3,
            3:3,
            4:5,
            5:9,
            6:1000000
        }
        self.value_dictionary = {}
        self.counter = 0

    def choose_move(self,board):
        #return self.choose_move_fn(board)
        return self.choose_move_ids(board,self.depth)
    def choose_move_fn(self, board):
        self.turn = board.turn
        value = -math.inf
        action = None
        for move in list(board.legal_moves):
            board.push(move)
            move_value = self.Min_value(board, 0)
            if (move_value >  value):
                value = move_value
                action = move
            board.pop()
        print("Mini AI: "+str(self.depth)+ " recommending move " + str(action))
        print("Mini AI function calls: " + str(self.counter) )
        self.counter = 0
        return action

    def choose_move_ids(self,board,depth):
        best_move = None
        init_depth = self.depth
        for i in range(depth):
            self.depth = i
            best_move = self.choose_move_fn(board)
        self.depth =init_depth
        return best_move

    def Max_value(self,board, count):
        self.counter += 1
        if self.cutoff_test(board, count):
            if BoardState(board) not in self.value_dictionary.keys():
                return self.evaluation(board)
            else:
                return [self.value_dictionary[BoardState(board)],action]
        value = -math.inf
        for move in list(board.legal_moves):
            board.push(move)
            value = max(value, self.Min_value(board, count+1))
            board.pop()
        return value

    def Min_value(self,board, count):
        self.counter += 1
        if self.cutoff_test(board, count):
            if BoardState(board) not in self.value_dictionary.keys():
                return self.evaluation(board)
            else:
                return [self.value_dictionary[BoardState(board)],action]
        value = math.inf
        for move in list(board.legal_moves):
            board.push(move)
            value = min(value, self.Max_value(board, count+1))
            board.pop()
        return value

    def cutoff_test(self,board, count):
        if self.depth == count or board.is_game_over() == True:
            return True
        return False

    def evaluation(self, board):
        value = 0
        if board.is_checkmate():
            if board.turn == self.turn:
                value -= self.pieces_weight[6]
            else:
                value += self.pieces_weight[6]
        for i in range(64):
            board_piece = board.piece_at(i)
            if board_piece != None:
                if board_piece.color == self.turn :
                    value += self.pieces_weight[board_piece.piece_type]
                else:
                    value -= self.pieces_weight[board_piece.piece_type]
        return value
