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
            "task2_example": -1,
            "task2": -1
        }

    def task1(self, input):
        start = Vector2(0, 0)
        head = start
        tail = head

        visited = set([tail])
        size = Vector2(6, 5)

        LOG = False

        def print_state(finished=False):
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
                        if point == head:
                            line.append("H")
                        elif point == tail:
                            line.append("T")
                        elif point == start:
                            line.append("s")
                        else:
                            line.append(".")
                lines.append("".join(line))

            print()
            for line in reversed(lines):
                print(line)
            print()

        if LOG:
            print("== Initial State ==")
            print_state()

        for action in input:
            dir = action[0]
            count = int(action[1])

            if LOG:
                print(f"== {dir} {count} ==")

            for itt in range(count):
                if LOG:
                    print(f"# {itt}")
                x_move = 0
                y_move = 0
                if dir == "R":
                    x_move = 1
                elif dir == "U":
                    y_move = 1
                elif dir == "L":
                    x_move = -1
                elif dir == "D":
                    y_move = -1

                old_head = head
                head = head.offset_by(x_move, y_move)

                if head != tail and head not in tail.adjacent8:
                    if LOG:
                        print(f"Move tail from {tail} to {old_head}")
                    tail = old_head
                    visited.add(tail)

                size.x = max(head.x + 1, size.x)
                size.y = max(head.y + 1, size.y)

                if LOG:
                    print_state()

        print_state(finished=True)

        return len(visited)

    def task2(self, input):
        return None


class InstructionsParser(InputParser):
    def parse(self, input):
        return list(map(lambda x: x.split(" "), input))
