from day import Day
from input_parser import DummyParser
from utils import prod

class Day9(Day):
    def title(self):
        return "Smoke Basin"

    def input_parser(self):
        return DummyParser()

    def neighbours(self, x, y, width, height):
        neighbours = []
        if y > 0: # Top
            neighbours.append((x, y - 1))
        if x < (width - 1): # Right
            neighbours.append((x + 1, y))
        if y < (height - 1): # Bottom
            neighbours.append((x, y + 1))
        if x > 0: # Left
            neighbours.append((x - 1, y))

        return neighbours

    def task1(self, input):
        low_points = self.find_low_points(input)
        values = sum(list(map(lambda p: 1 + int(input[p[1]][p[0]]), low_points)))

        return values

    def task2(self, input):
        basins = {}
        for p in self.find_low_points(input):
            basins[p] = self.find_basin(input, p)

        largest = sorted(list(map(lambda x: len(x), basins.values())))
        
        return prod(largest[-3:])

    def find_low_points(self, input):
        height = len(input)
        width = len(input[0])

        low_points = []
        for y in range(len(input)):
            row = input[y]

            for x in range(len(row)):
                value = int(row[x])

                if value == 0:
                    low_points.append((x, y))
                else:
                    neighours = list(map(lambda n: int(input[n[1]][n[0]]), self.neighbours(x, y, width, height)))
                    if min(neighours) > value:
                        low_points.append((x, y))

        return low_points

    def find_basin(self, input, position):
        height = len(input)
        width = len(input[0])

        basin = [position]
        to_check = [position]

        while len(to_check) > 0:
            new_points = []
            for p in to_check:
                neighbours = self.neighbours(p[0], p[1], width, height)
                neighbours = list(filter(lambda n: n not in basin, neighbours))
                
                neighbours_to_check = list(filter(lambda n: int(input[n[1]][n[0]]) < 9, neighbours))
                new_points.extend(neighbours_to_check)
                basin.extend(neighbours_to_check)
                
            to_check = new_points

        return basin