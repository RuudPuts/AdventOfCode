from abc import ABC, abstractmethod
from dataclasses import dataclass
import os
import sys

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

    def test(self):
        for test in self.tests:
            print()
            print(f"    Testing '{test.description}'")
            test.evaluate()
            print(f"    {'✅' if test.success else '❌'} Test '{test.description}' {'succeeded!' if test.success else f'failed! Expected {test.expected}, got {test.result}' }")

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
