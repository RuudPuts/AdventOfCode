from day import Day
from input_parser import InputParser
from math import floor, prod

class Day11(Day):
    @property
    def title(self):
        return "Monkey in the Middle"

    @property
    def input_parser(self):
        return MonkeyParser()

    @property
    def example_input(self):
        return """Monkey 0:
  Starting items: 79, 98
  Operation: new = old * 19
  Test: divisible by 23
    If true: throw to monkey 2
    If false: throw to monkey 3

Monkey 1:
  Starting items: 54, 65, 75, 74
  Operation: new = old + 6
  Test: divisible by 19
    If true: throw to monkey 2
    If false: throw to monkey 0

Monkey 2:
  Starting items: 79, 60, 97
  Operation: new = old * old
  Test: divisible by 13
    If true: throw to monkey 1
    If false: throw to monkey 3

Monkey 3:
  Starting items: 74
  Operation: new = old + 3
  Test: divisible by 17
    If true: throw to monkey 0
    If false: throw to monkey 1"""

    @property
    def expected_results(self):
        return {
            "task1_example": 10605,
            "task1": 112221,
            "task2_example": 2713310158,
            "task2": 25272176808
        }

    def run(self, monkeys, rounds, confidence_factor, common_divider=0):
        for _ in range(0, rounds):
            for monkey in monkeys:
                for item in monkey.items:
                    updated_item = monkey.inspect(item)

                    if confidence_factor > 0:
                        updated_item = updated_item // confidence_factor

                    if common_divider > 0:
                        updated_item %= common_divider

                    if monkey.check(updated_item):
                        monkeys[monkey.success_forward].items.append(updated_item)
                    else:
                        monkeys[monkey.failed_forward].items.append(updated_item)
                monkey.items = []

        return sorted(monkeys, key=lambda m: m.inspect_count, reverse=True)

    def task1(self, input):
        sorted_monkeys = self.run(input, rounds=20, confidence_factor=3)

        return prod(map(lambda m: m.inspect_count, sorted_monkeys[:2]))

    def task2(self, input):
        common_divider = prod(map(lambda x: x.test, input))
        sorted_monkeys = self.run(input, rounds=10000, confidence_factor=1, common_divider=common_divider)

        return prod(map(lambda m: m.inspect_count, sorted_monkeys[:2]))


class Monkey:
    def __init__(self, id, items, operation, test, success_forward, failed_forward):
        self.id = id
        self.items = items
        self.operation = operation
        self.test = test
        self.success_forward = success_forward
        self.failed_forward = failed_forward

        self.inspect_count = 0

    def check(self, value):
        return value % self.test == 0

    def inspect(self, input):
        self.inspect_count += 1

        value = input
        if self.operation[-1].isnumeric():
            value = int(self.operation[-1])

        if self.operation[0] == "+":
            return input + value
        elif self.operation[0] == "-":
            return input - value
        elif self.operation[0] == "*":
            return input * value
        elif self.operation[0] == "/":
            return input / value
        else:
            raise Exception(f"Unsupported operation '{self.operation}'!")


class MonkeyParser(InputParser):
    MONKEY = "Monkey "
    START_ITEMS = "Starting items: "
    OPERATION = "Operation: new = old "
    TEST = "Test: divisible by "
    TEST_SUCCESS = "If true: throw to monkey "
    TEST_FAILED = "If false: throw to monkey "

    def parse(self, input):
        monkeys = []

        start_items = None
        operation = None
        test = None
        success_forward = None
        failed_forward = None

        for line in input:
            line = line.strip()
            if line == "":
                monkey = Monkey(
                    len(monkeys),
                    start_items,
                    operation,
                    test,
                    success_forward,
                    failed_forward
                )
                monkeys.append(monkey)

                start_items = None
                operation = None
                test = None
                success_forward = None
                failed_forward = None
            elif line.startswith(self.START_ITEMS):
                values = line.split(self.START_ITEMS)[1].split(", ")
                start_items = [int(value) for value in values]
            elif line.startswith(self.OPERATION):
                parts = line.split(self.OPERATION)[1].split(" ")
                # operation = (parts[0], int(parts[1]))
                operation = (parts[0], parts[1])
            elif line.startswith(self.TEST):
                test = int(line.split(self.TEST)[1])
            elif line.startswith(self.TEST_SUCCESS):
                success_forward = int(line.split(self.TEST_SUCCESS)[1])
            elif line.startswith(self.TEST_FAILED):
                failed_forward = int(line.split(self.TEST_FAILED)[1])
            else:
                if not line.startswith(self.MONKEY):
                    raise Exception(f"Failed to parse line '{line}'")

        monkey = Monkey(
            len(monkeys),
            start_items,
            operation,
            test,
            success_forward,
            failed_forward
        )
        monkeys.append(monkey)

        return monkeys
