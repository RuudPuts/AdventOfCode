from day import Day
from input_parser import InputParser

import re

class Day2(Day):
    @property
    def title(self):
        return "Password Philosophy"

    @property
    def input_parser(self):
        return PasswordParser()

    @property
    def example_input(self):
        return """1-3 a: abcde
1-3 b: cdefg
2-9 c: ccccccccc"""

    @property
    def expected_results(self):
        return {
            "task1_example": 2,
            "task1": 614,
            "task2_example": 1,
            "task2": 354
        }

    def task1(self, input):
        valid = []
        for entry in input:
            char_count = entry['password'].count(entry['char'])
            if char_count >= entry['num_a'] and char_count <= entry['num_b']:
                valid.append(entry)

        return len(valid)

    def task2(self, input):
        valid = []
        for entry in input:
            chars = [
                entry['password'][entry['num_a'] - 1],
                entry['password'][entry['num_b'] - 1]
            ]
            if chars.count(entry['char']) == 1:
                valid.append(entry)

        return len(valid)

class PasswordParser(InputParser):
    def parse_line(self, line):
        regex = r"(\d+)-(\d+) (\w+): (.*)$"
        match = re.match(regex, line)

        return {
            'num_a': int(match.group(1)),
            'num_b': int(match.group(2)),
            'char': match.group(3),
            'password': match.group(4),
        }

    def parse(self, input):
        return list(map(self.parse_line, input))
