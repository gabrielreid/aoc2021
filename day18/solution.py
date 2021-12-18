import copy
import itertools
import math
from functools import *


class Leaf:
    def __init__(self, val):
        self.val = val

    def __str__(self):
        return str(self.val)

    def visit_in_order(self, visitor, depth):
        return visitor.accept_value(self)


class Node:
    def __init__(self, left, right):
        if isinstance(left, int):
            self.left = Leaf(left)
        elif isinstance(left, Node):
            self.left = left
        else:
            self.left = Node(*left)

        if isinstance(right, int):
            self.right = Leaf(right)
        elif isinstance(right, Node):
            self.right = right
        else:
            self.right = Node(*right)

    def __str__(self):
        return "[%s,%s]" % (self.left, self.right)

    def visit_in_order(self, visitor, depth=0):
        return self.left.visit_in_order(visitor, depth + 1) \
               and visitor.accept_node(self, depth) \
               and self.right.visit_in_order(visitor, depth + 1)


class Visitor:

    def accept_node(self, node, depth):
        return True

    def accept_value(self, node):
        return True


class ExplodeVisitor(Visitor):

    def __init__(self):
        self.n = 0
        self.exploded_node = None

    def accept_node(self, node, depth):
        if depth == 3:
            if isinstance(node.left, Node):
                self.exploded_node = node.left
                self.exploded_offset = self.n - 2
                node.left = Leaf(0)
                return False
            elif isinstance(node.right, Node):
                self.exploded_node = node.right
                self.exploded_offset = self.n
                node.right = Leaf(0)
                return False
        return True

    def accept_value(self, node):
        self.n += 1
        return True


class SetValueVisitor(Visitor):

    def __init__(self, target, value):
        self.target = target
        self.value = value
        self.n = 0

    def accept_value(self, node):
        if self.n == self.target:
            node.val += self.value
            return False
        self.n += 1
        return True


class SplitVisitor(Visitor):

    def accept_node(self, node, depth):
        if isinstance(node.left, Leaf) and node.left.val >= 10:
            val = node.left.val
            node.left = Node(math.floor(val / 2), math.ceil(val / 2))
            return False
        if isinstance(node.right, Leaf) and node.right.val >= 10:
            val = node.right.val
            node.right = Node(math.floor(val / 2), math.ceil(val / 2))
            return False
        return True


def sum_shellfish(n):
    while True:
        explode_visitor = ExplodeVisitor()
        if not n.visit_in_order(explode_visitor):
            n.visit_in_order(
                SetValueVisitor(explode_visitor.exploded_offset - 1, explode_visitor.exploded_node.left.val))
            n.visit_in_order(
                SetValueVisitor(explode_visitor.exploded_offset + 1, explode_visitor.exploded_node.right.val))
        elif n.visit_in_order(SplitVisitor()):
            return n


def magnitude(n):
    if isinstance(n, Node):
        return magnitude(n.left) * 3 + magnitude(n.right) * 2
    else:
        return n.val


def calculate(values):
    reduced = reduce(lambda acc, nxt: sum_shellfish(copy.deepcopy(Node(acc, copy.deepcopy(nxt)))), values)
    return magnitude(reduced)


with open('input.txt') as f:
    lines = [Node(*eval(l)) for l in f.read().splitlines()]
    print(f"p1: {calculate(lines)}")
    print(f"p2: {max(map(calculate, itertools.permutations(lines, 2)))}")
