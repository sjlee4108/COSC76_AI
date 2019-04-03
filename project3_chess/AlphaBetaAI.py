#Seungjae Jason Lee
#Cosc 76 Project 3
#Jan 24 2019

import chess
import math
import random
from chess import Move
from BoardState import BoardState
import time
class AlphaBetaAI():
    #AI that uses alpha beta pruning
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
        self.open_book = [[Move.from_uci('a2a4'),Move.from_uci('b2b3'),Move.from_uci('d2d3'),Move.from_uci('e2e4'),Move.from_uci('f2f3'),Move.from_uci('h2h3')],[Move.from_uci('a7a5'),Move.from_uci('b7b6'),Move.from_uci('d7d6'),Move.from_uci('e7e5'),Move.from_uci('f7f6'),Move.from_uci('h7h6')]]
        self.use_openbook = False #True  #Set this to true to use it
        self.counter = 0
        pawn = [0,0,0,0,0,0,0,0,0.5,1.0,1.0,-2.0,-2.0,1.0,1.0,0.5,0.5,-0.5,-1.0,0.0,0.0,-1.0,-0.5,0.5,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.5,0.5,1.0,2.5,2.5,1.0,0.5,0.5,1.0,1.0,2.0,3.0,3.0,2.0,1.0,1.0,5.0,5.0,5.0,5.0,5.0,5.0,5.0,5.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0]
        knight = [-5.0,-4.0,-3.0,-3.0,-3.0,-3.0,-4.0,-5.0,-4.0,-2.0,0.0,0.5,0.5,0.0,-2.0,-4.0,-3.0,0.5,1.0,1.5,1.5,1.0,0.5,-3.0,-3.0,0.0,1.5,2.0,2.0,1.5,0.0,-3.0,-3.0,0.5,1.5,2.0,2.0,1.5,0.5,-3.0,-3.0,0.0,1.0,1.5,1.5,1.0,0.0,-3.0,-4.0,-2.0,0.0,0.0,0.0,0.0,-2.0,-4.0,-5.0,-4.0,-3.0,-3.0,-3.0,-3.0,-4.0,-5.0]
        bishop = [-2.0,-1.0,-1.0,-1.0,-1.0,-1.0,-1.0,-2.0,-1.0,0.5,0.0,0.0,0.0,0.0,0.5,-1.0,-1.0,1.0,1.0,1.0,1.0,1.0,1.0,-1.0,-1.0,0.0,1.0,1.0,1.0,1.0,0.0,-1.0,-1.0,0.5,0.5,1.0,1.0,0.5,0.5,-1.0,-1.0,0.0,0.5,1.0,1.0,0.5,0.0,-1.0,-1.0,0.0,0.0,0.0,0.0,0.0,0.0,-1.0,-2.0,-1.0,-1.0,-1.0,-1.0,-1.0,-1.0,-2.0]
        rook = [0.0,0.0,0.0,0.5,0.5,0.0,0.0,0.0,-0.5,0.0,0.0,0.0,0.0,0.0,0.0,-0.5,-0.5,0.0,0.0,0.0,0.0,0.0,0.0,-0.5,-0.5,0.0,0.0,0.0,0.0,0.0,0.0,-0.5,-0.5,0.0,0.0,0.0,0.0,0.0,0.0,-0.5,-0.5,0.0,0.0,0.0,0.0,0.0,0.0,-0.5,0.5,1.0,1.0,1.0,1.0,1.0,1.0,0.5,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0]
        queen = [-2.0,-1.0,-1.0,-0.5,-0.5,-1.0,-1.0,-2.0,-1.0,0.0,0.5,0.0,0.0,0.0,0.0,-1.0,-1.0,0.5,0.5,0.5,0.5,0.5,0.0,-1.0,0.0,0.0,0.5,0.5,0.5,0.5,0.0,-0.5,-0.5,0.0,0.5,0.5,0.5,0.5,0.0,-0.5,-1.0,0.0,0.5,0.5,0.5,0.5,0.0,-1.0,-1.0,0.0,0.0,0.0,0.0,0.0,0.0,-1.0,-2.0,-1.0,-1.0,-0.5,-0.5,-1.0,-1.0,-2.0]
        king = [2.0,3.0,1.0,0.0,0.0,1.0,3.0,2.0,2.0,2.0,0.0,0.0,0.0,0.0,2.0,2.0,-1.0,-2.0,-2.0,-2.0,-2.0,-2.0,-2.0,-1.0,-2.0,-3.0,-3.0,-4.0,-4.0,-3.0,-3.0,-2.0,-3.0,-4.0,-4.0,-5.0,-5.0,-4.0,-4.0,-3.0,-3.0,-4.0,-4.0,-5.0,-5.0,-4.0,-4.0,-3.0,-3.0,-4.0,-4.0,-5.0,-5.0,-4.0,-4.0,-3.0,-3.0,-4.0,-4.0,-5.0,-5.0,-4.0,-4.0,-3.0]
        #print(len(pawn),len(knight),len(bishop),len(rook),len(queen),len(king))
        self.location_weight_book = [pawn, knight, bishop, rook, queen, king]

    def choose_move_ids(self,board,depth):
        #uses iterative deepening search with given depth
        best_move = None
        init_depth = self.depth
        for i in range(depth):
            self.depth = i+1
            best_move = self.choose_move_fn(board)
        self.depth = init_depth
        return best_move

    def choose_move_fn(self, board):
        # the method that actually does alpha beta pruning
        start = time.time()
        self.turn = board.turn
        [value,action] = self.Max_value(board,-math.inf, math.inf,0)
        print("AB AI: "+str(self.depth)+" recommending move " + str(action))
        end = time.time()
        print("number of function calls :" + str(self.counter))
        print("time taken: "+ str(end-start))
        self.counter = 0
        return action

    def choose_move(self,board):
        #returns the best move
        #for ids, use self.choose_move_ids
        #for regular, use self.choose.move_fn
        self.turn = board.turn
        if self.use_openbook == True:
            if self.turn == True and self.open_book[0] != []:
                move = self.open_book[0][0]
                self.open_book[0].pop(0)
                return move
            elif self.turn == False and self.open_book[1] != []:
                move = self.open_book[0][0]
                self.open_book[0].pop(0)
                return move
        #return self.choose_move_fn(board)
        return self.choose_move_ids(board,self.depth)


    def Max_value(self,board, a,b,count):
        #returns the max value of its children states
        self.counter += 1
        action = None
        if self.cutoff_test(board, count):
            if BoardState(board) not in self.value_dictionary.keys():
                return [self.evaluation(board,count+1),action]
            else:
                return [self.value_dictionary[BoardState(board)],action]
        value = -math.inf
        #moves = self.advanced_move_ordering(board,list(board.legal_moves),True )
        moves = list(board.legal_moves)
        for move in moves:
            board.push(move)
            old_value = value
            value = max(value, self.Min_value(board, a,b,count+1)[0])
            if old_value != value:
                action = move
            board.pop()
            if value >= b:
                return [value,action]
            a= max(a,value)
        return [value,action]

    def Min_value(self,board,a,b, count):
        #returns the min value of its children states
        self.counter += 1
        action = None
        if self.cutoff_test(board, count):
            if BoardState(board) not in self.value_dictionary.keys():
                return [self.evaluation(board,count+1),action]
            else:
                return [self.value_dictionary[BoardState(board)],action]
        value = math.inf
        #moves = self.advanced_move_ordering(board,list(board.legal_moves),False )
        moves = list(board.legal_moves)
        for move in moves:
            board.push(move)
            old_value = value
            value = min(value, self.Max_value(board, a,b,count+1)[0])
            if old_value != value:
                action = move
            board.pop()
            if value <= a:
                return [value,action]
            b = min(b,value)
        return [value, action]

    def cutoff_test(self,board, count):
        #base case for the tree search
        #checks if the tree should stop going deeper
        if board.is_game_over() == True or self.depth == count:
            return True
        return False

    def evaluation(self, board,depth):
        #returns the heuristic value of the board
        value = 0
        if board.is_checkmate():
            if board.turn == self.turn:
                value -= self.pieces_weight[6]/depth
            else:
                value += self.pieces_weight[6]/depth
        #<Old Implementation: modified through profiling>
        # for i in range(64):
        #     board_piece = board.piece_at(i)
        #     if board_piece != None:
        #         if board_piece.color == self.turn :
        #             value += self.pieces_weight[board_piece.piece_type]
        #         else:
        #             value -= self.pieces_weight[board_piece.piece_type]

        #new implementation
        piece_dict = board.piece_map()
        for location in piece_dict:
            piece = piece_dict[location]
            if piece.color == self.turn :
                value += self.pieces_weight[piece.piece_type]
                value += self.location_weight_book[piece.piece_type-1][location]
            else:
                value -= self.pieces_weight[piece.piece_type]
                value -= self.location_weight_book[piece.piece_type-1][31-(location-32)]
        if board.is_checkmate() == False:
            #since checkmate heuristic differs depending on the depth, dont save them
            self.value_dictionary[BoardState(board)] = value
        return value

    def random_move_ordering(self,move):
        #random sorting
        return random.shuffle(move)

    def advanced_move_ordering(self,board,move,order):
        #extension, sort based on evaluation values
        value = 0
        if order == True:
            value = - math.inf
        else:
            value = math.inf
        for i in range(len(move)):
            board.push(move[i])
            board_obj = BoardState(board)
            if board_obj not in self.value_dictionary.keys():
                    move[i] = tuple((move[i], value))
            else:
                    move[i] = tuple((move[i], self.value_dictionary[board_obj]))
            board.pop()
        move.sort(key = get_second,reverse = order)

        for i in range(len(move)):
            move[i] = move[i][0]
        return move

def get_second(value):
    #function used for sorting
    return value[1]

if __name__ == "__main__":
    board = chess.Board("6R1/8/8/7k/8/6Q1/8/K7 b KQkq - 0 4")
    board.push(list(board.legal_moves)[0])
    player = AlphaBetaAI(6)
    print(player.choose_move(board))
    print(player.evaluation(board,1))
    print(board)
    # for move in list(board.legal_moves):
    #    board.push(move)
    #    print(move,player.evaluation(board))
    #    print(board)
    #    board.pop()

    board.push(chess.Move.from_uci("g8g7"))
    print(board)
    print(player.evaluation(board,1))
