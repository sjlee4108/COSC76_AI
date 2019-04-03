#Seungjae Jason Lee
#COSC 76
#Project 1
class CannibalProblem:
    def __init__(self, start_state=(3, 3, 1), boat_max = 2):
        self.start_state = start_state
        self.goal_state = (0, 0, 0)
        self.total_miss = self.start_state[0]
        self.total_cann = self.start_state[1]
        self.boat_max = boat_max

    # get successor states for the given state
    def get_successors(self, state):
        successor_states = []
        if self.goal_test(state):
            return sucessor_states
        if state[2] == 1:
            # moving to right side of the river
            for i in range(self.boat_max):
                ppl_in_boat = i+1 # number of people moving in the boat
                successor_states += self.build_successors(state,ppl_in_boat)
        else:
            #moving to left side of the river
            for i in range(self.boat_max-1):
                ppl_in_boat = i+1 # number of people moving in the boat
                successor_states += self.build_successors(state,ppl_in_boat)
        return successor_states

    # get legal successors for given state
    def build_successors(self, state, boat_cap):
        successor_states = []
        boat_location = state[2]
        for i in range(boat_cap +1):
            moving_miss = i
            moving_cann = boat_cap - i
            if boat_location == 1:
                new_state = (state[0]-moving_miss, state[1]-moving_cann,0)
            else:
                new_state = (state[0]+moving_miss, state[1]+moving_cann,1)
            if self.legal_state(new_state) and new_state[0] >= 0 and new_state[1] >= 0 and new_state[0] <= self.start_state[0] and new_state[1] <= self.start_state[1]:
                successor_states.append(new_state)
        return successor_states
    def legal_state(self, state):
        return (state[0] >= state[1] or state[0] == 0) and (self.total_miss-state[0] >= self.total_cann-state[1] or self.total_miss-state[0] == 0)

    def goal_test(self,test_state):
        return test_state == self.goal_state
    def __str__(self):
        string =  "Missionaries and cannibals problem: " + str(self.start_state)
        return string


## A bit of test code

if __name__ == "__main__":
    test_cp = CannibalProblem((5, 5, 1),boat_max=3)
    print(test_cp.get_successors((3,3,1)))
