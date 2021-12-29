from day import Day
from input_parser import SplitBlankLineParser

class Day6(Day):
    @property
    def title(self):
        return "Custom Customs"

    @property
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