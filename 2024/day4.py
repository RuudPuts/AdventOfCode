from day import Day
from input_parser import GridParser


class Day4(Day):
    @property
    def title(self):
        return "Ceres Search"

    @property
    def input_parser(self):
        return GridParser()

    @property
    def example_input(self):
        return """MMMSXXMASM
MSAMXMSMSA
AMXSXMAAMM
MSAMASMSMX
XMASAMXAMM
XXAMMXXAMA
SMSMSASXSS
SAXAMASAAA
MAMMMXMMMM
MXMXAXMASX"""

    @property
    def expected_results(self):
        return {
            "task1_example": 18,
            "task1": 2370,
            "task2_example": 9,
            "task2": 1908
        }

    def task1(self, input):
        target_str = "XMAS"

        start_points = list(input.find_by_value(lambda x: x == target_str[0]))

        counter = 0
        for start in start_points:
            all_lines = input.lines8(start, length=len(target_str) - 1)

            for points in all_lines:
                value = list(map(lambda x: input.get(x), points))
                if None in value:
                    continue

                if "".join(value) == target_str[1:]:
                    counter += 1

        return counter

    def task2(self, input):
        start_points = list(input.find_by_value(lambda x: x == "A"))

        counter = 0
        for start in start_points:
            corner_neighbours = input.neighbours4diag(start)
            if len(corner_neighbours) != 4:
                # 'A' cell at edge of grid
                continue

            neighbours_values = [input.get(n) for n in corner_neighbours];
            valid_values = [
                f"MSSM",
                f"SMMS",
                f"MMSS",
                f"SSMM",
            ]
            if "".join(neighbours_values) in valid_values:
                counter += 1

        return counter
