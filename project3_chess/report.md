# COSC 76 Project 3: Chess
### Seungjae Jason Lee



## Introduction

#####Objective 
There are two main objectives to the project. First, we want to implement Minimax search THen, we want to implement Alpah Beta Pruning. Using these two different searches, we can build a AI that plays chess.

#####Game Rule 
THe game rule is basic chess rule.  


## Code Design/ Building the Model
For this project, we are given python chess to build our problem state. As for displaying the actual game, Professor has provided us with the sample, which we could modify. Thus, we just need to focus on implementing algorithms. 

## Minimax and Cutoff Test

First, I implemented cutoff_test, which checks two different conditions: search reaching maximum depth, and search reaching terminal state. It returns true if any of two conditions hold and false otherwise. 

Then, I wrote Min_value and Max_value methods based on the pseudo-code from our textbook. 

For the observation, I noticed that the number of functional calls are exponentially increasing as the depth limit increases

![Demo](/Users/SJLEE/Desktop/cosc\ 76/cslib3/IDS_DEMO.png )



## Evaluation

**Discussion:** For the evaluation function, I gave material value to pieces. For pawn, I gave 1. For bishop and knight, I gave 3. For Rook, I gave 5. For queen, 9 and, for king, I gave an arbitarily big number. Then, for the evaluation function, I subtracted weighted sum of oppoent's pieces from ym weighted sum of pieces. Thus, having a positive large evaluation value would mean the game is more advantageous for the AI while negative number would mean more advantageous state for the opponent. 


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

## IDS for Minimax
Since there are time limits for the actual chess game, I used IDS to find different possible solutions and return the best move. I basically used Minimax search and changed the depth for each function call. 

**Discussion:** I noticed that the optimal choice did change as the depth was deeper. However, the number of minimax function calls rose exponentially as IDS increased the depth limit. Also, given same amout of time, I noticed that IDS Minimax and Minimax in general cannot go deeper in compared to Alpha Beta Pruning.

![Demo](/Users/SJLEE/Desktop/cosc\ 76/cslib3/IDS_DEMO.png )


	def choose_move_ids(self,board,depth):
        best_move = None
        init_depth = self.depth
        for i in range(depth-1):
            self.depth = i+1
            best_move = self.choose_move(board)
        self.depth = init_depth
        return best_move


## Alpha Beta Pruning
For alpha beta pruning, I used the pseudocode from the textbook and implemented the algorithm. After completing implementation, I compared two different searches. Given depth of 3, I checked to see if MiniMaxAI provides the same move as AlphaBeta.

**Test:**  After completing implementation, I compared two different searches. Given depth of 3, I checked to see if MiniMaxAI provides the same move as AlphaBeta. To test it, I had both AIs play against the "random" player (gives random but same moves for both players) and see if they reach same state of the board. The first one is with Minimax and the second one is with Alpha Pruning. We see that they both reached same state of the board at certain time although alpha pruning reached the state much faster. 

![Demo](/Users/SJLEE/Desktop/cosc\ 76/cslib3/Minimax.png )
![Demo](/Users/SJLEE/Desktop/cosc\ 76/cslib3/AlphaBeta.png )



AB made an extra move with rook because I could not screenshot at the right time! (Thats how fast the AI was compared to Minimax)

## Transposition Table

For this section, I implemeted transposition table by using dictionary. Whenever cutoff test is true, the algorithm finds the evaluation value for the given board state. To avoid repetition of evaluating same boards, I used dictionary and saved the board's value. Since dictionary requires hashable object, I had to wrap a board state with a class and override hash function. I used overrode hash method by returning hash(str(board)) instead.

 **Test:** From the starting chess state, I tried alpha pruning with depth 6 with transposition table and without transposition table. Then, I was able to observe how transposition table can save a big chunk of time if the tree is big. Picture of the result is shown below.
 
 ![Demo](/Users/SJLEE/Desktop/cosc\ 76/cslib3/Transposition.png )

### Extension

	
**Extension 1:**
 For the extension, I did profiling to improve my search. By timing different functions, I figured that my evaluation is time consuming. Thus, I searched python chess documentation to find reduce evaluation method time. Then, I noticed that chess.board.piece_map() provides dictionary of locations and pieces. Thus, instead of iterating over the whole board to count pieces, counting over the dictionary was more efficient. The image below shows the result of two different evaluation functions. First one is the result of old evaluation and the second one is the result of new evaluation function. Old version is commented out. 
 ![Demo](/Users/SJLEE/Desktop/cosc\ 76/cslib3/Extension1.png )
 
**Extension 2:**
For the second extension, I tried to improve the heuristic function. One of the problems for the material heuristic is that it generalizes too much and often does not provide good comparison especially if none of the pieces are captured. To improve the heuristic, I used a chart from online that adds value for pieces depending on the location of pieces. The chart is shown below. AI with the chart and witout the chart both played the game but the chart one did reach checkmate faster although some moves were strange. In conclusion, although this is better, it is still not the best heuristic. 

![Demo](/Users/SJLEE/Desktop/cosc\ 76/cslib3/chart.png )

In the video new_heuristic, randomAi plays against AlphaBetaAI with depth of 4. The first one uses improved heuristic and wins the game in a minute while the second one that uses material heuristic wins the game in two minutes. In the video, we can clear see that second heuristic makes more threatening moves instead of making repetitive wasteful moves. 
	
**Extension 3:**
 For this extension, I improved heuristic so that my search would find checkmate faster. Prevously, whenever checkmate occurs, I gave +/- 1000000 to the evaluation value. However, I noticed that the search algorithm does not necessary choose the fastest checkmate with my improved heuristic. Since my new heuristic evaluates location as well, I noticed that such factor distracts the algorithm from finding the fastest checkmate. Thus, instead, I give 1000000/current_depth so that my algorithm would find the fastest checkmate. Demonstration is shown in a video extension3. 
 
 **Extension 4:**
 For this extension, I used advanced sorting for IDS. For any board states with evaluated values, I placed them at the front or back (sorted) depending on we are looking for max or min. However, it did not reduce down the time but increased but a lot when I tried with the starting state of the game. So, I think using advanced sorting is really inefficient when there arent "active capture moves" in the board but moving pieces without much changes in value. Thus, sorting would still consume time while it is not really sorting. So, for further study, I think it would be nice to find when to use advanced sorting vs when to not use it. method: advanced_move_reordering
 
 *Not Sorted*
 ![Demo](/Users/SJLEE/Desktop/cosc\ 76/cslib3/Sort.png )
 
 *Sorted*
  ![Demo](/Users/SJLEE/Desktop/cosc\ 76/cslib3/noSort.png )
 
**Extension 5:**
For this extension, I made a very simple open book that uses "pawns" first. The picture is shown below as well as video demonstration. To use the book, set self.use-open-book to True in AlphaBeta object.
![Demo](/Users/SJLEE/Desktop/cosc\ 76/cslib3/openbook.png )