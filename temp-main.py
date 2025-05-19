from temp import RubiksCube
from Solver import bfs, dfs, astar

cube = RubiksCube(2)  # Change to 2 or 4 as needed
cube.shuffle(moves=8)
print("Scrambled Cube:")
print(cube)

solution = astar(cube)  # or dfs(cube) or astar(cube)
print("Solution:", solution)
