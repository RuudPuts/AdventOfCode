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

    class Move(Enum):
        ROCK = 1
        PAPER = 2
        SCISSORS = 3

    class Result(Enum):
        LOST = 0
        DRAW = 3
        WIN = 6

    def play(self, other_move, my_move):
        if other_move == my_move:
            return Day2.Result.DRAW

        if (other_move.value + my_move.value) == (Day2.Move.ROCK.value + Day2.Move.SCISSORS.value):
            if other_move == Day2.Move.ROCK:
                return Day2.Result.LOST
            return Day2.Result.WIN

        if other_move.value > my_move.value:
            return Day2.Result.LOST

        return Day2.Result.WIN

    def task1(self, input):
        move_map = {
            'A': Day2.Move.ROCK,
            'B': Day2.Move.PAPER,
            'C': Day2.Move.SCISSORS,

            'X': Day2.Move.ROCK,
            'Y': Day2.Move.PAPER,
            'Z': Day2.Move.SCISSORS,
        }

        score = 0
        for moves in input:
            my_move = move_map[moves[1]]
            result = self.play(move_map[moves[0]], my_move)
            score = score + my_move.value + result.value

        return score

    def resolve(self, other_move, outcome):
        if outcome == Day2.Result.DRAW:
            return other_move.value

        if outcome == Day2.Result.WIN:
            if other_move == Day2.Move.SCISSORS:
                return Day2.Move.ROCK.value
            return other_move.value + 1

        if outcome == Day2.Result.LOST:
            if other_move == Day2.Move.ROCK:
                return Day2.Move.SCISSORS.value
            return other_move.value - 1

    def task2(self, input):
        move_map = {
            'A': Day2.Move.ROCK,
            'B': Day2.Move.PAPER,
            'C': Day2.Move.SCISSORS
        }

        result_map = {
            'X': Day2.Result.LOST,
            'Y': Day2.Result.DRAW,
            'Z': Day2.Result.WIN,
        }

        score = 0
        for moves in input:
            result = result_map[moves[1]]
            my_move = self.resolve(move_map[moves[0]], result)
            score = score + my_move + result.value

        return score


class RockPaperScissorsParser(InputParser):
    def parse(self, input):
        return [(line[0], line[-1]) for line in input]
