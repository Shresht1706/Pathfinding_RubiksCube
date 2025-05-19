from temp import RubiksCube
from Solver import bfs, dfs, astar

cube = RubiksCube(6)
cube.shuffle(moves=3)
print("Scrambled Cube:")
print(cube)

solution = astar(cube)  # or dfs(cube) or astar(cube)
print("Solution:", solution)

