from input_parser.input_parser import InputParser

class SplitBlankLineParser(InputParser):
    def parse(self, input):
        results = []
        
        chunk = []
        for line in input:
            if len(line.strip()) == 0 and len(chunk) > 0:
                results.append(chunk)
                chunk = []
            elif len(line.strip()) > 0:
                chunk.append(line)

        if len(chunk) > 0:
            results.append(chunk)

        return results
