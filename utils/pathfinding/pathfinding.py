# from abc import ABC, abstractmethod
# import heapq
# from typing import DefaultDict, Generic, TypeVar

# from utils.grid import Grid


# _T = TypeVar("_T")


# class PathNode(Generic[_T]):
#     def __init__(self, node: _T, cost: int, origin):
#         self.node = node
#         self.cost = cost
#         self.origin = origin

#     def __repr__(self):
#         return f"{self.__class__.__name__}({self.node=}, {self.cost=})"

#     def __lt__(self, other):
#         return self.cost < other.cost


# class PathFinder(ABC, Generic[_T]):
#     @abstractmethod
#     def neighbours(self, pn: PathNode[_T]):
#         pass

#     def find_path(self, start: _T, end: _T):
#         visited = {}
#         queue = []
#         node_parents = {}
#         node_costs = DefaultDict(lambda: float('inf'))

#         node_costs[start] = 0
#         heapq.heappush(queue, (0, PathNode(start, 0, None)))

#         while queue:
#             _, path_node = heapq.heappop(queue)

#             if path_node.node == end:
#                 break
#             visited[path_node.node] = path_node

#             for neighbour in self.neighbours(path_node):
#                 if neighbour.node in visited:
#                     continue

#                 new_cost = node_costs[path_node.node] + neighbour.cost
#                 if new_cost < node_costs[neighbour.node]:
#                     node_parents[neighbour.node] = path_node.node
#                     node_costs[neighbour.node] = new_cost
#                     heapq.heappush(queue, (new_cost, neighbour))

#         return node_costs[end]


# class Dijkstra(PathFinder):
#     pass


import heapq
from collections import defaultdict
from typing import DefaultDict
from PIL import Image, ImageFont, ImageDraw, ImageEnhance
from abc import ABC, abstractmethod
from utils.grid import Grid
from utils.vector2 import Vector2


class PathFinder(ABC):
    def __init__(self, tree):
        self.tree = tree

    @abstractmethod
    def weight(self, item):
        pass

    @abstractmethod
    def heuristic(self, item, end):
        pass

    @abstractmethod
    def neighbours(self, item):
        pass

    def find_path(self, start, end):
        visited = set()
        queue = []

        node_parents = {}
        node_costs = defaultdict(lambda: float('inf'))

        node_costs[start] = 0
        heapq.heappush(queue, (0, start))

        loop = 0
        while queue:
            loop += 1

            _, current_node = heapq.heappop(queue)

            visited.add(current_node)
            if current_node == end:
                break

            for neighbour in self.neighbours(current_node):
                if neighbour in visited:
                    continue
                # print(f"  Check neighbour {neighbour}")

                new_cost = node_costs[current_node] + self.weight(neighbour)
                # print(f"    New cost {new_cost}")
                if new_cost < node_costs[neighbour]:
                    node_parents[neighbour] = current_node
                    node_costs[neighbour] = new_cost
                    # queue.add(neighbour)
                    heuristic = self.heuristic(neighbour, end)
                    heapq.heappush(queue, (new_cost + heuristic, neighbour))

            # print(f"  Queue size: {len(queue)}")

            # self.visualize(loop, start, end, visited, queue)

        # path = []
        # if end in visited:
        #     # End reached, determine full path
        #     current = end
        #     while current in node_parents:
        #         path.append(current)
        #         current = node_parents[current]
        # else:
        #     print("🔥 Couldn't find path!")

        # self.visualize(loop, start, end, path, visited, queue, node_parents, node_costs)

        return node_costs[end]

    def visualize(self, cycle, start, end, path, visited, queue, node_parents, node_costs):
        node_size = 80 #20
        border_size = node_size / 20 #2
        visible_node_size = node_size - border_size * 2

        image_size = (self.tree.width * node_size, self.tree.height * node_size)
        image = Image.new('RGBA', image_size, "black")
        draw = ImageDraw.Draw(image)

        for y in range(self.tree.height):
            for x in range(self.tree.width):
                x_pixel = x * node_size + border_size
                y_pixel = y * node_size + border_size

                color = "grey"
                vector = Vector2(x, y)
                if vector == start:
                    color = "blue"
                elif vector == end:
                    color = "purple"
                elif Vector2(x, y) in visited:
                    color = "green"
                elif Vector2(x, y) in queue:
                    color = "orange"

                # if node_costs[vector] == max([v for v in node_costs.values() if v != float('inf')]):
                if vector in path:
                    if self.tree.get(vector) >= self.tree.get(node_parents[vector]):
                        # Going up
                        color = "pink"
                    else:
                        # Going down
                        color = "brown"

                draw.rectangle(((x_pixel, y_pixel), (x_pixel + visible_node_size, y_pixel + visible_node_size)), fill=color)
                draw.text((x_pixel, y_pixel), str(self.tree.get(vector)))
                draw.text((x_pixel, y_pixel + 10), str(node_costs[vector]), fill="red")

                if vector in node_parents:
                    x_elipse = x * node_size + node_size / 2
                    y_elipse = y * node_size + node_size / 2

                    parent = node_parents[vector]
                    if parent.x < vector.x:
                        x_elipse -= 24
                    elif parent.x > vector.x:
                        x_elipse += 24

                    if parent.y < vector.y:
                        y_elipse -= 24
                    elif parent.y > vector.y:
                        y_elipse += 24

                    draw.ellipse((x_elipse - 4, y_elipse - 4, x_elipse + 8, y_elipse + 8), fill = 'red')

        image.save(f"image_{cycle}.png", "PNG")