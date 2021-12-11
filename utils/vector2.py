class Vector2:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self): 
        return "%s(x=%d y=%d)" % (self.__class__.__name__, self.x, self.y)

    def __eq__(self, other):
        if isinstance(other, Vector2):
            return self.x == other.x and self.y == other.y

        return False

    def offset_by(self, x, y):
        return Vector2(self.x + x, self.y + y)

    @property
    def adjacent(self):
        return [
            self.offset_by(-1, -1),
            self.offset_by(0, -1),
            self.offset_by(1, -1),

            self.offset_by(-1, 0),
            self.offset_by(1, 0),

            self.offset_by(-1, 1),
            self.offset_by(0, 1),
            self.offset_by(1, 1)
        ]
