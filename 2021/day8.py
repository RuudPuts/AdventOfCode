from day import Day
from input_parser import InputParser
from collections import namedtuple
from utils import flatten

class Day8(Day):
    didget_for_segments = {
        2: 1,
        4: 4,
        3: 7,
        7: 8,
    }

    segments_for_diget = [
        [0, 1, 2, 4, 5, 6], # 0
        [2, 5], # 1
        [0, 2, 3, 4, 6], # 2
        [0, 2, 3, 5, 6], # 3
        [1, 2, 3, 5], # 4
        [0, 1, 3, 5, 6], # 5
        [0, 1, 3, 4, 5, 6], # 6
        [0, 2, 5], # 7
        [0, 1, 2, 3, 4, 5, 6], # 8
        [0, 1, 2, 3, 5, 6], # 9
    ]

    def title(self):
        return "Seven Segment Search"

    def input_parser(self):
        return SegmentDisplayParser()

    def task1(self, input):
        all_outputs = flatten(list(map(lambda x: x.outputs, input)))
        
        return len(list(filter(lambda x: len(x) in self.didget_for_segments.keys(), all_outputs)))

    def task2(self, input):
        for r in input:
            self.calculate(r)

        raise Exception("Task failed")

    def calculate(self, r):
        display_config = ['x'] * 7

        known_inputs = list(filter(lambda x: len(x) in self.didget_for_segments.keys(), r.inputs))
        known_inputs = sorted(known_inputs, key=len)
        guess_inputs = list(filter(lambda x: x not in known_inputs, r.inputs))

        for input in known_inputs:
            digit = self.didget_for_segments[len(input)]
            segments = self.segments_for_diget[digit]

            print("Known %s - %d - %s" % (input, digit, segments))
        
            for idx in range(len(input)):
                display_config[segments[idx]] = input[idx]

        print("")
        print(display_config)
        print("")

        if 'x' in display_config:
            raise Exception("DISPLAY NOT RESOLVED")

        for input in r.inputs:
            print("Input: ", input)
            segments = []
            for char in input:
                segments.append(display_config.index(char))
            
            digit = self.segments_for_diget.index(sorted(segments))

            print("Digit %d" % (digit))
            print("")

        results = []
        for output in r.outputs:
            print("Output: ", output)
            segments = []
            for char in output:
                segments.append(display_config.index(char))
            
            digit = self.segments_for_diget.index(sorted(segments))

            print("Digit %d" % (digit))
            print("")

            results.append(digit)

        return results

            


Record = namedtuple('Record', 'inputs outputs')

class SegmentDisplayParser(InputParser):
    def parse_line(self, line):
        split = line.split(' | ')
        inputs = split[0].split(' ')
        outputs = split[1].split(' ')

        return Record(inputs = inputs, outputs = outputs)

    def parse(self, input):
        input = [
            'be cfbegad cbdgef fgaecd cgeb fdcge agebfd fecdb fabcd edb | fdgacbe cefdb cefbgd gcbe',
            # 'edbfga begcd cbg gc gcadebf fbgde acbgfd abcde gfcbed gfec | fcgedb cgb dgebacf gc',
            # 'fgaebd cg bdaec gdafb agbcfd gdcbef bgcad gfac gcb cdgabef | cg cg fdcagb cbg',
            # 'fbegcd cbd adcefb dageb afcb bc aefdc ecdab fgdeca fcdbega | efabcd cedba gadfec cb',
            # 'aecbfdg fbg gf bafeg dbefa fcge gcbea fcaegb dgceab fcbdga | gecf egdcabf bgf bfgea',
            # 'fgeab ca afcebg bdacfeg cfaedg gcfdb baec bfadeg bafgc acf | gebdcfa ecba ca fadegcb',
            # 'dbcfg fgd bdegcaf fgec aegbdf ecdfab fbedc dacgb gdcebf gf | cefg dcbef fcge gbcadfe',
            # 'bdfegc cbegaf gecbf dfcage bdacg ed bedf ced adcbefg gebcd | ed bcgafe cdgba cbgef',
            # 'egadfb cdbfeg cegd fecab cgb gbdefca cg fgcdab egfdb bfceg | gbdfcae bgc cg cgb',
            # 'gcafb gcf dcaebfg ecagb gf abcdeg gaef cafbge fdbac fegbdc | fgae cfgab fg bagce',
        ]

        return list(map(self.parse_line, input))