from SearchSolution import SearchSolution
from heapq import heappush, heappop

class AstarNode:
    # each search node except the root has a parent node
    # and all search nodes wrap a state object

    def __init__(self, state, heuristic, parent=None, transition_cost=0):
        # you write this part
        self.parent = parent
        self.state = state
        self.heuristic = heuristic
        self.transition_cost = transition_cost

    def priority(self):
        # you write this part
        return self.heuristic + self.transition_cost

    def get_cost(self):
        return self.transition_cost

    def get_state(self):
        return self.state
    # comparison operator,
    # needed for heappush and heappop to work with AstarNodes:
    def __lt__(self, other):
        return self.priority() < other.priority()


# take the current node, and follow its parents back
#  as far as possible. Grab the states from the nodes,
#  and reverse the resulting list of states.
def backchain(node):
    result = []
    current = node
    while current:
        result.append(current.state)
        current = current.parent

    result.reverse()
    return result


def astar_search(search_problem, heuristic_fn):
    # I'll get you started:
    start_node = AstarNode(search_problem.start_state, heuristic_fn(search_problem.start_state))
    pqueue = []
    heappush(pqueue, start_node)

    solution = SearchSolution(search_problem, "Astar with heuristic " + heuristic_fn.__name__)

    visited_cost = {}
    visited_cost[start_node.state] = 0
    while(pqueue != []):
        node = heappop(pqueue)
        solution.nodes_visited += 1
        successors = search_problem.get_successors(node.get_state())

        if search_problem.goal_test(node.get_state()):
            if solution.get_cost() == 0 or (solution.get_cost() != 0 and solution.get_cost() > visited_cost[node.get_state()]):
                solution.set_path(backchain(node))
                solution.set_cost(visited_cost[node.get_state()])
        if solution.get_cost() < visited_cost[node.get_state()] and len(solution.get_path()) != 0:
            break
        for i in range(len(successors)):
            successor_cost = search_problem.get_cost(node.get_state(), successors[i]) + node.get_cost()
            n = AstarNode(successors[i], heuristic_fn(successors[i]), parent = node, transition_cost = successor_cost)
            if successors[i] in visited_cost.keys() and successor_cost >= visited_cost[successors[i]]:
                continue
            visited_cost[successors[i]] = successor_cost
            heappush(pqueue, n)
    return solution

    # you write the rest:
