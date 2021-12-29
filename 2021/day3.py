from day import Day
from input_parser import DummyParser

class Day3(Day):
    @property
    def title(self):
        return "Binary Diagnostic"

    @property
    def input_parser(self):
        return DummyParser()

    def task1(self, input):
        gamma = bin(int(self.most_common_bits(input), 2))
        epsilon = bin(int(self.most_common_bits(input, use_least_common_bit=True), 2))

        return int(gamma, 2) * int(epsilon, 2)

    def most_common_bits(self, input, use_least_common_bit = False):
        result = ""
        bin_length = len(input[0])

        for i in range(0, bin_length):
            bits = list(map(lambda x: int(x[i]), input))
            if sum(bits) > len(input) / 2:
                result += str(0 if use_least_common_bit else 1)
            else:
                result += str(1 if use_least_common_bit else 0)

        return result

    def task2(self, input):
        oxigen = bin(int(self.dig_bits(input), 2))
        co2 = bin(int(self.dig_bits(input, use_least_common_bit=True), 2))

        return int(oxigen, 2) * int(co2, 2)

    def dig_bits(self, input, use_least_common_bit=False):
        remaining = input.copy()
        bin_length = len(input[0])
        bit = 0

        while len(remaining) > 1 and bit < bin_length:
            bits = list(map(lambda x: int(x[bit]), remaining))

            if sum(bits) >= len(remaining) / 2:
                result = str(0 if use_least_common_bit else 1)
            else:
                result = str(1 if use_least_common_bit else 0)

            remaining = list(filter(lambda x: x[bit] == result, remaining))
            bit +=1

        return remaining[0]