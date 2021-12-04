import operator
import re
from functools import *
from itertools import *


def done(board):
    return any(map(lambda values: all(map(partial(operator.is_, None), values)),
                   chain(board[:], ([r[c] for r in board] for c in range(len(board[0]))))))


def mark(board, n):
    return [[v != n and v or None for v in row] for row in board]


def score(board):
    return sum(filter(partial(operator.is_, None), chain.from_iterable(*board)))


def partition(iterable, predicate):
    matching = list(map(predicate, iterable))
    return ([v for (v, t) in zip(iterable, matching) if t],
            [v for (v, t) in zip(iterable, matching) if not t])


with open('input.txt') as f:
    nums = map(int, re.split(r',', next(f).strip()))
    boards = [[[int(v) for v in re.split(r'\s+', l.strip())] for l in islice(f, 5)] for _ in f]
    while boards:
        num = next(nums)
        boards = list(map(partial(mark, n=num), boards))
        completed, boards = partition(boards, done)
        # Prints out winning boards in order
        for c in completed:
            print(sum(filter(partial(operator.is_not, None), chain.from_iterable(c))) * num)
