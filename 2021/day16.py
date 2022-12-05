from collections import namedtuple
from day import Day, DayTest
from input_parser import InputParser
from dataclasses import dataclass

from utils import prod, flatten, StringReader


class Day16(Day):
    @property
    def title(self):
        return "Packet Decoder"

    @property
    def input_parser(self):
        return HexCharToBinaryParser()

    @property
    def example_input(self):
        return ""

    @property
    def expected_results(self):
        return {
            "task1_example": 2021,
            "task1": 906,
            "task2_example": -1,
            "task2": 819324480368
        }

    @property
    def tests(self):
        def version_sum_tests(self):
            tests = {
                '8A004A801A8002F478': 16,
                '620080001611562C8802118E34': 12,
                'C0015000016115A2E0802F182340': 23,
                'A0016C880162017C3686B18A3D4780': 31,
            }

            return [DayTest(
                self,
                f"Version sum of {input} == {expected}",
                [input],
                expected,
                lambda s: s.version_sum
            ) for input, expected in tests.items()]

        OperationTest = namedtuple('OperationTest', 'input packet result')

        def operation_tests(self):
            tests = [
                OperationTest('C200B40A82', SumOperationPacket, 3),
                OperationTest('04005AC33890', ProductOperationPacket, 54),
                OperationTest('880086C3E88112', MinimumOperationPacket, 7),
                OperationTest('CE00C43D881120', MaximumOperationPacket, 9),
                OperationTest('D8005AC2A8F0', LessThanOperationPacket, 1),
                OperationTest('F600BC2D8F', GreaterThanOperationPacket, 0),
                OperationTest('9C005AC2F8F0', EqualOperationPacket, 0),
                OperationTest('9C0141080250320F1802104A08', EqualOperationPacket, 1)
            ]

            for test in tests:
                yield [
                    DayTest(
                        self,
                        f"{test.packet.__name__} operation packet parsing",
                        [test.input],
                        test.packet,
                        lambda s: type(s)
                    ),
                    DayTest(
                        self,
                        f"{test.packet.__name__} operation result",
                        [test.input],
                        test.result,
                        lambda s: s.evaluate()
                    )
                ]

        return version_sum_tests(self) + flatten(operation_tests(self))

    def task1(self, input):
        return input.version_sum

    def task2(self, input):
        return input.evaluate()


class HexCharToBinaryParser(InputParser):
    def to_binary(self, char):
        return bin(int(char, 16))[2:].zfill(4)

    def parse(self, input):
        binary_input = ''.join([self.to_binary(c) for c in input[0]])

        return self.read_packet(StringReader(binary_input))

    def read_packet(self, input):
        version = int(input.read(3), 2)
        type = int(input.read(3), 2)

        if type == 0:
            return SumOperationPacket(version, subpackets=self.read_subpackets(input))
        elif type == 1:
            return ProductOperationPacket(version, subpackets=self.read_subpackets(input))
        elif type == 2:
            return MinimumOperationPacket(version, subpackets=self.read_subpackets(input))
        elif type == 3:
            return MaximumOperationPacket(version, subpackets=self.read_subpackets(input))
        elif type == 4:
            return LiteralValuePacket(version, self.read_literal_value(input))
        elif type == 5:
            return GreaterThanOperationPacket(version, subpackets=self.read_subpackets(input))
        elif type == 6:
            return LessThanOperationPacket(version, subpackets=self.read_subpackets(input))
        elif type == 7:
            return EqualOperationPacket(version, subpackets=self.read_subpackets(input))
        else:
            raise Exception(f"Unsupported packet type {type}")

    def read_literal_value(self, input):
        value = ''
        while True:
            data = input.read(5)
            value += data[1:]
            if data[0] == '0':
                break

        return int(value, 2)

    def read_subpackets(self, input):
        subpackets = []

        length_type = input.read(1)

        if length_type == '0':
            subpackets_length = int(input.read(15), 2)

            max_offset = input.offset + subpackets_length
            while input.offset < max_offset:
                subpackets.append(self.read_packet(input))
        elif length_type == '1':
            subpacket_count = int(input.read(11), 2)

            for _ in range(subpacket_count):
                subpackets.append(self.read_packet(input))
        else:
            raise Exception(f"Invalid length type {length_type}, expected 0 or 1")

        return subpackets

@dataclass
class Packet:
    version: int
    value: int = None
    subpackets: list[any] = None

    @property
    def version_sum(self):
        sum = self.version
        for p in (self.subpackets or []):
            sum += p.version_sum

        return sum

    def evaluate(self):
        return None


class OperationPacket(Packet):
    @property
    def subpackages_evaluated(self):
        return [p.evaluate() for p in self.subpackets]


class SumOperationPacket(OperationPacket):
    def evaluate(self):
        return sum(self.subpackages_evaluated)


class ProductOperationPacket(OperationPacket):
    def evaluate(self):
        return prod(self.subpackages_evaluated)


class LiteralValuePacket(OperationPacket):
    def evaluate(self):
        return self.value


class MinimumOperationPacket(OperationPacket):
    def evaluate(self):
        return min(self.subpackages_evaluated)


class MaximumOperationPacket(OperationPacket):
    def evaluate(self):
        return max(self.subpackages_evaluated)


class LessThanOperationPacket(OperationPacket):
    def evaluate(self):
        return 1 if self.subpackages_evaluated[0] < self.subpackages_evaluated[1] else 0


class GreaterThanOperationPacket(OperationPacket):
    def evaluate(self):
        return 1 if self.subpackages_evaluated[0] > self.subpackages_evaluated[1] else 0


class EqualOperationPacket(OperationPacket):
    def evaluate(self):
        return 1 if self.subpackets[0].evaluate() == self.subpackets[1].evaluate() else 0