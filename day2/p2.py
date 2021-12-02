import operator
from functools import *

with open('input.txt') as f:
    commands = {
        'down': lambda v, x, y, a: (x, y, a + v),
        'up': lambda v, x, y, a: (x, y, a - v),
        'forward': lambda v, x, y, a: (x + v, y + (a * v), a)
    }


    def map_line(line):
        cmd, v = line.split(' ')
        return commands[cmd], int(v)


    reduced = reduce(lambda acc, v: v[0](v[1], acc[0], acc[1], acc[2]), map(map_line, f), (0, 0, 0))
    print(reduce(operator.mul, reduced[:2]))
