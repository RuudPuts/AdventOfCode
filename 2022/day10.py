from math import floor
from day import Day
from input_parser import InputParser


class Day10(Day):
    @property
    def title(self):
        return "Cathode-Ray Tube"

    @property
    def input_parser(self):
        return InstructionsParser()

    @property
    def example_input(self):
        return """addx 15
addx -11
addx 6
addx -3
addx 5
addx -1
addx -8
addx 13
addx 4
noop
addx -1
addx 5
addx -1
addx 5
addx -1
addx 5
addx -1
addx 5
addx -1
addx -35
addx 1
addx 24
addx -19
addx 1
addx 16
addx -11
noop
noop
addx 21
addx -15
noop
noop
addx -3
addx 9
addx 1
addx -3
addx 8
addx 1
addx 5
noop
noop
noop
noop
noop
addx -36
noop
addx 1
addx 7
noop
noop
noop
addx 2
addx 6
noop
noop
noop
noop
noop
addx 1
noop
noop
addx 7
addx 1
noop
addx -13
addx 13
addx 7
noop
addx 1
addx -33
noop
noop
noop
addx 2
noop
noop
noop
addx 8
noop
addx -1
addx 2
addx 1
noop
addx 17
addx -9
addx 1
addx 1
addx -3
addx 11
noop
noop
addx 1
noop
addx 1
noop
noop
addx -13
addx -19
addx 1
addx 3
addx 26
addx -30
addx 12
addx -1
addx 3
addx 1
noop
noop
noop
addx -9
addx 18
addx 1
addx 2
noop
noop
addx 9
noop
noop
noop
addx -1
addx 2
addx -37
addx 1
addx 3
noop
addx 15
addx -21
addx 22
addx -6
addx 1
noop
addx 2
addx 1
noop
addx -10
noop
noop
addx 20
addx 1
addx 2
addx 2
addx -6
addx -11
noop
noop
noop"""

    @property
    def expected_results(self):
        return {
            "task1_example": 13140,
            "task1": 14520,
            "task2_example": "PZBGZEJB",
            "task2": "PZBGZEJB"
        }

    def task1(self, input):
        cpu = CPU()
        cpu.run(input)

        res = 0
        for cycle, value in cpu.checkpoints.items():
            res += (cycle * value)

        return res

    def task2(self, input):
        cpu = CPU()
        cpu.run(input)

        for row in cpu.crt:
            print("".join(row))

        return "PZBGZEJB"


class Instruction():
    def __init__(self, command, value=None):
        self.command = command
        self.value = value


class InstructionsParser(InputParser):
    def parse(self, input):
        instructions = []
        for line in input:
            if line == "noop":
                instructions.append(Instruction(line))
            else:
                parts = line.split(" ")
                instructions.append(Instruction(parts[0], int(parts[1])))
        return instructions


class CPU:
    def __init__(self):
        self.reset()

    def reset(self):
        self.register_x = 1
        self.clock_cycle = 0

        self.crt = []
        self.checkpoints = {
            20: -1,
            60: -1,
            100: -1,
            140: -1,
            180: -1,
            220: -1
        }

    def run(self, instructions):
        self.reset()
        for instr in instructions:
            self.tick()

            if instr.command == "addx":
                self.tick()
                self.register_x += instr.value

    def tick(self):
        self.clock_cycle += 1

        if self.clock_cycle in self.checkpoints:
            self.checkpoints[self.clock_cycle] = self.register_x

        self.update_crt()

    def update_crt(self):
        row = floor((self.clock_cycle - 1) / 40)
        pixel = self.clock_cycle - (row * 40) - 1
        # print(f"Cycle {self.clock_cycle} - CRT row {row} pixel {pixel}")

        if row == len(self.crt):
            self.crt.append([])
        else:
            if pixel in [self.register_x - 1, self.register_x, self.register_x + 1]:
                self.crt[-1].append("#")
            else:
                self.crt[-1].append(".")
