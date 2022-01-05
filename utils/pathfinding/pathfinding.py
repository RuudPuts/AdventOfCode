from abc import ABC, abstractmethod
import heapq
from typing import DefaultDict, Generic, TypeVar

from utils.grid import Grid


_T = TypeVar("_T")


class PathNode(Generic[_T]):
    def __init__(self, node: _T, cost: int, origin):
        self.node = node
        self.cost = cost
        self.origin = origin

    def __repr__(self):
        return f"{self.__class__.__name__}({self.node=}, {self.cost=})"

    def __lt__(self, other):
        return self.cost < other.cost


class PathFinder(ABC, Generic[_T]):
    @abstractmethod
    def neighbours(self, pn: PathNode[_T]):
        pass

    def find_path(self, start: _T, end: _T):
        visited = {}
        queue = []
        node_parents = {}
        node_costs = DefaultDict(lambda: float('inf'))

        node_costs[start] = 0
        heapq.heappush(queue, (0, PathNode(start, 0, None)))

        while queue:
            _, path_node = heapq.heappop(queue)

            if path_node.node == end:
                break
            visited[path_node.node] = path_node

            for neighbour in self.neighbours(path_node):
                if neighbour.node in visited:
                    continue

                new_cost = node_costs[path_node.node] + neighbour.cost
                if new_cost < node_costs[neighbour.node]:
                    node_parents[neighbour.node] = path_node.node
                    node_costs[neighbour.node] = new_cost
                    heapq.heappush(queue, (new_cost, neighbour))

        return node_costs[end]


class Dijkstra(PathFinder):
    pass
