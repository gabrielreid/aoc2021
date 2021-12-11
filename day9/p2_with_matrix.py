import operator
from functools import *
from itertools import *

from util import *


def extend_basin(matrix, p, basin):
    for adj in matrix.get_adjacent(p, lambda adj: matrix[adj] != 9 and adj not in basin):
        basin.add(adj)
        extend_basin(matrix, adj, basin)


with open('input.txt') as f:
    matrix = Matrix()
    for y, line in enumerate(f):
        for x, v in enumerate(line.strip()):
            matrix[(x, y)] = int(v)
    all_in_basin = set()
    basins = []
    for p in matrix:
        if matrix[p] == 9 or p in all_in_basin:
            continue
        basin = set()
        basin.add(p)
        extend_basin(matrix, p, basin)
        all_in_basin.update(basin)
        basins.append(basin)
    print(reduce(operator.mul, islice(reversed(sorted(map(len, basins))), 3)))
