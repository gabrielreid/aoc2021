import operator
from functools import *
from itertools import *


def get_adjacent(rows, y, x):
    return filter(lambda k: k in rows,
                  starmap(lambda yoff, xoff: (y + yoff, x + xoff), ((-1, 0), (0, 1), (1, 0), (0, -1))))


def extend_basin(rows, y, x, basin):
    for adj in get_adjacent(rows, y, x):
        if adj not in basin and rows[adj] != 9:
            basin.add(adj)
            extend_basin(rows, adj[0], adj[1], basin)


with open('input.txt') as f:
    rows = {}
    for y, line in enumerate(f):
        for x, v in enumerate(line.strip()):
            rows[(y, x)] = int(v)
    all_in_basin = set()
    basins = []
    for k, val in rows.items():
        if val == 9 or k in all_in_basin:
            continue
        basin = set()
        basin.add(k)
        extend_basin(rows, *k, basin)
        all_in_basin.update(basin)
        basins.append(basin)
    print(reduce(operator.mul, islice(reversed(sorted(map(len, basins))), 3)))
