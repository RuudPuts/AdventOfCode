from day import Day
from input_parser import InputParser
from collections import namedtuple
from utils import Vector2, OCR
import re
from PIL import Image

from utils.grid import Grid

class Day13(Day):
    def title(self):
        return "Transparent Origami"

    def input_parser(self):
        return InstructionsParser()

    def create_grid(self, input):
        max_x, max_y = 0, 0
        for i in [di for di in input if isinstance(di, DotInstruction)]:
            max_x = max(max_x, i.point.x)
            max_y = max(max_y, i.point.y)

        return Grid(width=max_x + 1, height=max_y + 1, initial_value='.')

    def task1(self, input):
        grid = self.create_grid(input)
        grid = self.process_instructions(grid, input, max_folds=1)

        return len(list(grid.find_by_value(lambda x: x == '#')))

    def task2(self, input):
        grid = self.create_grid(input)
        grid = self.process_instructions(grid, input)

        return "".join(grid.ocr(fill_value='#'))

    def process_instructions(self, grid, input, max_folds=None):
        folds = 0

        for i in input:
            if isinstance(i, DotInstruction):
                grid.set(i.point, '#')
            if isinstance(i, FoldInstruction):
                if i.axis == 'x':
                    splitA, splitB = grid.split(x=i.index)
                    splitB.mirror_vertically()
                if i.axis == 'y':
                    splitA, splitB = grid.split(y=i.index)
                    splitB.mirror_horizontally()

                splitA.merge(splitB, lambda a, b: a if a == '#' else b)
                grid = splitA

                folds += 1

                if max_folds and folds == max_folds:
                    return grid
            
        return grid

class Instruction:
    pass

class FoldInstruction(Instruction):
    def __init__(self, axis, index):
        self.axis = axis
        self.index = index

    def __repr__(self): 
        return "%s(axis=%s index=%d)" % (self.__class__.__name__, self.axis, self.index)

class DotInstruction(Instruction):
    def __init__(self, point):
        self.point = point

    def __repr__(self): 
        return "%s(point=%s)" % (self.__class__.__name__, self.point)

class InstructionsParser(InputParser):
    def parse_line(self, line):
        if fold_match := re.match(r"fold along (\w)=(\d+)", line):
            return FoldInstruction(fold_match.group(1), int(fold_match.group(2)))
        else:
            splitted = line.split(",")
            return DotInstruction(Vector2(int(splitted[0]), int(splitted[1])))

    def parse(self, input):
        # input = [
        #     "6,10",
        #     "0,14",
        #     "9,10",
        #     "0,3",
        #     "10,4",
        #     "4,11",
        #     "6,0",
        #     "6,12",
        #     "4,1",
        #     "0,13",
        #     "10,12",
        #     "3,4",
        #     "3,0",
        #     "8,4",
        #     "1,10",
        #     "2,14",
        #     "8,10",
        #     "9,0",
        #     "",
        #     "fold along y=7",
        #     "fold along x=5",
        # ]

        input = [l for l in input if l]

        return list(map(self.parse_line, input))
