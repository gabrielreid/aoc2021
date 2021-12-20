import operator
from collections import *
from functools import *


def input_coords(x, y):
    return [
        (x - 1, y - 1),
        (x, y - 1),
        (x + 1, y - 1),
        (x - 1, y),
        (x, y),
        (x + 1, y),
        (x - 1, y + 1),
        (x, y + 1),
        (x + 1, y + 1)
    ]


def bounds(image):
    xs = list(map(lambda t: t[0], image.keys()))
    ys = list(map(lambda t: t[1], image.keys()))
    return min(xs), min(ys), max(xs), max(ys)


def calculate(image, default_value):
    minx, miny, maxx, maxy = bounds(image)
    next_image = defaultdict(lambda: default_value)
    for x in range(minx - 1, maxx + 2):
        for y in range(miny - 1, maxy + 2):
            offset = int("".join(
                map(lambda v: '1' if v == '#' else '0', map(partial(operator.getitem, image), input_coords(x, y)))), 2)
            c = enhancement_algo[offset]
            next_image[(x, y)] = c
    return next_image


def pixel_count(image):
    return sum(v == '#' for v in image.values())


with open('input.txt') as f:
    enhancement_algo, input_image = f.read().split("\n\n")
    image = defaultdict(lambda: '.')
    for y, row in enumerate(input_image.splitlines()):
        for x, v in enumerate(row):
            image[(x, y)] = v

    for i in range(50):
        image = calculate(image, default_value='.' if i % 2 == 1 else enhancement_algo[0])
        if i == 1:
            print(f"p1: {pixel_count(image)}")
        elif i == 49:
            print(f"p2: {pixel_count(image)}")
