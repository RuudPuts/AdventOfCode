from abc import ABC, abstractmethod
import heapq
from typing import Generic, TypeVar

from utils.grid import Grid


_T = TypeVar("_T")


# @dataclass
class PathNode(Generic[_T]):
    # node: _T
    # cost: int
    # origin: PathNode[_T]

    def __init__(self, node: _T, cost: int, origin):  #: PathNode[_T]):
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

    @abstractmethod
    def cost(self, pn: PathNode[_T]):
        pass

    def find_path(self, start: _T, end: _T):
        visited: dict[_T: int] = {}

        queue = [PathNode(start, 0, None)]
        heapq.heapify(queue)

        while queue:
            path_node = heapq.heappop(queue)

            if path_node.node in visited and visited[path_node.node] < path_node.cost:
                continue

            visited[path_node.node] = path_node.cost

            if path_node.node == end:
                print(f"Queue: {len(queue)}")
                for f in queue:
                    print(f"   {f.node}")
                return path_node

            for pn in self.neighbours(path_node):
                if pn in queue:
                    print("✅")
                heapq.heappush(queue, pn)

            if len(queue) > 100:
                for q in queue:
                    print(q.node)
                return None


class Dijkstra(PathFinder):
    def cost(self, pn: PathNode[_T]):
        return pn.cost
