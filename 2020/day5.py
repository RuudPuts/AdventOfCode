from day import Day
from input_parser import DummyParser

import math

class Day5(Day):
    @property
    def title(self):
        return "Binary Boarding"

    @property
    def input_parser(self):
        return DummyParser()

    def task1(self, input):
        highest_id = 0

        for data in input:
            self.log("Data:    " + data)
            row = self.resolve(data[0:7], 'F', 'B', 127)
            self.log("Row: " + str(row))
            column = self.resolve(data[-3:], 'L', 'R', 7)
            self.log("Column: " + str(column))
            seat_id = row * 8 + column
            self.log("ID: " + str(seat_id))
            self.log("")

            highest_id = max(highest_id, seat_id)

        return highest_id

    def task2(self, input):
        open_seats = []

        for column in range(0, 7): # Maybe +1?
            for row in range (1, 126): # Maybe +1?
                open_seats.append((column, row))


        for data in input:
            row = self.resolve(data[0:7], 'F', 'B', 127)
            column = self.resolve(data[-3:], 'L', 'R', 7)

            seat = (column, row)
            if seat in open_seats:
                open_seats.remove(seat)

        break_on_open_seat = False
        for row in range (1, 126): # Maybe +1?
            for column in range(0, 7): # Maybe +1?
                seat = (column, row)
                if seat not in open_seats and not break_on_open_seat:
                    break_on_open_seat = True

                if break_on_open_seat and seat in open_seats:
                    return row * 8 + column

        raise Exception("Task failed")

    def resolve(self, input, lower_char, higher_char, start_value):
        lower_bound = 0
        upper_bound = start_value

        for i in range(0, len(input) - 1):
            char = input[i]
            if char == lower_char:
                upper_bound = math.floor((upper_bound - lower_bound) / 2) + lower_bound
            elif char == higher_char:
                lower_bound = math.ceil((upper_bound - lower_bound) / 2) + lower_bound

        last_char = input[-1:]
        if last_char == lower_char:
            return lower_bound
        elif last_char == higher_char:
            return upper_bound