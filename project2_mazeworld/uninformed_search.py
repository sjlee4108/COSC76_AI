#Seungjae Jason lEE
#Cosc 76
#Project 1
from collections import deque
from SearchSolution import SearchSolution

class SearchNode:
    # each search node except the root has a parent node
    # and all search nodes wrap a state object

    def __init__(self, state, parent=None):
        self.parent = parent
        self.state = state

    def get_parent(self):
        return self.parent

    def get_state(self):
        return self.state

def backchaining(node):
    #backchaining for bfs search, returns a list with correct path order
    if node.get_parent() == None:
        array = [node.get_state()]
        return array
    return backchaining(node.get_parent()) + [node.get_state()]

def bfs_search(search_problem):
    #bfs search, returns a list if a path exists, and [] if no path exists.
    head = SearchNode(search_problem.start_state, None)
    frontier = deque([head])
    visited = set([search_problem.start_state])
    node = head
    while(len(frontier) != 0):
        node = frontier.popleft()
        state = node.get_state()

        if search_problem.goal_test(state):
            return backchaining(node)

        successors = search_problem.get_successors(state)
        for i in range(len(successors)):
            if successors[i] not in visited:
                child_node = SearchNode(successors[i],node)
                frontier.append(child_node)
                visited.add(successors[i])
    return []

def dfs_search(search_problem, depth_limit=100, node=None, solution=None):
    #depth first search, returns a path, returns [] if no path
    # if no node object given, create a new search from starting state
    if node == None:
        node = SearchNode(search_problem.start_state)
        solution = SearchSolution(search_problem, "DFS")
        solution.add_path(node.get_state())

    if search_problem.goal_test(node.get_state()):
        return solution.get_path()

    if solution.get_visited_count() == depth_limit:
        solution.pop_path()
        solution.change_visited_count(-1)
        return []

    successors = search_problem.get_successors(node.get_state())
    for i in range(len(successors)):
        if solution.check_visited(successors[i]) == False:
            solution.add_path(successors[i])
            solution.change_visited_count(1)
            path = dfs_search(search_problem, node =  SearchNode(successors[i]), depth_limit = depth_limit, solution = solution)
            if path != []:
                return path
    solution.pop_path()
    solution.change_visited_count(-1)
    return []


def ids_search(search_problem, depth_limit=100):
    #Iterative depth first search
    for i in range(depth_limit):
        search_result = dfs_search(search_problem, depth_limit = i)
        if search_result != []:
            return search_result
    return []
