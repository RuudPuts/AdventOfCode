from collections import namedtuple
from PIL import ImageFont
from utils.drawable import Drawable
from utils.heap import Heap, HeapItem
from utils.vector2 import Vector2
from utils.vector4 import Vector4


class PathFinder(Drawable):
    def __init__(self, grid, start_point, end_point):
        self.grid = grid
        self.start_point = start_point
        self.end_point = end_point
        self.open = Heap([HeapItem(start_point, score=0)])
        self.closed = dict()
        self.parents = dict()
        self.path = []

    def step(self):
        current_item = self.open.pop()
        current_point = current_item.data


        score = current_item.score + self.grid.get(current_point)
        for n in self.grid.neighbours(current_point, False):
            if item := self.open.get(n):
                if score <= item.score:
                    # print("🔥 Update open")
                    item.score = score
                    # if self.open.get(n).score != score:
                    #     print("🔥🔥 error updating open")
                    self.parents[item.data] = current_point
            elif n in self.closed:
                item = self.closed[n]
                if score <= item.score:
                    # print("🔥 Update closed")
                    item.score = score
                    # if self.closed[n].score != score:
                        # print("🔥🔥 error updating closed")
                    self.parents[item.data] = current_point
                    self.open.add(item)
            else:
                self.open.add(HeapItem(n, score=score))
                self.parents[n] = current_point


                    # if nb not in visited:
                    # new_dist = dist[cur_node[0], cur_node[1]] + grid[nb[0], nb[1]]
                    # if new_dist < dist[nb[0], nb[1]]:
                    #     dist[nb[0], nb[1]] = new_dist
                    #     heapq.heappush(node_list, (new_dist, nb))


        self.closed[current_point] = current_item

    @property
    def is_complete(self):
        return self.end_point in self.closed.keys()

    def trace(self):
        cost = 0
        if not self.is_complete:
            return cost, []

        print()
        print()
        print()

        path = [self.end_point]
        while self.start_point not in path:
            last_point = path[-1]
            # print(f"Cost {last_point}: {self.grid.get(last_point)}")
            cost += self.grid.get(last_point)
            path.append(self.parents[last_point])

        print()
        print()
        print()

        self.path = path

        # return (self.closed[self.end_point].score, list(reversed(path)))

        print(f"Calculated: {cost} - algo: {self.closed[self.end_point].score}")

        return cost, list(reversed(path))

    @property
    def filename(self):
        return "pathfinder"

    @property
    def image_size(self):
        return self.grid.image_size

    def background_color(self, point):
        if point == self.start_point:
            return "#f1c40f"
        if point == self.end_point:
            return "#9b59b6"
        if point in self.path:
            return "#2ecc71"
        # if self.open.holds(point):
        #     return "#2ecc71"
        # if point in self.closed.keys():
        #     return "#e74c3c"

        return "#000000"

    def draw_with(self, draw):
        print("Drawing backgrounds...")
        for y in range(self.grid.height):
            for x in range(self.grid.width):
                point = Vector2(x, y)

                rect = Vector4(point, 1, 1)
                rect = rect.scale(self.grid.image_scale)
                draw.rectangle(rect.shape, fill=self.background_color(point))

                # if point in self.path:
                #     rect = rect.rel_inset(0.75)
                #     draw.rectangle(rect.shape, fill="#2ecc71")

        print("Drawing scores...")
        for item in self.open:
            rect = Vector4(item.data, 1, 1)
            rect = rect.scale(self.grid.image_scale)
            rect = rect.offset(0, rect.height * 0.4)

            font = ImageFont.truetype("Arial", int(self.grid.image_scale / 8))
            draw.text((rect.center.x, rect.center.y), str(item.score), fill='black', anchor="mm", font=font)

        for item in self.closed.values():
            rect = Vector4(item.data, 1, 1)
            rect = rect.scale(self.grid.image_scale)
            rect = rect.offset(0, rect.height * 0.4)

            font = ImageFont.truetype("Arial", int(self.grid.image_scale / 8))
            draw.text((rect.center.x, rect.center.y), str(item.score), fill='black', anchor="mm", font=font)

        self.grid.draw_with(draw)

    def print(self):
        print()
        for y in range(self.grid.height):
            line = "" #f"{y}: "
            for x in range(self.grid.width):
                point = Vector2(x, y)

                if point == self.start_point:
                    line += "S"
                elif point == self.end_point:
                    line += "F"
                # elif self.open.holds(point):
                #     line += "O"
                # elif point in self.closed.keys():
                #     line += "C"
                elif point in self.path:
                    line += "#"
                else:
                    line += str(self.grid.get(point))

            print(line)
        print()



        data = []

        for y in range(self.grid.height):
            for x in range(self.grid.width):
                point = Vector2(x, y)

                data.append(f"{point}={self.closed[point].score}")

        print(data)
