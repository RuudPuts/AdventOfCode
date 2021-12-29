from day import Day
from input_parser import CommaSeparatedIntParser
import sys

class Day7(Day):
    @property
    def title(self):
        return "The Treachery of Whales"

    @property
    def input_parser(self):
        return CommaSeparatedIntParser()

    def task1(self, input):
        return self.calculate_alignment_cost(input, self.cost_to_move_part1)

    def task2(self, input):
        return self.calculate_alignment_cost(input, self.cost_to_move_part2)

    def cost_to_move_part1(self, input, location):
        cost = 0
        for pos in input:
            cost += (max(pos, location) - min(pos, location))

        return cost

    def cost_to_move_part2(self, input, location):
        cost = 0
        for pos in input:
            cost += sum(list(range(1, (max(pos, location) - min(pos, location)) + 1)))

        return cost

    def calculate_alignment_cost(self, input, cost_calculator):
        upper_cost = 0
        lower_cost = 0
        center_cost = 0

        costs = {}

        upper = sys.maxsize
        lower = -sys.maxsize
        while upper - lower > 1:
            if upper == sys.maxsize:
                upper = max(input)
                lower = min(input)
                center = round((upper - lower) / 2)
            else:
                upper_diff = max(upper_cost, center_cost) - min(upper_cost, center_cost)
                lower_diff = max(lower_cost, center_cost) - min(lower_cost, center_cost)

                if upper_diff < lower_diff:
                    lower = center
                else:
                    upper = center
                center = round((upper - lower) / 2) + lower

            upper_cost = costs[upper] if upper in costs.keys() else cost_calculator(input, upper)
            costs[upper] = upper_cost

            lower_cost = costs[lower] if lower in costs.keys() else cost_calculator(input, lower)
            costs[lower] = lower_cost

            center_cost = costs[center] if center in costs.keys() else cost_calculator(input, center)
            costs[center] = center_cost

        return min(costs.values())