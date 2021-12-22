import operator
import re
from dataclasses import dataclass
from functools import *


def parse_range(r):
    m = re.match(r'\w=(-?\d+)\.\.(-?\d+)', r)
    if not m:
        raise ValueError(r)
    return Range(int(m.group(1)), int(m.group(2)))


def overlaps(minmax):
    return minmax[0] <= minmax[1]


@dataclass(frozen=True)
class Range:
    minval: int
    maxval: int

    def size(self):
        return (self.maxval - self.minval) + 1

    def overlap(self, other):
        lower = max(self.minval, other.minval)
        upper = min(self.maxval, other.maxval)
        if lower <= upper:
            return Range(lower, upper)


@dataclass(frozen=True)
class Cube:
    xs: Range
    ys: Range
    zs: Range
    on: bool

    def intersection(self, other):
        overlap_xs = self.xs.overlap(other.xs)
        overlap_ys = self.ys.overlap(other.ys)
        overlap_zs = self.zs.overlap(other.zs)
        if overlap_xs and overlap_ys and overlap_zs:
            return Cube(overlap_xs, overlap_ys, overlap_zs, on=not (other.on))

    def volume(self):
        vol = reduce(operator.mul, map(lambda range: range.size(), (self.xs, self.ys, self.zs)))
        if not self.on:
            vol = -(vol)
        return vol


with open('input.txt') as f:
    cubes = []
    for i, line in enumerate(f.read().splitlines()):
        instr, tail = line.split()
        next_cube = Cube(*list(map(parse_range, tail.split(','))), on=instr == 'on')
        new_cubes = []
        for cube in cubes:
            intersection = next_cube.intersection(cube)
            if intersection:
                new_cubes.append(intersection)
        if instr == 'on':
            new_cubes.append(next_cube)
        cubes.extend(new_cubes)
    print(sum(c.volume() for c in cubes))
