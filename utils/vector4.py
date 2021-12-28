from utils.vector2 import Vector2

class Vector4:
    def __init__(self, position, width, height):
        self.position = position
        self.width = width
        self.height = height

    def __repr__(self):
        return f"{self.__class__.__name__}(position={self.position} width={self.width} height={self.height})"

    def __eq__(self, other):
        if isinstance(other, Vector4):
            return self.position == other.position and self.width == other.width and self.height == other.height

        return False

    @property
    def center(self):
        return Vector2(self.position.x + self.width / 2, self.position.y + self.height / 2)

    @property
    def shape(self):
        return [self.position.tuple, self.position.offset_by(self.width, self.height).tuple]

    def offset(self, horizontally, vertically):
        return Vector4(
            self.position.offset_by(horizontally, vertically),
            self.width,
            self.height
        )

    def scale(self, scale):
        return Vector4(
            self.position.scale(scale),
            self.width * scale,
            self.height * scale
        )

    def inset(self, hor_inset, ver_inset):
        return Vector4(
            self.position.offset_by(hor_inset, ver_inset),
            self.width - hor_inset * 2,
            self.height - ver_inset * 2
        )

    def rel_inset(self, inset):
        return self.inset(self.width * inset, self.height * inset)
