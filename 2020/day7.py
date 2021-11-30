from day import Day
from input_parser import InputParser
import re

class Day7(Day):
    def title(self):
        return "Handy Haversacks"

    def input_parser(self):
        return LuggageRuleParser()

    def task1(self, input):
        allowed_results = list(input.keys())
        results = []
        
        cache = {}
        targets = ["shiny gold"]
        while len(targets) > 0:
            new_targets = []

            for target in targets:
                if target in cache.keys():
                    resolved = cache[target]
                else:
                    resolved = self.resolve_bag_parents(target, input)
                    cache[target] = resolved

                for r in resolved:
                    if r in allowed_results:
                        results.append(r)
                new_targets += resolved

            targets = list(set(new_targets))

        return len(set(results))

    def resolve_bag_parents(self, target, rules):
        results = []
        for bag, contains in rules.items():
            if target in list(map(lambda x: x['bag'], contains)):
                results.append(bag)

        return results

    def task2(self, input):
        return self.count_bag_contents(input, "shiny gold")

    def count_bag_contents(self, input, bag, result = []):
        result.append(bag)
        for c in input[bag]:
            for _ in range(0, c['count']):
                self.count_bag_contents(input, c['bag'], result)

        return len(result) - 1

class LuggageRuleParser(InputParser):
    def parse_rule(self, line):
        bag_match = re.match(r"(.*?) bags contain ", line)
        bag = bag_match.group(1)
        
        contains_string = line[bag_match.span()[1]:]
        contains_matches = re.findall(r"(\d) (.*?) bag|bags\,|\.", contains_string)[:-1]
        contains = list(map(lambda x: { 'bag' : x[1], 'count': int(x[0]) }, contains_matches))

        return (bag, contains)

    def parse(self, input):
        rules = {}
        for rule in list(map(self.parse_rule, input)):
            rules[rule[0]] = rule[1]

        return rules
