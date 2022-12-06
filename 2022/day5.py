from math import ceil
from day import Day
from input_parser import InputParser
from utils import chunks


class Day5(Day):
    @property
    def title(self):
        return "Supply Stacks"

    @property
    def input_parser(self):
        return CreateMoverParser()

    @property
    def example_input(self):
        return """    [D]
[N] [C]
[Z] [M] [P]
 1   2   3

move 1 from 2 to 1
move 3 from 1 to 3
move 2 from 2 to 1
move 1 from 1 to 2"""

    @property
    def expected_results(self):
        return {
            "task1_example": "CMZ",
            "task1": "SPFMVDTZT",
            "task2_example": "MCD",
            "task2": "ZFSJBPRFP"
        }

    def task1(self, input):
        stacks = input[0]
        moves = input[1]

        for move in moves:
            for _ in range(move[0]):
                stacks[move[2] - 1].append(stacks[move[1] - 1][-1])
                stacks[move[1] - 1] = stacks[move[1] - 1][:-1]

        return ''.join(map(lambda x: x[-1], stacks))

    def task2(self, input):
        stacks = input[0]
        moves = input[1]

        for move in moves:
            stacks[move[2] - 1].extend(stacks[move[1] - 1][-move[0]:])
            stacks[move[1] - 1] = stacks[move[1] - 1][:-move[0]]

        return ''.join(map(lambda x: x[-1], stacks))


class CreateMoverParser(InputParser):
    def parse(self, input):
        start_state = []
        moves = []

        gathering_start_state = True
        for line in input:
            if line == "":
                gathering_start_state = False
            else:
                if gathering_start_state:
                    start_state.insert(0, line)
                else:
                    parts = line.split(" ")
                    moves.append((int(parts[1]), int(parts[3]), int(parts[5])))

        stacks = []
        for _ in range(ceil(len(start_state[0]) / 4)):
            stacks.append([])

        for row in start_state[1:]:
            for col, value in enumerate(chunks(row, 4)):
                value = value.strip()
                if len(value) == 0:
                    continue

                stacks[col].append(value[1])

        return stacks, moves
