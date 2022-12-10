import math
from day import Day
from input_parser import IntGridParser
from utils import Vector2, all_lower


class Day8(Day):
    @property
    def title(self):
        return "Treetop Tree House"

    @property
    def input_parser(self):
        return IntGridParser()

    @property
    def example_input(self):
        return """30373
25512
65332
33549
35390"""

    @property
    def expected_results(self):
        return {
            "task1_example": 21,
            "task1": 1669,
            "task2_example": 8,
            "task2": 331344
        }

    def task1(self, input):
        visible = set()
        for y in range(input.height):
            for x in range(input.width):
                point = Vector2(x, y)
                value = input.get(point)

                if (all_lower(input.values_left(point), value) or
                        all_lower(input.values_top(point), value) or
                        all_lower(input.values_right(point), value) or
                        all_lower(input.values_bottom(point), value)):
                    visible.add(point)

        return len(visible)

    def task2(self, input):
        score = 0
        for y in range(input.height):
            for x in range(input.width):
                point = Vector2(x, y)
                value = input.get(point)

                def calculate_score(list, value):
                    score = 0

                    for item in list:
                        score += 1

                        if item >= value:
                            break

                    return score

                point_score = math.prod([
                    calculate_score(input.values_left(point), value),
                    calculate_score(input.values_top(point), value),
                    calculate_score(input.values_right(point), value),
                    calculate_score(input.values_bottom(point), value)
                ])

                score = max(score, point_score)

        return score
