from input_parser.input_parser import InputParser
from utils.grid import Grid


class GridParser(InputParser):
    def parse(self, input):
        return Grid([[i for i in l] for l in input])
    

class IntGridParser(InputParser):
    def parse(self, input):
        return Grid([[int(i) for i in l] for l in input])
