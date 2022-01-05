from day import Day
from dataclasses import dataclass
import math
from input_parser import IntGridParser
from utils import Grid, Vector2
from utils.pathfinding import Dijkstra, PathNode
from utils.pathfinding.pathfinding import Dijkstra

class Day15(Day):
    @property
    def title(self):
        return "Chiton"

    @property
    def input_parser(self):
        return IntGridParser()

    def task1(self, input):
        start = Vector2(0, 0)
        end = Vector2(input.width - 1, input.height - 1)

        return ChitonPathFinder(input).find_path(start, end)

    def task2(self, input):
        input = ChitonGrid(input.data, repeats=4)

        start = Vector2(0, 0)
        end = Vector2(input.width - 1, input.height - 1)

        return ChitonPathFinder(input).find_path(start, end)


class ChitonGrid(Grid):
    def __init__(self, data=[], width=-1, height=-1, initial_value='', repeats=0):
        super().__init__(data, width, height, initial_value)
        self.repeats = repeats

    @property
    def width(self):
        return super().width * (self.repeats + 1)

    @property
    def height(self):
        return super().height * (self.repeats + 1)

    def get(self, point):
        offset = Vector2(
            math.floor(point.x / super().width),
            math.floor(point.y / super().height)
        )

        if offset.x == 0 and offset.y == 0:
            return super().get(point)

        original = Vector2(
            point.x - offset.x * super().width,
            point.y - offset.y * super().height
        )
        scaled = (super().get(original) + offset.x + offset.y) % 9

        return 9 if scaled == 0 else scaled


@dataclass
class ChitonPathFinder(Dijkstra):
    grid: Grid

    def neighbours(self, pn: PathNode[Vector2]):
        for n in self.grid.neighbours4(pn.node):
            yield PathNode(n, self.grid.get(n), pn)
