from day import Day
from input_parser import InputParser
import re

class Day4(Day):
    @property
    def title(self):
        return "Giant Squid"

    @property
    def input_parser(self):
        return BingoParser()

    @property
    def example_input(self):
        return """7,4,9,5,11,17,23,2,0,14,21,24,10,16,13,6,15,25,12,22,18,20,8,19,3,26,1

22 13 17 11  0
 8  2 23  4 24
21  9 14 16  7
 6 10  3 18  5
 1 12 20 15 19

 3 15  0  2 22
 9 18 13 17  5
19  8  7 25 23
20 11 10 24  4
14 21 16 12  6

14 21 17 24  4
10 16 15  9 19
18  8 23 26 20
22 11 13  6  5
 2  0 12  3  7"""

    @property
    def expected_results(self):
        return {
            "task1_example": 4512,
            "task1": 87456,
            "task2_example": 1924,
            "task2": 15561
        }

    def task1(self, input):
        numbers = input[0]
        boards = input[1]

        number_index = -1
        winning_board = None
        while winning_board is None and number_index < len(numbers):
            number_index += 1
            number = numbers[number_index]
            for b in boards:
                b.check_number(number)
                if b.has_won():
                    winning_board = b
                    break

        return numbers[number_index] * sum(winning_board.unchecked_numbers())

    def task2(self, input):
        numbers = input[0]
        remaining_boards = input[1]

        number_index = 0
        last_winning_board = None
        last_winning_number_idx = 0
        while len(remaining_boards) and number_index < len(numbers):
            number = numbers[number_index]
            for b in remaining_boards:
                b.check_number(number)

            for b in remaining_boards:
                if b.has_won():
                    last_winning_number_idx = number_index
                    last_winning_board = b
                    remaining_boards.remove(b)
            number_index += 1

        return numbers[last_winning_number_idx] * sum(last_winning_board.unchecked_numbers())

class BingoBoard:
    def __init__(self, idx, numbers):
        self.idx = idx
        self.numbers = numbers

        self.checked = []
        for row in numbers:
            self.checked.append(list(map(lambda x: False, row)))

    def check_number(self, number):
        for row in range(0, len(self.numbers)):
            for column in range(0, len(self.numbers[row])):
                if self.numbers[row][column] == number:
                    self.checked[row][column] = True

        return self.has_won

    def unchecked_numbers(self):
        numbs = []

        for row in range(0, len(self.numbers)):
            for column in range(0, len(self.numbers[row])):
                if self.checked[row][column] == False:
                    numbs.append(self.numbers[row][column])

        return numbs


    def has_won(self):
        for row in self.checked:
            if len(row) == row.count(True):
                return True

        for column_idx in range(0, len(self.checked[0])):
            column = list(map(lambda x: x[column_idx], self.checked))
            if len(column) == column.count(True):
                return True

        return False

class BingoParser(InputParser):
    def parse_board(self, idx, input):
        numbers = []
        for line in input:
            matches = re.findall(r"\d{1,}", line)
            numbers.append(list(map(lambda x: int(x), matches)))

        return BingoBoard(idx, numbers)

    def parse(self, input):
        numbers = []
        boards = []

        chunk = []
        for line in input:
            if line == '':
                if len(chunk) == 1:
                    numbers = list(map(lambda x: int(x), chunk[0].split(",")))
                else:
                    boards.append(self.parse_board(len(boards), chunk))
                chunk = []
            else:
                chunk.append(line)

        boards.append(self.parse_board(len(boards), chunk))

        return (numbers, boards)