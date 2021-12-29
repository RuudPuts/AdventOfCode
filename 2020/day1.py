from functools import reduce
import itertools
from day import Day
from input_parser import ConvertToIntParser


class Day1(Day):
    @property
    def title(self):
        return "Report Repair"

    @property
    def input_parser(self):
        return ConvertToIntParser()

    def task1(self, input):
        for i in range(len(input)):
            numA = input[i]

            for j in range(i + 1, len(input)):
                numB = input[j]

                if numA + numB == 2020:
                    return str(numA * numB)

        raise Exception("Task failed")

    def task2(self, input):
        all_combinations = list(itertools.combinations(input, 3))

        for i in range(len(all_combinations)):
            group = all_combinations[i]

            group_sum = sum(group)

            if group_sum == 2020:
                group_multiplied = reduce((lambda x, y: x * y), group)

                return str(group_multiplied)

        raise Exception("Task failed")
