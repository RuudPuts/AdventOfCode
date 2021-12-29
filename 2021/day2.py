from day import Day
from input_parser import InputParser
import re

class Day2(Day):
    @property
    def title(self):
        return "Dive!"

    @property
    def input_parser(self):
        return DirectionsParser()

    def task1(self, input):
        sub = Submarine()
        sub.move_part1(input)

        return sub.horizontal * sub.depth

    def task2(self, input):
        sub = Submarine()
        sub.move_part2(input)

        return sub.horizontal * sub.depth

class Submarine:
    horizontal = 0
    depth = 0
    aim = 0

    def move_part1(self, commands):
        for command in commands:
            if command.direction == "forward":
                self.horizontal += command.units
            elif command.direction == "up":
                self.depth -= command.units
            elif command.direction == "down":
                self.depth += command.units

    def move_part2(self, commands):
        for command in commands:
            if command.direction == "forward":
                self.horizontal += command.units
                self.depth += self.aim * command.units
            elif command.direction == "up":
                self.aim -= command.units
            elif command.direction == "down":
                self.aim += command.units


class Command:
    def __init__(self, direction, units):
        self.direction = direction
        self.units = units

class DirectionsParser(InputParser):
    def parse_line(self, line):
        match = re.match(r"(\w*) (\d)", line)

        return Command(match.group(1), int(match.group(2)))

    def parse(self, input):
        return list(map(self.parse_line, input))