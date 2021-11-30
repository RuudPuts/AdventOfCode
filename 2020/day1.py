from day import Day
from input_parser import ConvertToIntParser

import itertools
from functools import reduce

class Day1(Day):
    def title(self):
        return "Report Repair"

    def input_parser(self):
        return ConvertToIntParser()

    def task1(self, input):
        for i in range (0, len(input)):
            numA = input[i]

            for j in range(i + 1, len(input)):
                numB = input[j]
                
                if numA + numB == 2020:
                    return str(numA * numB)

        raise Exception("Task failed")

    def task2(self, input):
        all_combinations = list(itertools.combinations(input, 3))

        for i in range (0, len(all_combinations)):
            group = all_combinations[i]

            group_sum = sum(group)
            
            if group_sum == 2020:
                group_multiplied = reduce((lambda x, y: x * y), group)

                return str(group_multiplied)

        raise Exception("Task failed")
