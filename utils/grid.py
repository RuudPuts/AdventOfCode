from PIL import Image, ImageDraw, ImageFont
from utils import vector4
from utils.drawable import Drawable
from utils.ocr.ocr import OCR
from utils.vector2 import Vector2
from utils.vector4 import Vector4

class Grid(Drawable):
    def __init__(self, data=[], width=-1, height=-1, initial_value=''):
        if data:
            self.data = data
        else:
            self.data = [[initial_value for i in range(width)] for i in range(height)]

    def __iter__(self):
        return iter(self.data)

    @property
    def width(self):
        return len(self.data[0])

    @property
    def height(self):
        return len(self.data)

    @property
    def size(self):
        return self.width * self.height

    def get(self, point):
        return self.data[point.y][point.x]

    def set(self, point, value):
        self.data[point.y][point.x] = value

    def contains(self, point):
        return point.x in range(self.width) and point.y in range(self.height)

    def map(self, block):
        for y in range(self.height):
            for x in range(self.width):
                point = Vector2(x, y)
                self.set(point, block(point, self.get(point)))

    def split(self, x=None, y=None):
        if x is not None and y is not None:
            raise Exception("Can only split 'x', OR 'y'")
        if not self.contains(Vector2(x or 0, y or 0)):
            raise Exception("Split out of bounds")

        if y:
            return Grid(data=self.data[0:y]), Grid(data=self.data[y + 1:])
        else:
            dataA = []
            dataB = []
            for row in self.data:
                dataA.append(row[0:x])
                dataB.append(row[x + 1:])

            return Grid(data=dataA), Grid(data=dataB)

    def merge(self, other, on_conflict):
        for y in range(min(self.height, other.height)):
            for x in range(min(self.width, other.width)):
                point = Vector2(x, y)
                value = self.get(point)
                other_value = other.get(point)

                if value != other_value:
                    self.set(point, on_conflict(value, other_value))

    def mirror_vertically(self):
        self.data = list(map(lambda x: list(reversed(x)), self.data))

    def mirror_horizontally(self):
        self.data = list(reversed(self.data))

    def find_by_value(self, block):
        for y in range(self.height):
            for x in range(self.width):
                point = Vector2(x, y)
                if block(self.get(point)):
                    yield point

    def neighbours4(self, point):
        return [p for p in point.adjacent4 if self.contains(p)]

    def neighbours6(self, point):
        return [p for p in point.adjacent6 if self.contains(p)]

    def ocr(self, fill_value):
        self.map(lambda _, value: value if value == fill_value else ' ')
        return OCR(self.data).text()

    def print(self):
        # From https://stackoverflow.com/a/13214945
        s = [[str(e) for e in row] for row in self]
        lens = [max(map(len, col)) for col in zip(*s)]
        fmt = ''.join('{{:{}}}'.format(x) for x in lens)
        table = [fmt.format(*row) for row in s]

        print()
        print('\n'.join(table))
        print()

    @property
    def filename(self):
        return 'grid'

    @property
    def image_size(self):
        return (self.width * self.image_scale, self.height * self.image_scale)

    @property
    def image_scale(self):
        return 80

    def draw_with(self, draw):
        for y in range(self.height):
            for x in range(self.width):
                point = Vector2(x, y)

                value = self.get(point)
                grey = int(255 / value)
                color = (grey, grey, grey)

                rect = Vector4(point, 1, 1)
                rect = rect.scale(self.image_scale)

                font = ImageFont.truetype("Arial", int(self.image_scale / 2))
                draw.text((rect.center.x, rect.center.y), str(value), fill=color, anchor="mm", font=font)
