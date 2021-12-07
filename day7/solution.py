from functools import *


def p1(from_position, to_position):
    return abs(from_position - to_position)


@lru_cache
def p2(from_position, to_position):
    return sum(range(1, abs(from_position - to_position) + 1))


with open('input.txt') as f:
    values = list(map(int, next(f).strip().split(',')))
    for pfunc in (p1, p2):
        print("%s => %d" % (pfunc.__name__, min(map(lambda v: sum(map(lambda x: pfunc(v, x), values)), values))))
