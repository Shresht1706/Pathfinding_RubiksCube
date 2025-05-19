from collections import deque
from temp import RubiksCube
import heapq
import itertools

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
