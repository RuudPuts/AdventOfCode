from day import Day
from input_parser import InputParser


class Day7(Day):
    @property
    def title(self):
        return "No Space Left On Device"

    @property
    def input_parser(self):
        return TerminalParser()

    @property
    def example_input(self):
        return """$ cd /
$ ls
dir a
14848514 b.txt
8504156 c.dat
dir d
$ cd a
$ ls
dir e
29116 f
2557 g
62596 h.lst
$ cd e
$ ls
584 i
$ cd ..
$ cd ..
$ cd d
$ ls
4060174 j
8033020 d.log
5626152 d.ext
7214296 k"""

    @property
    def expected_results(self):
        return {
            "task1_example": 95437,
            "task1": 1447046,
            "task2_example": 24933642,
            "task2": 578710
        }

    def calculate_dir_size(self, node, size=0):
        size += sum(map(lambda x: x.size, node.files))

        for dir in node.subdirectories:
            size = self.calculate_dir_size(dir, size=size)

        return size

    def task1(self, input):
        score = 0

        dirs_to_check = [input]
        while len(dirs_to_check) > 0:
            dir = dirs_to_check.pop(0)
            total_size = self.calculate_dir_size(dir)

            if total_size < 100000:
                score += total_size

            dirs_to_check.extend(dir.subdirectories)

        return score

    def task2(self, input):
        total = 70000000
        needed = 30000000
        used = self.calculate_dir_size(input)
        free = total - used
        to_delete = needed - free

        smallest_to_delete = total

        dirs_to_check = [input]
        while len(dirs_to_check) > 0:
            dir = dirs_to_check.pop(0)
            total_size = self.calculate_dir_size(dir)

            if total_size >= to_delete and total_size < smallest_to_delete:
                smallest_to_delete = total_size

            dirs_to_check.extend(dir.subdirectories)

        return smallest_to_delete


class TreeNode():
    def __init__(self, title, parent=None):
        self.title = title
        self.parent = parent
        self.children = []


class DirNode(TreeNode):
    @property
    def subdirectories(self):
        return filter(lambda x: isinstance(x, DirNode), self.children)

    @property
    def files(self):
        return filter(lambda x: isinstance(x, FileNode), self.children)


class FileNode(TreeNode):
    def __init__(self, title, size, parent=None):
        super().__init__(title, parent)
        self.size = size


class TerminalParser(InputParser):
    def parse(self, input):
        result = None
        current = None

        listing_dir = False

        for line in input:
            # print(f" > {line}")
            if line.startswith('$'):
                listing_dir = False

                command = line[2:4]
                if command == "ls":
                    listing_dir = True
                elif command == "cd":
                    param = line[5:]
                    if param == "/":
                        if result is None:
                            # print("   Create root node")
                            result = DirNode(param)
                        # print("   Activate root node")
                        current = result
                    elif param == "..":
                        # print(f"   Change dir to parent '{current.parent.title}'")
                        current = current.parent
                    else:
                        # print(f"   Change dir to '{param}'")
                        # Change dir?
                        children = list(filter(lambda x: x.title == param, current.subdirectories))
                        if len(children) > 0:
                            child = children[0]
                            # print(f"   Reusing dir '{child.title}'")
                        else:
                            child = DirNode(param, current)
                            # print(f"   Adding dir '{child.title}' to '{child.parent.title}'")
                            current.children.append(child)
                        current = child
            elif listing_dir:
                if not line.startswith("dir"):
                    parts = line.split(" ") # size, filename
                    file = FileNode(parts[1], int(parts[0]), current)
                    # print(f"   Adding file '{file.title}' size {file.size} to '{file.parent.title}'")
                    current.children.append(file)

        return result
