import operator
from dataclasses import dataclass
from functools import *
from typing import TypeVar, Generic, Dict, Optional, Iterator

T = TypeVar('T')

@dataclass(frozen=True)
class Point:
    x: int
    y: int

    def __getitem__(self, item):
        if item == 0:
            return self.x
        elif item == 1:
            return self.y
        else:
            raise IndexError(f"No value for {item} in {self}")

    def __add__(self, other):
        return Point(self.x + other[0], self.y + other[1])


@dataclass()
class Node(Generic[T]):
    point: Point
    val: T


class Matrix(Generic[T]):
    nodes: Dict[Point, Node]

    def __init__(self):
        self.nodes = {}

    def get(self, point: Point) -> Optional[Node[T]]:
        return self.nodes.get(point)

    def add(self, node: Node[T]):
        self.nodes[node.point] = node

    def get_adjacent(self, point, predicate=lambda p: True) -> Iterator[Point]:
        return filter(predicate, self._get_adjacent(point, (-1, 0), (1, 0), (0, -1), (0, 1)))

    def get_adjacent_diag(self, point, predicate=lambda p: True) -> Iterator[Point]:
        return filter(predicate,
                      self._get_adjacent(point, (-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)))

    def _get_adjacent(self, point, *offsets) -> Iterator[Point]:
        return filter(lambda k: k in self.nodes, map(partial(operator.add, point), offsets))

    def __iter__(self):
        return iter(self.nodes.keys())

    def __getitem__(self, point) -> T:
        try:
            return self.nodes[point].val
        except KeyError:
            return None

    def __setitem__(self, key, value: T):
        if type(key) == tuple and len(key) == 2:
            key = Point(*key)
        self.nodes[key] = Node(point=key, val=value)

    def __len__(self):
        return len(self.nodes)
