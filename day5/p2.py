import re
from collections import *
from itertools import *


def points(x1, y1, x2, y2):
    if x1 == x2:
        y1, y2 = sorted((y1, y2))
        return ((x1, y) for y in range(y1, y2 + 1))
    elif y1 == y2:
        x1, x2 = sorted((x1, x2))
        return ((x, y1) for x in range(x1, x2 + 1))
    elif abs(x2 - x1) == abs(y2 - y1):
        xstep = 1 if x2 > x1 else -1
        ystep = 1 if y2 > y1 else -1
        return accumulate(range(abs(x2 - x1)), func=lambda xy, i: (xy[0] + xstep, xy[1] + ystep), initial=(x1, y1))


with open('input.txt') as f:
    hit = Counter()
    for line in f.read().splitlines():
        m = re.match(r'(\d+),(\d+) -> (\d+),(\d+)', line)
        x1, y1, x2, y2 = map(int, m.groups())
        hit.update(Counter(points(x1, y1, x2, y2)))
    print(sum(h[1] > 1 for h in hit.most_common()))
