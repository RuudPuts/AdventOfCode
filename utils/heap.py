class HeapItem:
    def __init__(self, data, index=0, score=0):
        self.data = data
        self.index = index
        self.score = score


class Heap:
    def __init__(self, items):
        self.items = []

        for item in items:
            self.add(item)

    def __iter__(self):
        return iter(self.items)

    def __len__(self):
        return len(self.items)

    def print(self):
        print(f"Items: {[i.score for i in self.items]}")
        for i in self.items:
            print(f"   {i.data} - {i.index} - {i.score}")

    def add(self, item):
        # print(f"🏔 Heap add item {item.data}: {item.score}")
        item.index = len(self.items)
        self.items.append(item)
        self.sort_up(item)

    def contains(self, item):
        return self.items[item.heapIndex] == item

    def get(self, data):
        for i in self.items:
            if i.data == data:
                return i

        return None

    def holds(self, data):
        return self.get(data) is not None

    def pop(self):
        if len(self.items) == 0:
            return None

        first = self.items[0]
        # print(f"🏔 Heap pop first {first.index} - {first.score}")
        # self.print()

        if self.items:
            self.items = self.items[1:]

        if len(self.items) < 2:
            return first

        last = self.items.pop()
        # print(f"🏔 [Heap] Moving {last.index} - {last.score} to front")
        self.items.insert(0, last)
        last.index = 0

        self.sort_down(last)

        return first

    def update(self, item):
        self.sort_up(item)

    def swap(self, item_a, item_b):
        # print(f"🏔 [Heap] Swapping {item_a.index} -> {item_b.index}")
        self.items[item_a.index] = item_b
        self.items[item_b.index] = item_a

        item_a_index = item_a.index
        item_a.index = item_b.index
        item_b.index = item_a_index

    def sort_up(self, item):
        # print(f"🏔 [Heap] Sort up {item.index} - {item.score}")
        while True:
            parent_index = int((item.index - 1) / 2)
            parent = self.items[parent_index]

            if item.score < parent.score:
                self.swap(item, parent)
            else:
                return

    def sort_down(self, item):
        # print(f"🏔 [Heap] Sort down {item.index} - {item.score}")
        while True:
            left_child_index = item.index * 2 + 1
            right_child_index = item.index * 2 + 2
            swap_index = 0

            if left_child_index < len(self.items):
                swap_index = left_child_index

                if right_child_index < len(self.items):
                    if self.items[right_child_index].score < self.items[left_child_index].score:
                        swap_index = right_child_index

                if self.items[swap_index].score < item.score:
                    self.swap(item, self.items[swap_index])
                else:
                    return
            else:
                return
