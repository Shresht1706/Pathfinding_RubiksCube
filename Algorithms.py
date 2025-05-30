from collections import deque
from Cube import RubiksCube
import heapq
import itertools
import time
import csv
import copy

def get_neighbors(cube):    #gets immedieate neighbouring states of the cube for the different algos
    neighbors = []
    size = cube.size
    for face in ['U', 'D', 'F', 'B', 'L', 'R']:
        for clockwise in [True, False]:
            new_cube = copy_cube(cube)
            new_cube.rotate_layer(face, clockwise)
            neighbors.append((new_cube, f"{face}{'+' if clockwise else '-'}"))
    if size > 2:
        for axis in ['x', 'y', 'z']:
            for layer in range(1, size - 1):
                for clockwise in [True, False]:
                    new_cube = copy_cube(cube)
                    new_cube.rotate_inner_slice(axis, layer, clockwise)
                    neighbors.append((new_cube, f"{axis}{layer}{'+' if clockwise else '-'}"))
    return neighbors

def copy_cube(cube):    #self explanatory
    import copy
    new_cube = RubiksCube(cube.size)
    new_cube.faces = copy.deepcopy(cube.faces)
    return new_cube

def bfs(cube):      #uses FIFO finds shortest path uses get_neighbours to generate all next states
    visited = set()
    queue = deque([(cube, [])])
    while queue:
        current, path = queue.popleft()
        state = current.cube_to_tuple()
        if state in visited:
            continue
        visited.add(state)
        if current.is_solved():
            return path
        for neighbor, move in get_neighbors(current):
            queue.append((neighbor, path + [move]))
    return None

def dfs(cube, max_depth=7):     #uses LIFO and explores depth and same as BFS for neighbours
    visited = set()
    stack = [(cube, [])]
    while stack:
        current, path = stack.pop()
        if len(path) > max_depth:
            continue
        state = current.cube_to_tuple()
        if state in visited:
            continue
        visited.add(state)
        if current.is_solved():
            return path
        for neighbor, move in get_neighbors(current):
            stack.append((neighbor, path + [move]))
    return None

def heuristic(cube):    #measures misplaces coloured cubes for more guidance
    misplaced = 0
    for face in cube.faces.values():
        color = face[0][0]
        misplaced += sum(cell != color for row in face for cell in row)
    return misplaced

def astar(cube):    #cost of f = g + h and uses heap to avoid revisitation.
    visited = set()
    counter = itertools.count()
    heap = [(heuristic(cube), 0, next(counter), cube, [])]

    while heap:
        est, cost, _, current, path = heapq.heappop(heap)
        state = current.cube_to_tuple()
        if state in visited:
            continue
        visited.add(state)
        if current.is_solved():
            return path
        for neighbor, move in get_neighbors(current):
            heapq.heappush(heap, (
                cost + 1 + heuristic(neighbor),  # f = g + h
                cost + 1,                        # g
                next(counter),                  # unique tie-breaker
                neighbor,
                path + [move]
            ))
    return None

def append_results(alg_name,size,shuffles,length,time_taken):
    csv_file = 'results.csv'
    file = open(csv_file, mode='a', newline='')
    writer = csv.writer(file)
    writer.writerow([alg_name, size, shuffles, length, time_taken]) #written as 'algorithm', 'cube_size', 'shuffle_count', 'solution_length', 'time_taken'

def results(size,alg_func,shuffle_numbers):        
    for i in range(1,shuffle_numbers+1):
        cube = RubiksCube(size)
        cube.shuffle(moves=i)
        print(f"\nCube Size: {size}, Shuffles: {i}")
        print(cube)
        start = time.time()
        solution = alg_func(copy.deepcopy(cube))
        end = time.time()
        time_taken = round(end - start, 4)
        length = len(solution) if solution else 0
        
        alg_name = alg_func.__name__
        print(f"{alg_name}: {length} moves, Time: {time_taken}s")
        time.sleep(1)
        append_results(alg_name,size,i,length,time_taken)
        time.sleep(1)


