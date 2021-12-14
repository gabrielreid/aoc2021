import operator
from itertools import *
from collections import *
from functools import *

with open('input.txt') as f:
    template, lines = f.read().split("\n\n")
    d = {t[0]: t[1] for t in [line.split(' -> ') for line in lines.splitlines()]}

    counter = Counter(map(lambda t: "".join(t), zip(template, template[1:])))
    for i in range(40):
        counter = reduce(operator.add, chain.from_iterable(
            map(lambda ab: (Counter({ab[0] + d[ab]: counter[ab]}), Counter({d[ab] + ab[1]: counter[ab]})), counter)))
        char_counts = reduce(operator.add, map(lambda t: Counter({t[0][0]: t[1]}), counter.items()))
        char_counts[template[-1]] += 1
        print(f"{i + 1}: {char_counts.most_common()[0][1] - char_counts.most_common()[-1][1]}")
