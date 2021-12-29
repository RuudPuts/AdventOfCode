from day import Day
from input_parser import CommaSeparatedIntParser

class Day6(Day):
    @property
    def title(self):
        return "Lanternfish"

    @property
    def input_parser(self):
        return FishParser()

    def task1(self, input):
        return self.simulate(input, number_of_days = 80)

    def task2(self, input):
        return self.simulate(input, number_of_days = 256)

    def simulate(self, fish, number_of_days):
        for _ in range(number_of_days):
            fish = self.simulate_day(fish)

        return sum(fish.values())

    def simulate_day(self, input):
        offspring = input[0] if 0 in input.keys() else 0

        fish = {}
        for number, count in input.items():
            if number == 0:
                pass
            fish[number - 1] = count

        if -1 in fish.keys():
            del fish[-1]

        if 6 in fish.keys():
            fish[6] = fish[6] + offspring
        elif offspring > 0:
            fish[6] = offspring

        fish[8] = offspring

        return fish

class FishParser(CommaSeparatedIntParser):
    def parse(self, input):
        input = super().parse(input)

        fish = {}
        for value in set(input):
            fish[value] = input.count(value)

        return fish