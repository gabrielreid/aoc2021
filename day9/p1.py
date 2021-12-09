from itertools import *


def is_low(rows, y, x):
    return not any(filter(lambda k: k in rows and rows[k] <= rows[(y, x)],
                          starmap(lambda yoff, xoff: (y + yoff, x + xoff), ((-1, 0), (0, 1), (1, 0), (0, -1)))))


with open('input.txt') as f:
    rows = {}
    for y, line in enumerate(f):
        for x, v in enumerate(line.strip()):
            rows[(y, x)] = int(v)
    print(sum(map(lambda k: rows[k] + 1, list(filter(lambda k: is_low(rows, *k), rows.keys())))))
