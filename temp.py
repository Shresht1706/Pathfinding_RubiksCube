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
        """Check if each face has a uniform color."""
        for face in self.faces.values():
            color = face[0][0]
            if any(cell != color for row in face for cell in row):
                return False
        return True

    def rotate_layer(self, face, clockwise=True):
        """Rotate an outer face and its adjacent edge strips."""
        s = self.size
        f = self.faces

        # Rotate the face itself
        new_face = [[None] * s for _ in range(s)]
        for i in range(s):
            for j in range(s):
                if clockwise:
                    new_face[j][s - 1 - i] = f[face][i][j]
                else:
                    new_face[s - 1 - j][i] = f[face][i][j]
        f[face] = new_face

        # Define adjacent edges to rotate
        if face == 'U':
            sides = ['F', 'R', 'B', 'L']
            idxs = [(0, i) for i in range(s)]
        elif face == 'D':
            sides = ['F', 'L', 'B', 'R']
            idxs = [(s - 1, i) for i in range(s)]
        elif face == 'F':
            sides = ['U', 'R', 'D', 'L']
            idxs = [(s - 1, i) for i in range(s)]
        elif face == 'B':
            sides = ['U', 'L', 'D', 'R']
            idxs = [(0, i) for i in range(s)]
        elif face == 'L':
            sides = ['U', 'F', 'D', 'B']
            idxs = [(i, 0) for i in range(s)]
        elif face == 'R':
            sides = ['U', 'B', 'D', 'F']
            idxs = [(i, s - 1) for i in range(s)]
        else:
            raise ValueError(f"Invalid face '{face}'.")

        # Extract edge values
        values = [[f[side][i][j] for (i, j) in idxs] for side in sides]

        # Rotate edge values
        if clockwise:
            values = values[-1:] + values[:-1]
        else:
            values = values[1:] + values[:1]

        # Assign rotated values
        for side, val in zip(sides, values):
            for (i, j), v in zip(idxs, val):
                f[side][i][j] = v

    def rotate_inner_slice(self, axis, layer_index, clockwise=True):
        """
        Rotate an inner slice (not an outer face).
        Axis: 'x', 'y', or 'z'
        Layer index: must be 1 <= index <= size - 2
        """
        s = self.size
        if layer_index == 0 or layer_index == s - 1:
            raise ValueError("Use rotate_layer() for outer layers (index 0 or size-1).")

        f = self.faces
        # Helper to deep copy rows/columns
        def get_col(face, col): return [f[face][i][col] for i in range(s)]
        def set_col(face, col, values): [f[face].__setitem__(i, [*f[face][i][:col], values[i], *f[face][i][col+1:]]) for i in range(s)]
        
        if axis == 'x':
            # Vertical slice across U -> B -> D -> F
            u_col = get_col('U', layer_index)
            b_col = get_col('B', s - 1 - layer_index)[::-1]  # reverse B column
            d_col = get_col('D', layer_index)
            f_col = get_col('F', layer_index)

            if clockwise:
                set_col('U', layer_index, f_col)
                set_col('B', s - 1 - layer_index, u_col[::-1])
                set_col('D', layer_index, b_col)
                set_col('F', layer_index, d_col)
            else:
                set_col('U', layer_index, b_col[::-1])
                set_col('B', s - 1 - layer_index, d_col)
                set_col('D', layer_index, f_col)
                set_col('F', layer_index, u_col)

        elif axis == 'y':
            # Horizontal slice across F -> R -> B -> L
            row = layer_index
            f_row = f['F'][row]
            r_row = f['R'][row]
            b_row = f['B'][row][::-1]
            l_row = f['L'][row][::-1]

            if clockwise:
                f['F'][row] = l_row
                f['R'][row] = f_row
                f['B'][row] = r_row[::-1]
                f['L'][row] = b_row[::-1]
            else:
                f['F'][row] = r_row
                f['R'][row] = b_row[::-1]
                f['B'][row] = l_row[::-1]
                f['L'][row] = f_row

        elif axis == 'z':
            # Depth slice (like rotating a layer of the cube face)
            u_row = f['U'][s - 1 - layer_index]
            r_col = get_col('R', layer_index)
            d_row = f['D'][layer_index]
            l_col = get_col('L', s - 1 - layer_index)

            if clockwise:
                f['U'][s - 1 - layer_index] = l_col[::-1]
                set_col('R', layer_index, u_row)
                f['D'][layer_index] = r_col[::-1]
                set_col('L', s - 1 - layer_index, d_row)
            else:
                f['U'][s - 1 - layer_index] = r_col
                set_col('R', layer_index, d_row[::-1])
                f['D'][layer_index] = l_col
                set_col('L', s - 1 - layer_index, u_row[::-1])
        else:
            raise ValueError("Axis must be 'x', 'y', or 'z'.")


    def shuffle(self, moves=20):
        """Randomly apply face and slice rotations."""
        faces = ['U', 'D', 'F', 'B', 'L', 'R']
        axes = ['x', 'y', 'z']
        for _ in range(moves):
            if self.size > 2 and random.random() < 0.3:
                axis = random.choice(axes)
                layer = random.randint(1, self.size - 2)
                self.rotate_inner_slice(axis, layer, clockwise=random.choice([True, False]))
            else:
                self.rotate_layer(random.choice(faces), clockwise=random.choice([True, False]))

    def __str__(self):
        result = ""
        for name in ['U', 'D', 'F', 'B', 'L', 'R']:
            result += f"{name} face:\n"
            for row in self.faces[name]:
                result += ' '.join(row) + '\n'
        return result

    def cube_to_tuple(self):
        """Serialize cube state to a hashable form for visited tracking."""
        return tuple(tuple(tuple(row) for row in self.faces[face]) for face in ['U', 'D', 'F', 'B', 'L', 'R'])
