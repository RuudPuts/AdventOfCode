from day import Day
from dataclasses import dataclass
from input_parser import IntGridParser
from utils import Grid, Vector2
from utils.pathfinding import Dijkstra, PathNode

class Day15(Day):
    @property
    def title(self):
        return "Chiton"

    @property
    def input_parser(self):
        return IntGridParser()

    def task1(self, input):
        # input.draw()



        # pathfinder = PathFinder(input, Vector2(0, 0), Vector2(input.width - 1, input.height - 1))
        # # pathfinder.draw()

        # run = 0
        # for id in range(1000000000):
        #     # print(id)
        #     run = id
        #     pathfinder.step()
        #     # pathfinder.draw()

        #     if pathfinder.is_complete:
        #         break

        # print(f"🔥🔥 Finished after {run + 1} steps, complete: {pathfinder.is_complete}")
        # print("Tracing...")
        # score, path = pathfinder.trace()
        # print("Path len ", len(path))
        # print("Score ", score)

        # # for p in path:
        # #     print(F"point: {p} -- {input.get(p)}")

        # # pathfinder.draw()
        # # pathfinder.print()

        # ## Not 371
        # ## Not 369
        # ## Not 376

        # ## Goal 373

        path_finder = TestPathFinder(input)
        end_node = path_finder.find_path(Vector2(0, 0), Vector2(input.width - 1, input.height - 1))

        return end_node.cost if end_node else -1

    def task2(self, input):
        return 0


@dataclass
class TestPathFinder(Dijkstra):
    grid: Grid

    def neighbours(self, pn: PathNode[Vector2]):
        return [PathNode(n, self.grid.get(n) + pn.cost, pn) for n in self.grid.neighbours4(pn.node)]

