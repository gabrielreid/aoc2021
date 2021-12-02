import operator
from functools import *

with open('input.txt') as f:
    cmds = {
        'forward': (1, 0),
        'up': (0, -1),
        'down': (0, 1)
    }


    def map_line(line):
        cmd, v = line.split(' ')
        return tuple(int(v) * c for c in cmds[cmd])


    sums = reduce(lambda a, b: (a[0] + b[0], a[1] + b[1]), map(map_line, f), (0, 0))
    print(reduce(operator.mul, sums))
