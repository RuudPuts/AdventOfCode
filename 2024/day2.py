from day import Day
from input_parser import InputParser


class Day2(Day):
    @property
    def title(self):
        return "Red-Nosed Reports"

    @property
    def input_parser(self):
        return ReportsParser()

    @property
    def example_input(self):
        return """7 6 4 2 1
1 2 7 8 9
9 7 6 2 1
1 3 2 4 5
8 6 4 4 1
1 3 6 7 9"""

    @property
    def expected_results(self):
        return {
            "task1_example": 2,
            "task1": 257,
            "task2_example": 4,
            "task2": 328
        }

    def task1(self, input):
        results = [self.check_report(r) for r in input]
        return len(list(filter(lambda x: x, results)))
    
    def check_report(self, report):
        dir = ">" if report[0] < report[1] else "<"
        for i in range(1, len(report)):
            if dir == ">" and report[i] < report[i-1]:
                return False
            elif dir == "<" and report[i] > report[i-1]:
                return False
            
            diff = abs(report[i] - report[i-1])
            if diff < 1 or diff > 3:
                return False
        
        return True

    def task2(self, input):
        results = { idx: self.check_report(r) for idx, r in enumerate(input) }
        
        for idx, result in results.items():
            if result:
                continue

            report = input[idx]
            for i in range(len(report)):
                new_report = report[:i] + report[i+1:]
                if self.check_report(new_report):
                    results[idx] = True
                    break

        return len(list(filter(lambda x: x, results.values())))


class ReportsParser(InputParser):
    def parse(self, input):
        return [[int(i) for i in line.split()] for line in input]