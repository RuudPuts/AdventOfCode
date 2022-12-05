from typing import DefaultDict
from day import Day
from input_parser import InputParser
from utils import flatten
from collections import defaultdict, deque


class Day12(Day):
    @property
    def title(self):
        return "Passage Pathing"

    @property
    def input_parser(self):
        return CaveConnectionParser()

    @property
    def example_input(self):
        return """start-A
start-b
A-c
A-b
b-d
A-end
b-end"""

    @property
    def expected_results(self):
        return {
            "task1_example": 10,
            "task1": 4549,
            "task2_example": 36,
            "task2": 120535
        }

    def task1(self, input):
        paths = 0
        queue = deque([("start", {"start", }), ])

        while queue:
            current, previous = queue.pop()
            for next in input[current]:
                if next == "end":
                    paths += 1
                elif next.lower() != next or next not in previous:
                    queue.append((next, previous | {next, }))

        return paths

    def task2(self, input):
        paths = 0
        queue = deque([("start", {"start", }, False), ])

        while queue:
            current, previous, previous_double = queue.pop()
            for next in input[current]:
                if next == "start":
                    continue

                if next == "end":
                    paths += 1
                else:
                    is_small = next.lower() == next

                    if not ((is_small and next in previous) and previous_double):
                        queue.append((next, previous | {next, }, previous_double or (is_small and next in previous)))

        return paths


class CaveConnectionParser(InputParser):
    def parse(self, input):
        data = defaultdict(set)
        for line in input:
            split = line.split('-')
            data[split[0]].add(split[1])
            data[split[1]].add(split[0])

        return data
