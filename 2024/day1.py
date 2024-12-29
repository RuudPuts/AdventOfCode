from day import Day
from input_parser import InputParser


class Day1(Day):
    @property
    def title(self):
        return "Historian Hysteria"

    @property
    def input_parser(self):
        return DoubleListParser()

    @property
    def example_input(self):
        return """3   4
4   3
2   5
1   3
3   9
3   3"""

    @property
    def expected_results(self):
        return {
            "task1_example": 11,
            "task1": 1151792,
            "task2_example": 31,
            "task2": 21790168
        }

    def task1(self, input):
        left_list, right_list = input
        left_list.sort()
        right_list.sort()
        
        distances = [ abs(left_list[i] - right_list[i]) for i in range(len(left_list)) ]

        return sum(distances)

    def task2(self, input):
        left_list, right_list = input

        # how many times does 3 apprear in right_list?
        similarities = [ i * len(list(filter(lambda x: x == i, right_list))) for i in left_list ]

        return sum(similarities)


class DoubleListParser(InputParser):
    def parse(self, input):
        left_list = []
        right_list = []

        for line in input:
            parts = line.split(" ")
            left_list.append(int(parts[0]))
            right_list.append(int(parts[-1]))

        return left_list, right_list