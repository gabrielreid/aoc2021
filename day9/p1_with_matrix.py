from functools import partial

from util import *


def is_low(matrix, p):
    return not any(matrix.get_adjacent(p, lambda adj: matrix[adj] <= matrix[p]))


with open('input.txt') as f:
    matrix = Matrix()
    for y, line in enumerate(f):
        for x, v in enumerate(line.strip()):
            matrix[(x, y)] = int(v)
    print(sum(map(lambda p: matrix[p] + 1, filter(partial(is_low, matrix), matrix))))
