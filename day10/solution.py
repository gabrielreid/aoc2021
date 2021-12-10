from functools import *

matching = {
    '(': ')',
    '{': '}',
    '[': ']',
    '<': '>'
}

with open('input.txt') as f:
    p1_score = 0
    p2_scores = []
    incomplete_lines = []
    for line in f.read().splitlines():
        stack = []
        for c in line:
            if c in matching:
                stack.append(c)
            else:
                if matching[stack.pop()] != c:
                    p1_score += {')': 3, ']': 57, '}': 1197, '>': 25137}[c]
                    break
        else:
            p2_scores.append(reduce(lambda acc, c: acc * 5 + {'(': 1, '[': 2, '{': 3, '<': 4}[c], stack, 0))
    print(f"p1: {p1_score}")
    print(f"p2: {sorted(p2_scores)[len(p2_scores) // 2]}")
