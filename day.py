from abc import ABC, abstractmethod
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

        return self.input_parser.parse(input)

    def log(self, message):
        if not self.debug:
            return

        print(message)
