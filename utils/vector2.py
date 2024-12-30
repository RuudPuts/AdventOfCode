import math

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

    def __lt__(self, other):
        return self.tuple < other.tuple

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

    def offset_by(self, x=0, y=0):
        return Vector2(self.x + x, self.y + y)

    def distance_to(self, other):
        dx = abs(self.x - other.x)
        dy = abs(self.y - other.y)
        return math.sqrt(dx * 2 + dy * 2)

    def line_to(self, other):
        dx = abs(self.x - other.x)
        dy = abs(self.y - other.y)
        if dx > 0 and dy > 0:
            raise Exception("Diagonals not supported!")

        if dx > 0:
            source = self
            if other.x < source.x:
                source = other

            return list(map(lambda x: source.offset_by(x=x), range(dx + 1)))
        if dy > 0:
            source = self
            if other.y < source.y:
                source = other

            return list(map(lambda y: source.offset_by(y=y), range(dy + 1)))


    @property
    def adjacent4(self):
        return [
            self.offset_by(0, -1),
            self.offset_by(-1, 0),
            self.offset_by(1, 0),
            self.offset_by(0, 1)
        ]
    
    @property
    def adjacent4diag(self):
        return [
            self.offset_by(-1, -1),
            self.offset_by(1, -1),
            self.offset_by(1, 1),
            self.offset_by(-1, 1)
        ]

    @property
    def adjacent8(self):
        return self.adjacent4 + [
            self.offset_by(-1, -1),
            self.offset_by(1, -1),

            self.offset_by(-1, 1),
            self.offset_by(1, 1)
        ]
