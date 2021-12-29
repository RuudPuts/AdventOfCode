from day import Day
from input_parser import ConvertToIntParser
import sys

from utils import windows

class Day1(Day):
    @property
    def title(self):
        return "Sonar Sweep"

    @property
    def input_parser(self):
        return ConvertToIntParser()

    def task1(self, input):
        last_input = sys.maxsize
        increases = 0

        for i in input:
            if i > last_input:
                increases += 1
            last_input = i


        return increases

    def task2(self, input):
        window_size = 3
        last_sum = sys.maxsize
        increases = 0

        for window in windows(input, window_size):
            window_sum = sum(window)
            if window_sum > last_sum:
                increases += 1
            last_sum = window_sum

        return increases