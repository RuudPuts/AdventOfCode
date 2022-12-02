from day import Day
from input_parser import InputParser
from enum import Enum

class Day2(Day):
    @property
    def title(self):
        return "Rock Paper Scissors"

    @property
    def input_parser(self):
        return RockPaperScissorsParser()

    @property
    def example_input(self):
        return """A Y
B X
C Z"""

    @property
    def expected_results(self):
        return {
            "task1_example": 15,
            "task1": 9759,
            "task2_example": 12,
            "task2": 12429
        }

    MOVE_ROCK = 1
    MOVE_PAPER = 2
    MOVE_SCISSORS = 3

    RESULT_LOST = 0
    RESULT_DRAW = 3
    RESULT_WIN = 6

    def play(self, other_move, my_move):
        if other_move == my_move:
            return Day2.RESULT_DRAW

        if (other_move + my_move) == (Day2.MOVE_ROCK + Day2.MOVE_SCISSORS):
            if other_move == Day2.MOVE_ROCK:
                return Day2.RESULT_LOST
            return Day2.RESULT_WIN

        if other_move > my_move:
            return Day2.RESULT_LOST

        return Day2.RESULT_WIN

    def task1(self, input):
        move_map = {
            'A': Day2.MOVE_ROCK,
            'B': Day2.MOVE_PAPER,
            'C': Day2.MOVE_SCISSORS,

            'X': Day2.MOVE_ROCK,
            'Y': Day2.MOVE_PAPER,
            'Z': Day2.MOVE_SCISSORS,
        }

        score = 0
        for moves in input:
            my_move = move_map[moves[1]]
            result = self.play(move_map[moves[0]], my_move)
            score = score + my_move + result

        return score

    def resolve(self, other_move, outcome):
        if outcome == Day2.RESULT_DRAW:
            return other_move

        if outcome == Day2.RESULT_WIN:
            if other_move == Day2.MOVE_SCISSORS:
                return Day2.MOVE_ROCK
            return other_move + 1

        if outcome == Day2.RESULT_LOST:
            if other_move == Day2.MOVE_ROCK:
                return Day2.MOVE_SCISSORS
            return other_move - 1

    def task2(self, input):
        move_map = {
            'A': Day2.MOVE_ROCK,
            'B': Day2.MOVE_PAPER,
            'C': Day2.MOVE_SCISSORS
        }

        result_map = {
            'X': Day2.RESULT_LOST,
            'Y': Day2.RESULT_DRAW,
            'Z': Day2.RESULT_WIN,
        }

        score = 0
        for moves in input:
            result = result_map[moves[1]]
            my_move = self.resolve(move_map[moves[0]], result)
            score = score + my_move + result

        return score


class RockPaperScissorsParser(InputParser):
    def parse(self, input):
        return [(line[0], line[-1]) for line in input]
