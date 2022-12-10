class Vector2:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return "%s(x=%d, y=%d)" % (self.__class__.__name__, self.x, self.y)

    def __eq__(self, other):
        if isinstance(other, Vector2):
            return self.x == other.x and self.y == other.y

        return False

    def __hash__(self):
        return hash((self.x, self.y))

    @property
    def tuple(self):
        return (self.x, self.y)

    def scale(self, scale):
        return Vector2(
            self.x * scale,
            self.y * scale
        )

    def offset_by(self, x, y):
        return Vector2(self.x + x, self.y + y)

    @property
    def adjacent4(self):
        return [
            self.offset_by(0, -1),
            self.offset_by(-1, 0),
            self.offset_by(1, 0),
            self.offset_by(0, 1)
        ]

    @property
    def adjacent8(self):
        return self.adjacent4 + [
            self.offset_by(-1, -1),
            self.offset_by(1, -1),

            self.offset_by(-1, 1),
            self.offset_by(1, 1)
        ]
