from day import Day
from input_parser import ConvertToIntParser
from collections import defaultdict
import itertools

class Day10(Day):
    def title(self):
        return "Adapter Array"

    def input_parser(self):
        return ConvertToIntParser()

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
        for adapter in input[1:]:
            count[adapter] = count.get(adapter-1, 0) + count.get(adapter-2, 0) + count.get(adapter-3, 0)

        return count[input[-1]]
