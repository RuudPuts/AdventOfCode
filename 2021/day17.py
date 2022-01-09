from day import Day, DayTest
from input_parser import InputParser
from dataclasses import dataclass
from utils import Grid, flatten
import re

from utils.vector2 import Vector2


class Day17(Day):
    @property
    def title(self):
        return "Trick Shot"

    @property
    def input_parser(self):
        return RegionParser()

    @property
    def tests(self):
        tests = {
            'target area: x=20..30, y=-10..-5': (45, 112),
            'input': (5778, 2576)
        }

        return flatten([[
            DayTest(
                self,
                f"Task 1 {input} == {expected[0]}",
                [input],
                expected[0],
                lambda s: self.task1(s)
            ),
            DayTest(
                self,
                f"Task 2 {input} == {expected[1]}",
                [input],
                expected[1],
                lambda s: self.task2(s)
            )
            ] for input, expected in tests.items()])

    def task1(self, input):
        trajectory_region = self.determine_trajectory_region(input)

        return int((min(trajectory_region.y) * (min(trajectory_region.y) + 1) / 2))

    def task2(self, input):
        trajectory_region = self.determine_trajectory_region(input)

        hits = 0
        for x in trajectory_region.x:
            for y in trajectory_region.y:
                if self.simulate_trajectory(x, y, input):
                    hits += 1
        return hits

    def determine_trajectory_region(self, target):
        # // The min X velocity is the lowest velocity that will come to a standstill at the start of the target.
        # val minX = (1..target.min.x).first { it * (it + 1) / 2 >= target.min.x }
        for i in range(1, max(target.x)):
            if i * (i + 1) / 2 >= min(target.x):
                x_min = i
                break

        # The x should not overshoot the target in 1 step
        x_max = max(target.x)

        # The y should not overshoot the target in 1 step
        y_min = min(target.y)

        # The trajectory is parabolic, thus will never exceed the min y
        y_max = -y_min - 1

        return Region(range(x_min, x_max + 1), range(y_min, y_max + 1))

    def simulate_trajectory(self, velocity_x, velocity_y, target):
        probe = Probe(velocity_x, velocity_y)

        while not (probe.path[-1].x in target.x and probe.path[-1].y in target.y):
            probe.simulate_step()

            if probe.path[-1].x > target.x[-1]:
                # print(f"{probe.path[-1]} overshoots X")
                return None

            if probe.path[-1].y < target.y[0]:
                # print(f"{probe.path[-1]} overshoots Y")
                return None

        # self.print_trajectory(target, probe)

        return probe.path

    def print_trajectory(self, target, probe):
        y_offset = max([p.y for p in probe.path])
        width = max(target.x) + 1
        height = abs(min(target.y) - y_offset) + 1

        grid = Grid(width=width * 2, height=height * 2, initial_value='.')

        for x in target.x:
            for y in target.y:
                grid.set(Vector2(x, probe.path[0].y - y + y_offset), 'T')

        grid.set(probe.path[0].offset_by(0, y_offset), 'S')
        for p in probe.path[1:]:
            point = Vector2(p.x, probe.path[0].y - p.y + y_offset)
            grid.set(point, '#')

        grid.print()


class Probe:
    def __init__(self, velocity_x, velocity_y):
        self.x = 0
        self.y = 0
        self.velocity_x = velocity_x
        self.velocity_y = velocity_y
        self.path = [Vector2(self.x, self.y)]

    @property
    def max_y(self):
        return max([p.y for p in self.path])

    def simulate_step(self):
        # The probe's `x` position increases by its `x` velocity.
        self.x += self.velocity_x
        # The probe's `y` position increases by its `y` velocity.
        self.y += self.velocity_y

        self.path.append(Vector2(self.x, self.y))

        # Due to drag, the probe's `x` velocity changes by `1` toward the value `0`; that is,
        # it decreases by `1` if it is greater than `0`,
        if self.velocity_x > 0:
            self.velocity_x -= 1
        # increases by `1` if it is less than `0`, or does not change if it is already `0`.
        elif self.velocity_x < 0:
            self.velocity_x += 1
        # Due to gravity, the probe's `y` velocity decreases by `1`.
        self.velocity_y -= 1





@dataclass
class Region:
    x: range
    y: range


class RegionParser(InputParser):
    def parse(self, input):
        regex = r".*?x=(-?\d+)..(-?\d+), y=(-?\d+)..(-?\d+)$"
        match = re.match(regex, input[0])

        return Region(
            range(int(match.group(1)), int(match.group(2)) + 1),
            range(int(match.group(3)), int(match.group(4)) + 1)
        )
