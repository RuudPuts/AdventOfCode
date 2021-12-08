from typing import Coroutine
from day import Day
from input_parser import InputParser
from collections import namedtuple
import re
from utils import generate_grid

class Day5(Day):
    def title(self):
        return "Hydrothermal Venture"

    def input_parser(self):
        return LineParser()

    def task1(self, input):
        input = self.filter_diagonal_lines(input)
        return self.run_task(input)

    def task2(self, input):
        return self.run_task(input)

    def run_task(self, input):
        board = Board(self.get_board_size(input))
        
        for line in input:
            for c in line.coordinates():
                board.count_coordinate(c)

        return board.count_overlaps()

    def filter_diagonal_lines(self, input):
        return list(filter(lambda l: l.start.x == l.end.x or l.start.y == l.end.y, input))

    def get_board_size(self, lines):
        max_x = 0
        max_y = 0
        for l in lines:
            max_x = max([max_x, l.start.x, l.end.x])
            max_y = max([max_y, l.start.y, l.end.y])

        return max_x + 1, max_y + 1

class Board:
    def __init__(self, size):
        self.grid = generate_grid(width=size[0], height=size[1], initial_value=0)

    def print(self):
        print("")
        for row in self.grid:
            print(''.join(list(map(lambda x: str(x) if x > 0 else '.', row))))
        print("")
                
    def count_coordinate(self, coordinate):
        self.grid[coordinate.y][coordinate.x] += 1

    def count_overlaps(self):
        all_counts = [point for row in self.grid for point in row]

        return len(list(filter(lambda x: x > 1, all_counts)))


Coordinate = namedtuple('Coordinate', 'x y')
class Line:
    def __init__(self, start, end):
        self.start = start
        self.end = end

    def coordinates(self):
        coordinates = [self.start]
        while self.end not in coordinates:
            last_coordinate = coordinates[-1]
            next_x = last_coordinate.x
            next_y = last_coordinate.y

            if last_coordinate.x < self.end.x:
                next_x += 1
            elif last_coordinate.x > self.end.x:
                next_x -= 1

            if last_coordinate.y < self.end.y:
                next_y += 1
            elif last_coordinate.y > self.end.y:
                next_y -= 1

            coordinates.append(Coordinate(x = next_x, y = next_y))

        return coordinates

class LineParser(InputParser):
    def parse_line(self, line):
        match = re.match(r"(\d*),(\d*) -> (\d*),(\d*)", line)

        return Line(
            start = Coordinate(x = int(match.group(1)), y = int(match.group(2))),
            end = Coordinate(x = int(match.group(3)), y = int(match.group(4)))
        )

    def parse(self, input):
        return list(map(self.parse_line, input))