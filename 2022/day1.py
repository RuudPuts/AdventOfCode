from day import Day
from input_parser import InputParser


class Day1(Day):
    @property
    def title(self):
        return "Calorie Counting"

    @property
    def input_parser(self):
        return CaloriesParser()

    @property
    def example_input(self):
        return """1000
2000
3000

4000

5000
6000

7000
8000
9000

10000"""

    @property
    def expected_results(self):
        return {
            "task1_example": 24000,
            "task1": 71934,
            "task2_example": 45000,
            "task2": 211447
        }

    def task1(self, input):
        return max(input)

    def task2(self, input):
        return sum(input[-3:])


class CaloriesParser(InputParser):
    def parse(self, input):
        array = []
        temp_array = []

        for line in input:
            if len(line) == 0:
                if len(temp_array) > 0:
                    array.append(sum(temp_array))
                    temp_array = []
                continue

            temp_array.append(int(line))

        if len(temp_array) > 0:
            array.append(sum(temp_array))
            temp_array = []

        array.sort()
        return array
