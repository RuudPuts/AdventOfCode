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
        vm = VirtualConsole()
        success = vm.run(input)
        if success:
            return vm.accumulator

        patchable_instructions = {}
        for offset, instruction in vm.instruction_history.items():
            if instruction.operation == 'jmp':
                patchable_instructions[offset] = instruction
        
        self.log("POSSIBLE PATCHES")
        for offset, instruction in patchable_instructions.items():
            self.log("  %d | %s %d" % (offset, instruction.operation, instruction.value))

        patch_try = 0
        while not success and patch_try < len(patchable_instructions):
            instruction_to_patch = list(patchable_instructions.items())[patch_try]
            patch_offset = instruction_to_patch[0]
            
            patched_instructions = input.copy()
            patched_instructions[patch_offset] = Instruction('nop', instruction_to_patch[1].value)

            success = vm.run(patched_instructions)
            patch_try += 1

        if success:
            patch = list(patchable_instructions.items())[patch_try]
            self.log("Found working patch: %d | %s %d" % (patch[0], patch[1].operation, patch[1].value))
        else:
            self.log("Exhausted all patch tries")

        return vm.accumulator

class VirtualConsole:
    accumulator = 0
    instruction_offset = 0
    instruction_history = {}

    def run(self, instructions):
        self.reset()

        while self.instruction_offset not in self.instruction_history.keys() and self.instruction_offset < len(instructions):
            instruction = instructions[self.instruction_offset]
            self.instruction_history[self.instruction_offset] = instruction

            self.run_next_instruction(instruction)

        return list(self.instruction_history.keys())[-1] == len(instructions) - 1

    def reset(self):
        self.accumulator = 0
        self.instruction_offset = 0
        self.instruction_history = {}

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