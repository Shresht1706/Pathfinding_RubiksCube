    def __str__(self):
        """Return a simple string representation of the cube (flattened view)"""
        result = ""
        for name in ['U', 'D', 'F', 'B', 'L', 'R']:
            result += f"{name} face:\n"
            for row in self.faces[name]:
                result += ' '.join(row) + '\n'
        return result