import json
import functools
from day import Day, DayTest
from input_parser import InputParser
from utils import chunks, flatten


class Day13(Day):
    @property
    def title(self):
        return "Distress Signal"

    @property
    def input_parser(self):
        return DistressSignalParser()

    @property
    def example_input(self):
        return """[1,1,3,1,1]
[1,1,5,1,1]

[[1],[2,3,4]]
[[1],4]

[9]
[[8,7,6]]

[[4,4],4,4]
[[4,4],4,4,4]

[7,7,7,7]
[7,7,7]

[]
[3]

[[[]]]
[[]]

[1,[2,[3,[4,[5,6,7]]]],8,9]
[1,[2,[3,[4,[5,6,0]]]],8,9]"""

    @property
    def tests(self):
        tests = [
            (["[1,1,3,1,1]",                 "[1,1,5,1,1]"],                             -1),
            (["[[1],[2,3,4]]",               "[[1],4]"],                                 -1),
            (["[9]",                         "[[8,7,6]]"],                               1),
            (["[[4,4],4,4]",                 "[[4,4],4,4,4]"],                           -1),
            (["[7,7,7,7]",                   "[7,7,7]"],                                 1),
            (["[]",                          "[3]"],                                     -1),
            (["[[[]]]",                      "[[]]"],                                    1),
            (["[1,[2,[3,[4,[5,6,7]]]],8,9]", "[1,[2,[3,[4,[5,6,0]]]],8,9]"],             1),
            (["[[8,[[7]]]]",                 "[[[[8]]]]"],                               1),
            (["[[8,[[7]]]]",                 "[[[[8],[3]]]]"],                           -1),
            (["[1,2,3,[1,2,3],4,1]",         "[1,2,3,[1,2,3],4,0]"],                     1),
            (["[[[1,6,[1,9,0,9],6]]]",       "[[],[[[5,6,3],6,[6,5,3,3]],8,3],[],[4]]"], 1)
        ]

        return [
            DayTest(
                self,
                f"Example {input[0]} vs {input[1]} == {expected}",
                input,
                expected,
                lambda s: self.compare(s[0][0], s[0][1])
            )
            for (input, expected) in tests]

    @property
    def expected_results(self):
        return {
            "task1_example": 13,
            "task1": 6484,
            "task2_example": 140,
            "task2": 19305
        }

    def compare(self, lhs, rhs):
        types = (lhs.__class__, rhs.__class__)
        if types == (int, int):
            if lhs < rhs:
                return -1
            elif lhs > rhs:
                return 1
            else:
                return 0
        elif types == (list, int):
            return self.compare(lhs, [rhs])
        elif types == (int, list):
            return self.compare([lhs], rhs)
        elif types == (list, list):
            lhs_len = len(lhs)
            rhs_len = len(rhs)

            result = 0
            for i in range(min(lhs_len, rhs_len)):
                result = self.compare(lhs[i], rhs[i])
                if result:
                    break

            if result == 0:
                return self.compare(lhs_len, rhs_len)

            return result

    def task1(self, input):
        result = 0

        for idx, task in enumerate(input):
            if self.compare(task[0], task[1]) == -1:
                result += (idx + 1)
        return result

    def task2(self, input):
        key_start = [[2]]
        key_end = [[6]]

        all_packets = flatten(input)
        all_packets.extend([key_start, key_end])

        all_packets.sort(key=functools.cmp_to_key(self.compare))

        return (all_packets.index(key_start) + 1) * (all_packets.index(key_end) + 1)


class DistressSignalParser(InputParser):
    def parse(self, input):
        return [(json.loads(c[0]), json.loads(c[1])) for c in chunks(input, 3)]
