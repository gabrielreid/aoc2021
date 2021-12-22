import re

def parse_range(r):
    m = re.match(r'\w=(-?\d+)\.\.(-?\d+)', r)
    if not m:
        raise ValueError(r)
    return range(max(int(m.group(1)), -50), min(int(m.group(2)), 50) + 1)

with open('input.txt') as f:
    d = {}
    for line in f.read().splitlines():
        instr, tail = line.split()
        xs, ys, zs = list(map(parse_range, tail.split(',')))
        for x in xs:
            for y in ys:
                for z in zs:
                    k = (x, y, z)
                    d[k] = instr
    print(sum(v == 'on' for v in d.values()))


