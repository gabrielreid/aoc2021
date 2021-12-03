from collections import *
from functools import *


def cnt(counters, line):
    for counter, c in zip(counters, line.strip()):
        counter[c] += 1
    return counters


with open('input.txt') as f:
    counters = [Counter() for i in range(12)]
    reduce(cnt, f, counters)
    print(int("".join([c.most_common(2)[0][0] for c in counters]), 2) * int(
        "".join([next(reversed(c.most_common(2)))[0][0] for c in counters]), 2))
