import re
from collections import defaultdict
from day import Day
from input_parser import InputParser


class Day14(Day):
    @property
    def title(self):
        return "Extended Polymerization"

    @property
    def input_parser(self):
        return PolymerizationParser()

    @property
    def example_input(self):
        return """NNCB

CH -> B
HH -> N
CB -> H
NH -> C
HB -> C
HC -> B
HN -> C
NN -> C
BH -> H
NC -> B
NB -> B
BN -> B
BB -> N
BC -> B
CC -> N
CN -> C"""

    @property
    def expected_results(self):
        return {
            "task1_example": 1588,
            "task1": 2408,
            "task2_example": 2188189693529,
            "task2": 2651311098752
        }

    def task1(self, input):
        start, rules = input

        return self.run_task(start, rules, 10)

    def task2(self, input):
        start, rules = input

        return self.run_task(start, rules, 40)

    def run_task(self, input, rules, step_count):
        window_size = 2

        data = defaultdict(int)
        for idx in range(len(input) - 1):
            data[input[idx: idx + window_size]] += 1

        for _ in range(step_count):
            self.run_step(data, rules)

        char_count = defaultdict(int)
        for k, v in data.items():
            char_count[k[0]] += v
            char_count[k[1]] += v

        max_char_count = int(char_count[max(char_count, key=char_count.get)] + 1) / 2
        min_char_count = int(char_count[min(char_count, key=char_count.get)] + 1) / 2

        return round(max_char_count - min_char_count)

    def run_step(self, data, rules):
        inserts = list(filter(lambda x: x[1] > 0, data.items()))

        for k, v in inserts:
            data[k[0] + rules[k]] += v
            data[rules[k] + k[-1]] += v
            data[k] -= v

        return data


class PolymerizationParser(InputParser):
    def parse_line(self, line):
        match = re.match(r"(\w+) -> (\w+)", line)

        return (match.group(1), match.group(2))

    def parse(self, input):
        start = input[0]
        rules = dict({v for v in [self.parse_line(l) for l in input[1:] if l]})

        return (start, rules)
