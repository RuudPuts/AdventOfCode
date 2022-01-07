from collections import defaultdict
from functools import reduce


def chunks(list, size):
    """Yield max-size chunks from list."""
    for i in range(0, len(list), size):
        yield list[i:i + size]


def windows(list, size):
    """Yield size windows from list.

199  A
200  A B
208  A B C
210    B C D
200  E   C D
207  E F   D
240  E F G
269    F G H
260      G H
263        H"""
    for i in range(0, len(list) - size + 1):
        yield list[i:i + size]


def generate_grid(width, height, initial_value):
    return [[initial_value for i in range(width)] for i in range(height)] # list(map(lambda y: list(map(lambda x: initial_value, range(0, width))), range(0, height)))


def flatten(list):
    return [item for sublist in list for item in sublist]


def prod(list):
    return reduce((lambda x, y: x * y), list)


def median(list):
    middle = float(len(list))/2
    if middle % 2 != 0:
        return list[int(middle - .5)]
    else:
        return (list[int(middle)], list[int(middle-1)])

# Strings


def count_chars(text):
    char_count = defaultdict(int)
    for char in text:
        char_count[char] += 1

    return char_count
