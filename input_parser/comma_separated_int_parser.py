from input_parser.convert_to_int_parser import ConvertToIntParser

class CommaSeparatedIntParser(ConvertToIntParser):
    def parse(self, input):
        input = input[0].split(',')

        return super().parse(input)