from day import Day
from input_parser import InputParser
from utils import Vector2


class Day9(Day):
    @property
    def title(self):
        return "Rope Bridge"

    @property
    def input_parser(self):
        return InstructionsParser()

    @property
    def example_input(self):
        return """R 4
U 4
L 3
D 1
R 4
D 1
L 5
R 2"""

    @property
    def expected_results(self):
        return {
            "task1_example": 13,
            "task1": 6284,
            "task2_example": 1,
            "task2": 2661
        }

    def print_state(self, size, visited, start, rope, finished=False):
        lines = []
        for y in range(size.y):
            line = []
            for x in range(size.x):
                point = Vector2(x, y)
                if finished:
                    if point in visited:
                        line.append("#")
                    else:
                        line.append(".")
                else:
                    if point == rope[0]:
                        line.append("H")
                    elif point == rope[-1]:
                        line.append("T")
                    elif point in rope:
                        line.append(str(rope.index(point)))
                    elif point == start:
                        line.append("s")
                    else:
                        line.append(".")
            lines.append("".join(line))

        print()
        for line in reversed(lines):
            print(line)
        print()

    def traverse_path(self, actions, rope_length=2):
        movement = {
            "U": (0, 1),
            "D": (0, -1),
            "R": (1, 0),
            "L": (-1, 0)
        }

        def sign(number):
            if number > 0:
                return 1
            elif number < 0:
                return -1
            else:
                return 0

        start = Vector2(0, 0)
        rope = [start for _ in range(rope_length)]
        visited = set([start])

        size = Vector2(6, 5)

        for action in actions:
            dir = action[0]
            count = int(action[1])

            for _ in range(count):
                x_move, y_move = movement[dir]

                rope[0] = rope[0].offset_by(x_move, y_move)
                head = rope[0]

                for idx in range(1, len(rope)):
                    knot = rope[idx]
                    parent = rope[idx - 1]

                    x_delta = parent.x - knot.x
                    y_delta = parent.y - knot.y

                    if x_delta == 0 or y_delta == 0:
                        if abs(x_delta) >= 2:
                            rope[idx] = knot.offset_by(sign(x_delta), 0)
                        if abs(y_delta) >= 2:
                            rope[idx] = knot.offset_by(0, sign(y_delta))
                    elif (abs(x_delta), abs(y_delta)) != (1, 1):
                        rope[idx] = knot.offset_by(sign(x_delta), sign(y_delta))

                visited.add(rope[-1])

                size.x = max(head.x + 1, size.x)
                size.y = max(head.y + 1, size.y)

        return visited

    def task1(self, input):
        return len(self.traverse_path(input))

    def task2(self, input):
        return len(self.traverse_path(input, rope_length=10))


class InstructionsParser(InputParser):
    def parse(self, input):
        return list(map(lambda x: x.split(" "), input))
