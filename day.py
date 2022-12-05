from abc import ABC, abstractmethod
from dataclasses import dataclass
import os
import sys
import time

class Day(ABC):
    debug = False

    @property
    @abstractmethod
    def title(self):
        pass

    @property
    @abstractmethod
    def input_parser(self):
        pass

    @property
    @abstractmethod
    def example_input(self):
        pass

    @property
    @abstractmethod
    def expected_results(self):
        pass

    def test(self):
        # Day specific tests
        for test in self.tests:
            test_start = time.perf_counter()
            test.evaluate()
            test_end = time.perf_counter()
            test_duration = test_end - test_start
            print(f"    {'✅' if test.success else '❌'} Test '{test.description}' {'succeeded!' if test.success else f'failed! Expected {test.expected}, got {test.result}' } (took {test_duration * 1000:0.4f}ms)")
        if len(self.tests) > 0:
            print()

        # Default tests

        tests = [
            # Task 1
            DayTest(
                self,
                f"Task 1 == {self.expected_results['task1']}",
                ['input'],
                self.expected_results['task1'],
                lambda s: self.task1(s)
            ),
            # Task 2
            DayTest(
                self,
                f"Task 2 == {self.expected_results['task2']}",
                ['input'],
                self.expected_results['task2'],
                lambda s: self.task2(s)
            )
        ]

        if len(self.example_input) > 0:
            # Task 1
            tests.insert(0, DayTest(
                self,
                f"Task 1 example == {self.expected_results['task1_example']}",
                self.example_input.splitlines(),
                self.expected_results['task1_example'],
                lambda s: self.task1(s)
            ))

            # Task 2
            tests.insert(2, DayTest(
                self,
                f"Task 2 example == {self.expected_results['task2_example']}",
                self.example_input.splitlines(),
                self.expected_results['task2_example'],
                lambda s: self.task2(s)
            ))

        for test in tests:
            try:
                test_start = time.perf_counter()
                test.evaluate()
                test_end = time.perf_counter()
                test_duration = test_end - test_start
                print(f"    {'✅' if test.success else '❌'} Test '{test.description}' {'succeeded!' if test.success else f'failed! Expected {test.expected}, got {test.result}' } (took {test_duration * 1000:0.4f}ms)")

                if not test.success:
                    break
            except Exception as ex:
                print(f"    ❌ Test '{test.description}' failed! Exception occurred {ex}'")
                break


    @property
    def tests(self):
        return []

    @abstractmethod
    def task1(self, input):
        pass

    @abstractmethod
    def task2(self, input):
        pass

    @property
    def day(self):
        return self.__class__.__name__

    @property
    def number(self):
        return self.day.replace("Day", "")

    def read_input(self):
        path = sys.modules[self.__module__].__file__.replace(".py", "-input.txt")

        file = open(path, 'r')
        input = file.read().splitlines()
        file.close()

        return input

    def log(self, message):
        if not self.debug:
            return

        print(message)


@dataclass
class DayTest:
    day: Day
    description: str
    input: list[str]
    expected: any
    function: any

    result = False
    success = False

    def evaluate(self):
        if self.input == ['input']:
            input = self.day.input_parser.parse(self.day.read_input())
        else:
            input = self.day.input_parser.parse(self.input)

        self.result = self.function(input)
        self.success = self.result == self.expected

        return self
