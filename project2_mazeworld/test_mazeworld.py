from MazeworldProblem import MazeworldProblem
from Maze import Maze
import time
from astar_search import astar_search

# null heuristic, useful for testing astar search without heuristic (uniform cost search).
def null_heuristic(state):
    return 0

# Test problem: checks if one robot functions well
test_maze1 = Maze("maze2.maz")
test_mp = MazeworldProblem(test_maze1, (3,0))
result = astar_search(test_mp, test_mp.manhattan_heuristic)
print(result)
test_mp.animate_path_extension(result.path)


# Test problem: checks if all robots go to right goal by fixing the combination(5 robots)
test_maze2 = Maze("maze1.maz")
test_mp = MazeworldProblem(test_maze2, (8,3,6,3,4,3,7,3,5,3))
result = astar_search(test_mp, test_mp.manhattan_heuristic)
print(result)
test_mp.animate_path_extension(result.path)


# Test problems
#8 puzzle demo
test_puzzle = Maze("8puzzle.maz")
test_mp = MazeworldProblem(test_puzzle, (0,2,1,2,2,2,0,1,1,1,2,1,0,0,1,0))
result = astar_search(test_mp, test_mp.manhattan_heuristic)
print(result)
test_mp.animate_path_extension(result.path)


#Test Problem: three robots moving and also try all three heurisitic
test_maze3 = Maze("maze3.maz")
test_mp = MazeworldProblem(test_maze3, (1, 4, 1, 3, 1, 2))

# this should explore a lot of nodes; it's just uniform-cost search
result = astar_search(test_mp, null_heuristic)
print(result)

# this should do a bit better:
result = astar_search(test_mp, test_mp.manhattan_heuristic)
print(result)
#test_mp.animate_path_extension(result.path)

#demonstrate wavefront
result = astar_search(test_mp, test_mp.wavefront_bfs_heuristic)
print(result)
test_mp.animate_path_extension(result.path)



# Test problem: maze4.maz --> my own version of 10*10 maze with 6 robot_turns
# bigger state spaces, measure time of different heuristics

test_maze4 = Maze("maze4.maz")
test_mp = MazeworldProblem(test_maze4, (8,8,8,9,9,0))
start = time.time()
# this should explore a lot of nodes; it's just uniform-cost search
result = astar_search(test_mp, null_heuristic)
end = time.time()
print("time taken for null_heuristic(s):", end - start)
print(result)


# this should do a bit better:
start = time.time()
result = astar_search(test_mp, test_mp.manhattan_heuristic)
end = time.time()
print("time taken for manhattan(s): ", end - start)
print(result)


start = time.time()
result = astar_search(test_mp, test_mp.wavefront_bfs_heuristic)
end = time.time()
print("time taken for wavefront bfs(s): ", end - start)
print(result)

test_mp.animate_path_extension(result.path)
