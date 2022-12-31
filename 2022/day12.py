import string
import sys
from day import Day
from dataclasses import dataclass
from input_parser import InputParser
from utils import Grid, PathFinder, Vector2

class Day12(Day):
    @property
    def title(self):
        return "Hill Climbing Algorithm"

    @property
    def input_parser(self):
        return HeightMapParser()

    @property
    def example_input(self):
        return """Sabqponm
abcryxxl
accszExk
acctuvwj
abdefghi"""

    @property
    def expected_results(self):
        return {
            "task1_example": 31,
            "task1": 408,
            "task2_example": 29,
            "task2": 399
        }

    def task1(self, input):
        map, start, end = input

        # map.print(delimeter=" ")

        result = SignalPathFinder(map).find_path(start, end)

        return result

    def task2(self, input):
        map, _, end = input

        path_finder = SignalPathFinder(map)
        start_locations = map.find_by_value(lambda x: x == 0)
        paths = {start: path_finder.find_path(start, end) for start in start_locations}

        return min(paths.values())


class HeightMapParser(InputParser):
    def parse(self, input):
        map = []
        start = None
        end = None

        for y, line in enumerate(input):
            row = []
            for x, char in enumerate(line):
                value = char
                if char == "S":
                    start = Vector2(x, y)
                    value = 'a'
                elif char == "E":
                    end = Vector2(x, y)
                    value = 'z'

                row.append(string.ascii_lowercase.index(value))
            map.append(row)

        return (Grid(map), start, end)


class SignalPathFinder(PathFinder):
    def weight(self, item):
        return 1

    def heuristic(self, item, end):
        return 0

    def neighbours(self, item):
        neighbours = [n for n in item.adjacent4 if self.tree.contains(n)]

        return [n for n in neighbours if (self.tree.get(n) - self.tree.get(item)) <= 1]