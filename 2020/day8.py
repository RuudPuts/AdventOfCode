from day import Day
from input_parser.input_parser import InputParser
import re

class Day8(Day):
    def title(self):
        return "Handheld Halting"

    def input_parser(self):
        return IntructionsParser()

    def task1(self, input):
        vm = VirtualConsole()
        vm.run(input)

        return vm.accumulator

    def task2(self, input):
        raise Exception("Task failed")

class VirtualConsole:
    instruction_offset = 0
    instruction_history = []
    accumulator = 0

    def run(self, instructions):
        while self.instruction_offset not in self.instruction_history:
            instruction = instructions[self.instruction_offset]
            self.instruction_history.append(self.instruction_offset)

            self.run_next_instruction(instruction)

    def run_next_instruction(self, instruction):
        if instruction.operation == 'acc':
            self.accumulator += instruction.value
            self.instruction_offset += 1
        elif instruction.operation == 'jmp':
            self.instruction_offset += instruction.value
        else:
            self.instruction_offset += 1

class Instruction:
    def __init__(self, operation, value):
        self.operation = operation
        self.value = value


class IntructionsParser(InputParser):
    def parse_instruction(self, line):
        match = re.match(r"(\w{3}) ([+|-]\d+)$", line)

        return Instruction(match.group(1), int(match.group(2)))

    def parse(self, input):
        return list(map(self.parse_instruction, input))