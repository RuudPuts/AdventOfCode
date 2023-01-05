from day import Day
from input_parser import InputParser
from utils import flatten, windows, Grid, Vector2


class Day14(Day):
    @property
    def title(self):
        return "Regolith Reservoir"

    @property
    def input_parser(self):
        return SolidStructureParser()

    @property
    def example_input(self):
        return """498,4 -> 498,6 -> 496,6
503,4 -> 502,4 -> 502,9 -> 494,9"""

    @property
    def expected_results(self):
        return {
            "task1_example": 24,
            "task1": 964,
            "task2_example": 93,
            "task2": 32041
        }

    def simulate_sand(self, grid):
        start_vector = Vector2(500, 0)
        sand_counter = 0
        sand_max_y = grid.height - 2
        while True:
            sand_coord = start_vector
            while True:
                sand_moved = False
                targets = [
                    sand_coord.offset_by(y=1),  # Down
                    sand_coord.offset_by(x=-1, y=1),  # Down left
                    sand_coord.offset_by(x=1, y=1),  # Down right
                ]

                for target in targets:
                    if grid.get(target) == '.':
                        grid.set(sand_coord, '.')
                        sand_coord = target
                        sand_moved = True
                        break

                if not sand_moved or sand_coord.y > sand_max_y:
                    break

            grid.set(sand_coord, 'o')
            grid.set(start_vector, "+")
            sand_counter += 1

            # Stop if sand falls into abyss
            if sand_coord.y > sand_max_y:
                sand_counter -= 1
                break

            # Stop if sand ends at start
            if sand_coord == start_vector:
                break

        return sand_counter

    def task1(self, input):
        grid = input

        return self.simulate_sand(grid)

    def task2(self, input):
        grid = input
        for x in range(grid.width):
            grid.set(Vector2(x, grid.height - 1), "#")

        return self.simulate_sand(grid)


class SolidStructureParser(InputParser):
    def parse(self, input):
        structures = []

        for line in input:
            structure = map(lambda x: Vector2(int(x[0]), int(x[1])), map(lambda c: c.split(","), line.split(" -> ")))
            structures.append(list(structure))

        all_coords = flatten(structures)
        all_x = list(map(lambda v: v.x, all_coords))
        all_y = list(map(lambda v: v.y, all_coords))

        grid = Grid(width=max(all_x) * 2, height=max(all_y) + 3, initial_value='.')
        for structure in structures:
            for window in windows(structure, 2):
                for point in window[0].line_to(window[1]):
                    grid.set(point, '#')

        return grid
