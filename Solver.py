from collections import deque
from temp import RubiksCube
import heapq
import itertools
import time
import csv
import copy

def get_neighbors(cube):
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

def copy_cube(cube):
    import copy
    new_cube = RubiksCube(cube.size)
    new_cube.faces = copy.deepcopy(cube.faces)
    return new_cube

def bfs(cube):
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

def dfs(cube, max_depth=7):
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

def heuristic(cube):
    misplaced = 0
    for face in cube.faces.values():
        color = face[0][0]
        misplaced += sum(cell != color for row in face for cell in row)
    return misplaced

# --- A* Search with tie-breaker to avoid comparing RubiksCube objects ---
def astar(cube):
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


def results(size,alg_func):
    shuffle_numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    csv_file = 'results.csv'
    with open(csv_file, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['algorithm', 'cube_size', 'shuffle_count', 'solution_length', 'time_taken'])
        for shuffles in shuffle_numbers:
            cube = RubiksCube(size)
            cube.shuffle(moves=shuffles)
            print(f"\nCube Size: {size}, Shuffles: {shuffles}")
            print(cube)
            start = time.time()
            solution = alg_func(copy.deepcopy(cube))
            end = time.time()
            time_taken = round(end - start, 4)
            length = len(solution) if solution else 0
            
            alg_name = alg_func.__name__
            print(f"{alg_name}: {length} moves, Time: {time_taken}s")
            writer.writerow([alg_name, size, shuffles, length, time_taken]) #written as 'algorithm', 'cube_size', 'shuffle_count', 'solution_length', 'time_taken'
            time.sleep(1)

