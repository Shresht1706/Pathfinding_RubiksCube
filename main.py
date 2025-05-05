from Rubik_Cube import RubiksCube

# Create a 6x6 Rubik's Cube
cube = RubiksCube(size=6)

print("Before shuffling (solved cube):")
print(cube)

# Shuffle it with 20 random moves
cube.shuffle(moves=20)

print("After shuffling:")
print(cube)
