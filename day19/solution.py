import itertools
import operator
from collections import *
from functools import *
from itertools import *


class Block:
    def __init__(self, title, lines):
        self.title = title
        self.points = [tuple(map(int, l.split(','))) for l in lines]

    def distances(self):
        for i in range(len(self.points)):
            origin = self.points[i]
            other_points = self.points[:i] + self.points[i + 1:]
            yield self._distances(origin, other_points)

    def _distances(self, origin, others):
        distances = []
        for other in others:
            dist = abs(origin[0] - other[0]) + abs(origin[1] - other[1]) + abs(origin[2] - other[2])
            distances.append(dist)
        return origin, Counter(distances)


class OrientationTransform:
    def __init__(self, signs, axis_order):
        self.signs = signs
        self.axis_order = axis_order

    def __call__(self, point):
        return tuple(map(operator.mul,
                         map(partial(operator.getitem, point), self.axis_order),
                         map(partial(operator.getitem, self.signs), self.axis_order)))


class OffsetTransform:
    def __init__(self, offsets):
        self.offsets = offsets

    def __call__(self, point):
        return tuple(map(operator.add, point, self.offsets))


def get_transform(origin_a, block_a, origin_b, block_b):
    for orientation_transform in starmap(OrientationTransform,
                                         itertools.product(itertools.product((1, -1), repeat=3),
                                                           permutations([0, 1, 2], 3))):
        offset_transform = OffsetTransform(tuple(map(operator.sub, origin_a, orientation_transform(origin_b))))
        transform = lambda p: offset_transform(orientation_transform(p))
        overlap = set(block_a.points) & set(map(transform, block_b.points))
        if len(overlap) > 10:
            return transform


def get_path(transforms, from_scanner, to_scanner, visited=None, path=None):
    if path is None:
        path = []
    if visited is None:
        visited = set()
    visited.add(from_scanner)
    path.append(from_scanner)

    if from_scanner == to_scanner:
        return path[:]
    else:
        for scanner in transforms[from_scanner]:
            if scanner not in visited:
                found = get_path(transforms, scanner, to_scanner, visited, path)
                if found:
                    return found

    path.pop()
    visited.remove(from_scanner)


def pairwise(iterable):
    a, b = tee(iterable)
    next(b, None)
    return zip(a, b)


with open('input.txt') as f:
    blocks = []
    block_by_title = {}
    for block in f.read().split("\n\n"):
        block_lines = block.splitlines()
        block = Block(block_lines[0], block_lines[1:])
        blocks.append(block)
        block_by_title[block.title] = block

    transforms = defaultdict(dict)
    for (block_a, block_b) in combinations(blocks, 2):
        matches = 0
        for origin_a, dist_a in block_a.distances():
            for origin_b, dist_b in block_b.distances():
                overlap_count = sum(bval for (bkey, bval) in dist_b.items() if bkey in dist_a)
                if overlap_count > 10:
                    transforms[block_b.title][block_a.title] = get_transform(origin_a, block_a, origin_b,
                                                                             block_b)
                    transforms[block_a.title][block_b.title] = get_transform(origin_b, block_b, origin_a,
                                                                             block_a)
                    break

    all_points = set()
    all_origins = [(0, 0, 0)]
    for block in blocks:
        if block.title == '--- scanner 0 ---':
            all_points.update(block.points)
        else:
            curr = block.title
            path = get_path(transforms, block.title, '--- scanner 0 ---')
            points = block.points[:]
            origin = (0, 0, 0)
            for trans_from, trans_to in pairwise(path):
                transform = transforms[trans_from][trans_to]
                points = list(map(transform, points))
                origin = transform(origin)
            all_origins.append(origin)
            all_points.update(points)
    print(f"p1: {len(all_points)} points in total")
    max_dist = max(starmap(lambda o1, o2: sum(map(abs, map(operator.sub, o1, o2))), combinations(all_origins, 2)))
    print(f"p2: max distance = {max_dist}")
