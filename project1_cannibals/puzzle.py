#Seungjae Jason Lee
#COSC 76
#Project 1

class PuzzleProblem:
    def __init__(self, start_state):
        #puzzle problem
        self.start_state = start_state
        self.goal_state = tuple([1,2,3,4,5,6,7,8,'x'])
        self.swap_dict =	{
            0: [1,3],
            1: [0,2,4],
            2: [1,5],
            3: [0,4,6],
            4: [1,3,5,7],
            5: [2,4,8],
            6: [3,7],
            7: [4,6,8],
            8: [5,7]
        }

    def swap_tiles(self, state, index1, index2):
        #swaps tile of given index
        new_state = list(state)
        temp = new_state[index1]
        new_state[index1] = new_state[index2]
        new_state[index2] = temp

        return tuple(new_state)

    # get successor states for the given state
    def get_successors(self, state):
        empty_tile_index = state.index('x')
        successor_states = []
        for i in range(len(self.swap_dict[empty_tile_index])):
            successor_states.append(self.swap_tiles(state, empty_tile_index, self.swap_dict[empty_tile_index][i]))
        return successor_states

    #checks if given state is goal state
    def goal_test(self,test_state):
        return test_state == self.goal_state

    def __str__(self):
        string =  "Puzzle Problem: " + str(self.start_state)
        return string
