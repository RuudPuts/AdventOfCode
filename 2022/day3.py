import string
from day import Day
from utils import chunks
from input_parser import InputParser

class Day3(Day):
    @property
    def title(self):
        return "Rucksack Reorganization"

    @property
    def input_parser(self):
        return InputParser()

    @property
    def example_input(self):
        return """vJrwpWtwJgWrhcsFMMfFFhFp
jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL
PmmdzqPrVvPwwTWBwg
wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn
ttgJtRGJQctTZtZT
CrZsJsPPZsGzwwsLwLmpwMDw"""

    @property
    def expected_results(self):
        return {
            "task1_example": 157,
            "task1": 7581,
            "task2_example": 70,
            "task2": 2525
        }

    def score(self, char):
        idx = string.ascii_lowercase.index(char.lower())
        if char.isupper():
            idx += 26
        return idx + 1

    def task1(self, input):
        score = 0
        for line in input:
            left, right = line[:len(line)//2], line[len(line)//2:]

            for char in set(set(left) & set(right)):
                score += self.score(char)

        return score

    def task2(self, input):
        score = 0
        for group in chunks(input, 3):
            overlaps = set(set(group[0]) & set(group[1]) & set(group[2]))
            for char in overlaps:
                score += self.score(char)

        return score
