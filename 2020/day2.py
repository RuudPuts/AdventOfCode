from day import Day
from input_parser.input_parser import InputParser

import re

class Day2(Day):
    def title(self):
        return "Password Philosophy"

    def input_parser(self):
        return PasswordParser()

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
