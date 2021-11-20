from input_parser.input_parser import InputParser

class ConvertToListParser(InputParser):
    def parse(self, input):
        return list(map(lambda l: list(l), input))