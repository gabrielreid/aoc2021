from itertools import *
import operator

def pairwise(iterable):
    a, b = tee(iterable)
    next(b, None)
    return zip(a, b)

def triplewise(iterable):
    for (a, _), (b, c) in pairwise(pairwise(iterable)):
        yield a, b, c

# Part 1
with open('input.txt') as f:
    print(sum(starmap(operator.lt, pairwise(map(int, f)))))

# Part 2
with open('input.txt') as f:
    print(sum(starmap(operator.lt, pairwise(map(sum, triplewise(map(int, f)))))))




