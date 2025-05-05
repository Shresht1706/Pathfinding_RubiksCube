import random

class RubiksCube:
    def __init__(self, size):
        self.size = size
        self.faces = {
            'U': [['W'] * size for _ in range(size)],
            'D': [['Y'] * size for _ in range(size)],
            'F': [['G'] * size for _ in range(size)],
            'B': [['B'] * size for _ in range(size)],
            'L': [['O'] * size for _ in range(size)],
            'R': [['R'] * size for _ in range(size)],
        }

    def is_solved(self):
        """Check if all faces are one uniform color (solved state)"""
        for face in self.faces.values():
            color = face[0][0]
            if any(cell != color for row in face for cell in row):
                return False
        return True

    def rotate_face_clockwise(self, face):
        """Rotate a face 90 degrees clockwise"""
        size = self.size
        new_face = [[None] * size for _ in range(size)]
        for i in range(size):
            for j in range(size):
                new_face[j][size - 1 - i] = self.faces[face][i][j]
        self.faces[face] = new_face

    def rotate_face_counterclockwise(self, face):
        """Rotate a face 90 degrees counterclockwise"""
        for _ in range(3):  # 3 clockwise = 1 counterclockwise
            self.rotate_face_clockwise(face)

    def rotate(self, face, clockwise=True):
        """Rotate an outer face and its adjacent sides"""
        s = self.size
        f = self.faces

        self.rotate_face_clockwise(face) if clockwise else self.rotate_face_counterclockwise(face)

        if face == 'U':
            rows = ['F', 'R', 'B', 'L']
            idxs = [(0, i) for i in range(s)]
        elif face == 'D':
            rows = ['F', 'L', 'B', 'R']
            idxs = [(s - 1, i) for i in range(s)]
        elif face == 'F':
            rows = ['U', 'R', 'D', 'L']
            idxs = [(s - 1, i) for i in range(s)]
        elif face == 'B':
            rows = ['U', 'L', 'D', 'R']
            idxs = [(0, i) for i in range(s)]
        elif face == 'L':
            rows = ['U', 'F', 'D', 'B']
            idxs = [(i, 0) for i in range(s)]
        elif face == 'R':
            rows = ['U', 'B', 'D', 'F']
            idxs = [(i, s - 1) for i in range(s)]
        else:
            return

        values = []
        for face_name in rows:
            values.append([f[face_name][i][j] for i, j in idxs])

        if not clockwise:
            values = values[1:] + values[:1]
        else:
            values = values[-1:] + values[:-1]

        for (face_name, val) in zip(rows, values):
            for (i, j), v in zip(idxs, val):
                f[face_name][i][j] = v

    def rotate_inner_slice(self, axis, layer_index, clockwise=True):
        """
        Rotate an inner slice of the cube.
        - axis: 'x', 'y', or 'z'
        - layer_index: 0 to size-1 (0 and size-1 are outer layers; others are inner slices)
        """
        s = self.size
        if layer_index == 0 or layer_index == s - 1:
            return  # Outer layers should use rotate(), not this function

        if axis == 'x':
            # Vertical slice parallel to R/L faces
            faces = ['U', 'B', 'D', 'F']
            coords = [(i, layer_index) for i in range(s)]
        elif axis == 'y':
            # Horizontal slice parallel to U/D faces
            faces = ['F', 'R', 'B', 'L']
            coords = [(layer_index, i) for i in range(s)]
        elif axis == 'z':
            # Slice between F and B
            faces = ['U', 'R', 'D', 'L']
            coords = [(i, layer_index) for i in range(s)]
        else:
            raise ValueError("Invalid axis. Use 'x', 'y', or 'z'.")

        values = [[self.faces[face][i][j] for (i, j) in coords] for face in faces]

        # Rotate the four face strips
        values = values[-1:] + values[:-1] if clockwise else values[1:] + values[:1]

        for f_idx, face in enumerate(faces):
            for k, (i, j) in enumerate(coords):
                self.faces[face][i][j] = values[f_idx][k]

    def shuffle(self, moves=20):
        """Randomly rotate faces and slices to scramble the cube"""
        faces = ['U', 'D', 'F', 'B', 'L', 'R']
        axes = ['x', 'y', 'z']
        for _ in range(moves):
            if self.size > 2 and random.random() < 0.3:
                axis = random.choice(axes)
                layer = random.randint(1, self.size - 2)  # inner slices only
                self.rotate_inner_slice(axis, layer, clockwise=random.choice([True, False]))
            else:
                self.rotate(random.choice(faces), clockwise=random.choice([True, False]))

    def __str__(self):
        """Return a readable string representation of all cube faces"""
        result = ""
        for name in ['U', 'D', 'F', 'B', 'L', 'R']:
            result += f"{name} face:\n"
            for row in self.faces[name]:
                result += ' '.join(row) + '\n'
        return result
