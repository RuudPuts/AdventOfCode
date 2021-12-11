from day import Day
from input_parser import ConvertToIntParser
import itertools

from utils.functions import windows

class Day9(Day):
    def title(self):
        return "Encoding Error"

    def input_parser(self):
        return ConvertToIntParser()

    def task1(self, input):
        return self.find_invalid_number(input)

    def task2(self, input):
        target = self.find_invalid_number(input)
        window = self.find_window_sum(input, target)
                
        return min(window) + max(window)

    def find_invalid_number(self, input, preamble=25):
        sum_count = 2

        for i in range(preamble, len(input)):
            windows = input[max(0, i - preamble): i]
            combinations = list(itertools.permutations(windows, sum_count))
            if input[i] not in [sum(list(x)) for x in combinations]:
                return input[i]

        return None

    def find_window_sum(self, input, target):
        start_index = 0
        while start_index < len(input) - 1:
            numbers = []
            for i in range(start_index, len(input)):
                numbers.append(input[i])
                
                if sum(numbers) == target:
                    return numbers
                elif sum(numbers) > target:
                    start_index += 1
                    break