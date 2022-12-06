from day import Day, DayTest
from input_parser import InputParser
from utils import flatten, windows


class Day6(Day):
    @property
    def title(self):
        return "Tuning Trouble"

    @property
    def input_parser(self):
        return InputParser()

    @property
    def example_input(self):
        return "mjqjpqmgbljsphdztnvjfqwrcgsmlb"

    @property
    def tests(self):
        tests = {
            'bvwbjplbgvbhsrlpgdmjqwftvncz': [5, 23],
            'nppdvjthqldpwncqszvftbrmjlhg': [6, 23],
            'nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg': [10, 29],
            'zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw': [11, 26],
            }

        return flatten([[
            DayTest(
                self,
                f"Task 1 {input} == {expected[0]}",
                [input],
                expected[0],
                lambda s: self.task1(s)
            ),
            DayTest(
                self,
                f"Task 2 {input} == {expected[1]}",
                [input],
                expected[1],
                lambda s: self.task2(s)
            )
        ] for input, expected in tests.items()])

    @property
    def expected_results(self):
        return {
            "task1_example": 7,
            "task1": 1965,
            "task2_example": 19,
            "task2": 2773
        }

    def run_task(self, line, chunk_size):
        for idx, char in enumerate(windows(line, chunk_size)):
            if len(set(char)) == chunk_size:
                return idx + chunk_size

        return None

    def task1(self, input):
        return self.run_task(input[0], 4)

    def task2(self, input):
        return self.run_task(input[0], 14)
