from day import Day
from input_parser import InputParser


class Day4(Day):
    @property
    def title(self):
        return "Camp Cleanup"

    @property
    def input_parser(self):
        return AssignmentsParser()

    @property
    def example_input(self):
        return """2-4,6-8
2-3,4-5
5-7,7-9
2-8,3-7
6-6,4-6
2-6,4-8"""

    @property
    def expected_results(self):
        return {
            "task1_example": 2,
            "task1": 515,
            "task2_example": 4,
            "task2": 883
        }

    def in_range(self, lhs, rhs):
        start = lhs.start >= rhs.start
        end = lhs.stop <= rhs.stop
        return start and end

    def task1(self, input):
        count = 0

        for assignments in input:
            left = assignments[0]
            right = assignments[1]

            if self.in_range(left, right) or self.in_range(right, left):
                count += 1

        return count

    def task2(self, input):
        count = 0

        for assignments in input:
            left = assignments[0]
            right = assignments[1]

            if len(set(left).intersection(right)) > 0:
                count += 1

        return count


class AssignmentsParser(InputParser):
    def parse(self, input):
        assignments = []
        for line in input:
            groups = line.split(",")
            left = groups[0].split("-")
            right = groups[1].split("-")
            assignments.append((
                range(int(left[0]), int(left[1]) + 1),
                range(int(right[0]), int(right[1]) + 1),
            ))

        return assignments
