from day import Day
from input_parser import InputParser
from collections import defaultdict, namedtuple, Counter
from utils import flatten

class Day8(Day):
    didget_for_segments = {
        2: 1,
        4: 4,
        3: 7,
        7: 8,
    }

    segments_for_diget = [
        [0, 1, 2, 4, 5, 6],    # 0
        [2, 5],                # 1
        [0, 2, 3, 4, 6],       # 2
        [0, 2, 3, 5, 6],       # 3
        [1, 2, 3, 5],          # 4
        [0, 1, 3, 5, 6],       # 5
        [0, 1, 3, 4, 5, 6],    # 6
        [0, 2, 5],             # 7
        [0, 1, 2, 3, 4, 5, 6], # 8
        [0, 1, 2, 3, 5, 6],    # 9
    ]

    @property
    def title(self):
        return "Seven Segment Search"

    @property
    def input_parser(self):
        return SegmentDisplayParser()

    def task1(self, input):
        all_outputs = flatten(list(map(lambda x: x.outputs, input)))

        return len(list(filter(lambda x: len(x) in self.didget_for_segments.keys(), all_outputs)))

    def task2(self, input):
        results = []

        for record in input:
            # print(" ".join(record.inputs))
            config = self.determine_display_config(record.inputs)
            output = int(''.join(list(map(lambda x: str(self.get_output_value(x, config)), record.outputs))))
            # print("%s: %s" % (' '.join(record.outputs), output))
            # print("")
            results.append(output)

        return sum(results)

    def determine_display_config(self, data):
        inputs = {}
        for x in data:
            inputs.setdefault(len(x), []).append(sorted(x))

        digit1_segments = inputs[2][0]
        digit4_segments = inputs[4][0]
        digit7_segments = inputs[3][0]

        segment_options = defaultdict(list)

        ## Right top segment
        segment_options[2] = digit1_segments
        ## Right bottom segment
        segment_options[5] = digit1_segments
        ## Top segment
        segment_options[0] = [x for x in digit7_segments if x not in digit1_segments][0]
        ## Left top segment
        segment_options[1] = [x for x in digit4_segments if x not in digit1_segments]
        ## Center segment
        segment_options[3] = segment_options[1]
        ## Bottom segment
        bottom_data = "".join(list(map(lambda x: "".join(x), inputs[5])))
        for c in flatten(segment_options.values()):
            bottom_data = bottom_data.replace(c, '')
        bottom_data = Counter(bottom_data)
        segment_options[6] = max(bottom_data, key=bottom_data.get)
        ## Left bottom segment
        segment_options[4] = [x for x in inputs[7][0] if x not in flatten(segment_options.values())][0]
        ## Resolve top left & center
        char_count = defaultdict(int)
        for char in filter(lambda x: x in segment_options[3], flatten(inputs[5])):
            char_count[char] += 1
        segment_options[3] = max(char_count, key=char_count.get)
        segment_options[1].remove(segment_options[3])
        segment_options[1] = segment_options[1][0]
        ## Resolve right top & right bottom
        if sorted(list(map(lambda x: segment_options[x][0], self.segments_for_diget[5]))) in flatten(inputs.values()):
            segment_options[5] = segment_options[2][0]
            segment_options[2] = segment_options[2][1]
        else:
            segment_options[2] = segment_options[5][0]
            segment_options[5] = segment_options[5][1]

        return dict((v, k) for k, v in segment_options.items())

    def get_output_value(self, output, config):
        resolved = sorted(list(map(lambda x: config[x], output)))
        return self.segments_for_diget.index(resolved)

    def print_options(self, options):
        print()
        print("------------")
        print()
        print("    " + "/".join(options[0]))
        print()
        print("/".join(options[1]) + "\t" + "/".join(options[2]))
        print()
        print("   " + "/".join(options[3]))
        print()
        print("/".join(options[4]) + "\t" + "/".join(options[5]))
        print()
        print("    " + "/".join(options[6]))
        print()
        print("------------")
        print()

Record = namedtuple('Record', 'inputs outputs')

class SegmentDisplayParser(InputParser):
    def parse_line(self, line):
        split = line.split(' | ')
        inputs = split[0].split(' ')
        outputs = split[1].split(' ')

        return Record(inputs = inputs, outputs = outputs)

    def parse(self, input):
        return list(map(self.parse_line, input))