from day import Day
from input_parser import ConvertToListParser

from functools import reduce

class Day3(Day):
    @property
    def title(self):
        return "Toboggan Trajectory"

    @property
    def input_parser(self):
        return ConvertToListParser()

    def task1(self, input):
        squares = 0
        trees = 0

        slope_x = 3
        slope_y = 1

        position_x = slope_x
        position_y = slope_y

        while position_y < len(input):
            line = input[position_y]
            char = line[position_x]

            if char == '.':
                squares += 1
            elif char == '#':
                trees += 1

            position_y += slope_y
            position_x += slope_x
            if position_x >= len(line):
                position_x -= len(line)

        self.log("Total: " + str(squares + trees))
        self.log("Squares: " + str(squares))
        self.log("Trees: " + str(trees))

        return trees

    def task2(self, input):
        slopes = [
            (1, 1),
            (3, 1),
            (5, 1),
            (7, 1),
            (1, 2)
        ]

        trees_per_slope = list(map(lambda x: self.traverse_slope(x, input), slopes))
        self.log("Trees per slope: " + str(trees_per_slope))
        trees_total = reduce((lambda x, y: x * y), trees_per_slope)
        self.log("Trees total: " + str(trees_total))

        return trees_total

    def traverse_slope(self, slope, input):
        squares = 0
        trees = 0

        slope_x = slope[0]
        slope_y = slope[1]

        position_x = slope_x
        position_y = slope_y

        while position_y < len(input):
            line = input[position_y]
            char = line[position_x]

            if char == '.':
                squares += 1
            elif char == '#':
                trees += 1

            position_y += slope_y
            position_x += slope_x
            if position_x >= len(line):
                position_x -= len(line)

        self.log("Slope right " + str(slope_x) + ", down " + str(slope_y))
        self.log("Total: " + str(squares + trees))
        self.log("Squares: " + str(squares))
        self.log("Trees: " + str(trees))
        self.log("")
        self.log("")
        return trees