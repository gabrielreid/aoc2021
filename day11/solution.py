from itertools import *

from util import *

with open('input.txt') as f:
    matrix = Matrix()
    for y, row in enumerate(f.read().splitlines()):
        for x, v in enumerate(row):
            matrix[(x, y)] = int(v)
    total_flashed = 0
    for step in count(start=1):
        flash_queue = []
        flashed = set()
        for p in matrix:
            matrix[p] += 1
            if matrix[p] > 9:
                flash_queue.append(p)
                flashed.add(p)
                matrix[p] = 0
        while flash_queue:
            k = flash_queue.pop(0)
            for adj in matrix.get_adjacent_diag(k, lambda adj: adj not in flashed):
                matrix[adj] += 1
                if matrix[adj] > 9:
                    flash_queue.append(adj)
                    flashed.add(adj)
                    matrix[adj] = 0
        total_flashed += len(flashed)
        if len(flashed) == len(matrix):
            print(f"All flashed in step {step}")
            break
        if step == 100:
            print(f"After 100 steps there are {total_flashed} flashed")
