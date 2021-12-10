from day import Day
from input_parser import InputParser
from collections import namedtuple
from utils import median

class Day10(Day):
    def title(self):
        return "Syntax Scoring"

    def input_parser(self):
        return NavigationSubsystemParser()

    def task1(self, input):
        input = list(filter(lambda x: not x.valid, input))
        
        return sum(list(map(lambda x: x.illegal_char_penalty, input)))

    def task2(self, input):
        input = list(filter(lambda x: x.valid, input))
        completion_scores = list(map(lambda x: x.completion_score, input))

        return median(sorted(completion_scores))

ValidationError = namedtuple('ValidationError', 'idx expected got')

class Chunk:
    TAGS = {
        '(': ')',
        '[': ']',
        '{': '}',
        '<': '>'
    }

    def __init__(self, data):
        self.data = data
        self.validate()

    def validate(self):
        history = []

        for idx in range(len(self.data)):
            char = self.data[idx]
            if char in self.TAGS.keys():
                history.append(char)
            if char in self.TAGS.values():
                open_tag = history.pop()
                expected = self.TAGS[open_tag]

                if char != expected:
                    self.valid = False
                    self.missing = list(map(lambda x: self.TAGS[x], reversed(history)))
                    self.complete = False
                    self.error = ValidationError(idx=idx, expected=expected, got=char)
                    return

        self.valid = True
        self.missing = list(map(lambda x: self.TAGS[x], reversed(history)))
        self.complete = len(history) == 0
        self.error = None

    @property
    def illegal_char_penalty(self):
        if self.valid:
            return 0

        penalties = {
            ')': 3,
            ']': 57,
            '}': 1197,
            '>': 25137
        }

        return penalties[self.error.got]

    @property
    def completion_score(self):
        scores = {
            ')': 1,
            ']': 2,
            '}': 3,
            '>': 4
        }

        score = 0
        for m in self.missing:
            score = score * 5 + scores[m]

        return score

class NavigationSubsystemParser(InputParser):
    def parse(self, input):
        return list(map(lambda x: Chunk(x), input))