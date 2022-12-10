from day import Day
from input_parser import IntGridParser
from utils import Vector2

class Day11(Day):
    @property
    def title(self):
        return "Dumbo Octopus"

    @property
    def input_parser(self):
        return IntGridParser()

    @property
    def example_input(self):
        return """5483143223
2745854711
5264556173
6141336146
6357385478
4167524645
2176841721
6882881134
4846848554
5283751526"""

    @property
    def expected_results(self):
        return {
            "task1_example": 1656,
            "task1": 1713,
            "task2_example": 195,
            "task2": 502
        }

    def task1(self, input):
        return sum([self.simulate_step(input) for _ in range(100)])

    def task2(self, input):
        step = 1
        while self.simulate_step(input) != input.size:
            step

        return step

    def simulate_step(self, grid):
        grid.map(lambda _, value: value + 1)

        flashed = []
        to_flash = self.points_to_flash(grid, flashed)
        while len(to_flash) > 0:
            for point in to_flash:
                flashed.append(point)

                for n in grid.neighbours8(point):
                    grid.set(n, grid.get(n) + 1)

            to_flash = self.points_to_flash(grid, flashed)

        for f in flashed:
            grid.set(f, 0)

        return len(flashed)

    def points_to_flash(self, grid, flashed):
        return [p for p in grid.find_by_value(lambda x: x > 9) if p not in flashed]