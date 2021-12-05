import re
from collections import *


def points(x1, y1, x2, y2):
    if x1 == x2:
        return ((x1, y) for y in range(y1, y2 + 1))
    elif y1 == y2:
        return ((x, y1) for x in range(x1, x2 + 1))
    else:
        return ()


with open('input.txt') as f:
    hit = Counter()
    for line in f.read().splitlines():
        m = re.match(r'(\d+),(\d+) -> (\d+),(\d+)', line)
        x1, y1, x2, y2 = map(int, m.groups())
        x1, x2 = sorted((x1, x2))
        y1, y2 = sorted((y1, y2))
        hit.update(Counter(points(x1, y1, x2, y2)))
    print(sum(h[1] > 1 for h in hit.most_common()))
