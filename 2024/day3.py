from day import Day
from input_parser import InputParser
from functools import reduce
from operator import mul
import re


class Day3(Day):
    @property
    def title(self):
        return "Mull It Over"

    @property
    def input_parser(self):
        return MemoryParser()

    @property
    def example_input(self):
        return """x**mul(2,4)**&mul[3,7]!^**don't()**_mul(5,5)+mul(32,64](mul(11,8)un**do()**?**mul(8,5)**)"""

    @property
    def expected_results(self):
        return {
            "task1_example": 161,
            "task1": 173731097,
            "task2_example": 48,
            "task2": 93729253
        }

    def task1(self, input):
        return self.calculate(input, use_state_modifiers=False)

    def task2(self, input):
        return self.calculate(input, use_state_modifiers=True)
    
    def calculate(self, input, use_state_modifiers):
        result = 0
        enabled = True

        for action, *args in input:
            if action == 'do':
                enabled = True
            elif action == 'dont' and use_state_modifiers:
                enabled = False
            elif action == 'mul' and enabled:
                result += reduce(mul, map(int, args))

        return result


class MemoryParser(InputParser):
    def parse(self, input):
        regexes = {
            'do': re.compile(r"do\(\)"),
            'dont': re.compile(r"don't\(\)"),
            'mul': re.compile(r"mul\((\d+),(\d+)\)")
        }

        actions = []

        for line in input:
            re.findall(r"mul\((\d+),(\d+)\)", line)

            line_matches = {}
            
            for key, regex in regexes.items():
                for match in list(regex.finditer(line)):
                    line_matches[match.start()] = (key, match.groups())

            for k in sorted(line_matches.keys()):
                key, groups = line_matches[k]
                actions.append((key, *groups))

        return actions