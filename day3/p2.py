from collections import *
from functools import *


def counter_for_values(i, lines):
    def inc(counter, line):
        counter[line[i]] += 1
        return counter

    return reduce(inc, lines, Counter())


def o2_filter(i, lines):
    counter = counter_for_values(i, lines)
    if counter['1'] == counter['0']:
        return '1'
    return counter.most_common()[0][0]


def co2_filter(i, lines):
    counter = counter_for_values(i, lines)
    if counter['1'] == counter['0']:
        return '0'
    return counter.most_common()[-1][0]


def reduce_values(i, lines, extract_filter):
    bit_filter = extract_filter(i, lines)
    return list(filter(lambda v: v[i] == bit_filter, lines))


def calculate(lines, extract_filter):
    i = 0
    while len(lines) > 1:
        lines = reduce_values(i, lines, extract_filter)
        i += 1
    return int(lines[0], 2)


with open('input.txt') as f:
    lines = [l.strip() for l in f]
    print(calculate(lines, o2_filter) * calculate(lines, co2_filter))
