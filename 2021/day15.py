from day import Day
from dataclasses import dataclass
from input_parser import IntGridParser
from utils import Grid, Vector2
from utils.pathfinding import Dijkstra, PathNode

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
        return 0


@dataclass
class ChitonPathFinder(Dijkstra):
    grid: Grid

    def neighbours(self, pn: PathNode[Vector2]):
        return [PathNode(n, self.grid.get(n), pn) for n in self.grid.neighbours4(pn.node)]

