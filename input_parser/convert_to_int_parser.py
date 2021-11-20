from input_parser.input_parser import InputParser

class ConvertToIntParser(InputParser):
    def parse(self, input):
        return list(map(lambda x: int(x), input))