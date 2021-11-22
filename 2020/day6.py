from os import SCHED_OTHER
from day import Day
from input_parser.split_blank_line_parser import SplitBlankLineParser

class Day6(Day):
    def title(self):
        return "Custom Customs"

    def input_parser(self):
        return SplitBlankLineParser()

    def task1(self, input):
        score = 0
        for group in input:
            combined = ''.join(group)
            score += len(set(combined))

        return score

    def task2(self, input):
        score = 0
        for group in input:
            all_answers = ''.join(group)

            for question in set(all_answers):
                if all_answers.count(question) == len(group):
                    score += 1

        return score