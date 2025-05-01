import random

class RubiksCube:
    def __init__(self, size):
        self.size = size
        self.faces = {
            'U': [[ 'W' for _ in range(size)] for _ in range(size)],
            'D': [[ 'Y' for _ in range(size)] for _ in range(size)],
            'F': [[ 'G' for _ in range(size)] for _ in range(size)],
            'B': [[ 'B' for _ in range(size)] for _ in range(size)],
            'L': [[ 'O' for _ in range(size)] for _ in range(size)],
            'R': [[ 'R' for _ in range(size)] for _ in range(size)],
        }

    def is_solved(self):
        for face in self.faces.values():
            color = face[0][0]
            if any(cell != color for row in face for cell in row):
                return False
        return True

    def rotate_face_clockwise(self, face):
        """Rotate a face 90 degrees clockwise (in-place)"""
        size = self.size
        new_face = [[None]*size for _ in range(size)]
        for i in range(size):
            for j in range(size):
                new_face[j][size - 1 - i] = self.faces[face][i][j]
        self.faces[face] = new_face

    def rotate_face_counterclockwise(self, face):
        """Rotate a face 90 degrees counterclockwise (in-place)"""
        for _ in range(3):
            self.rotate_face_clockwise(face)

    def rotate(self, face, clockwise=True):
        """Rotate a face and the adjacent rows/columns"""
        s = self.size
        f = self.faces

        self.rotate_face_clockwise(face) if clockwise else self.rotate_face_counterclockwise(face)

        if face == 'U':
            rows = ['F', 'R', 'B', 'L']
            idxs = [(0, i) for i in range(s)]
        elif face == 'D':
            rows = ['F', 'L', 'B', 'R']
            idxs = [(s-1, i) for i in range(s)]
        elif face == 'F':
            rows = ['U', 'R', 'D', 'L']
            idxs = [(s-1, i) for i in range(s)]
        elif face == 'B':
            rows = ['U', 'L', 'D', 'R']
            idxs = [(0, i) for i in range(s)]
        elif face == 'L':
            rows = ['U', 'F', 'D', 'B']
            idxs = [(i, 0) for i in range(s)]
        elif face == 'R':
            rows = ['U', 'B', 'D', 'F']
            idxs = [(i, s-1) for i in range(s)]
        else:
            return

        # Get the values from the 4 affected face rows/columns
        values = []
        for face_name in rows:
            values.append([f[face_name][i][j] for i, j in idxs])

        # Rotate them
        if not clockwise:
            values = values[1:] + values[:1]
        else:
            values = values[-1:] + values[:-1]

        # Assign rotated values back
        for (face_name, val) in zip(rows, values):
            for (i, j), v in zip(idxs, val):
                f[face_name][i][j] = v

    def shuffle(self, moves=20):
        faces = ['U', 'D', 'F', 'B', 'L', 'R']
        for _ in range(moves):
            self.rotate(random.choice(faces), clockwise=random.choice([True, False]))

    def __str__(self):
        """Return a simple string representation of the cube (flattened view)"""
        result = ""
        for name in ['U', 'D', 'F', 'B', 'L', 'R']:
            result += f"{name} face:\n"
            for row in self.faces[name]:
                result += ' '.join(row) + '\n'
        return result


cube = RubiksCube(6)
cube.shuffle(moves=20)  # You can change the number of moves for more/less randomness
print(cube)