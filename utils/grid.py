from collections import namedtuple

from utils.vector2 import Vector2

class Grid:
    def __init__(self, data):
        self.data = data

    # def __init__(self, width, height, initial_value):
    #     self.data = [[initial_value for i in range(width)] for i in range(height)]

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
        # print("GET %d %d - %s" % (self.width, self.height, point))
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

    def find_by_value(self, block):
        for y in range(self.height):
            for x in range(self.width):
                point = Vector2(x, y)
                if block(self.get(point)):
                    yield point

    def neighbours(self, point):
        return [p for p in point.adjacent if self.contains(p)]

    def print(self):
        # From https://stackoverflow.com/a/13214945
        s = [[str(e) for e in row] for row in self]
        lens = [max(map(len, col)) for col in zip(*s)]
        fmt = ''.join('{{:{}}}'.format(x) for x in lens)
        table = [fmt.format(*row) for row in s]

        print()
        print('\n'.join(table))
        print()