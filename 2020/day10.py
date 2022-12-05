from day import Day
from input_parser import ConvertToIntParser
from collections import defaultdict
import itertools

class Day10(Day):
    @property
    def title(self):
        return "Adapter Array"

    @property
    def input_parser(self):
        return ConvertToIntParser()

    @property
    def example_input(self):
        return """16
10
15
5
1
11
7
19
6
12
4"""

    @property
    def expected_results(self):
        return {
            "task1_example": 35,
            "task1": 3000,
            "task2_example": 8,
            "task2": 193434623148032
        }

    def task1(self, input):
        input = sorted(input)
        input.insert(0, 0)
        input.append(max(input) + 3)

        jumps = defaultdict(int)
        for i in range(1, len(input)):
            jumps[input[i] - input[i - 1]] += 1

        return jumps[1] * jumps[3]

    def task2(self, input):
        input = sorted(input)
        input.insert(0, 0)
        input.append(max(input) + 3)

        count = {0: 1}
        for i in input[1:]:
            count[i] = count.get(i - 1, 0) + count.get(i - 2, 0) + count.get(i - 3, 0)

        return count[input[-1]]
