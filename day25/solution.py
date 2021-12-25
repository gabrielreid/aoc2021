from itertools import *


def apply_moves(d, moves):
    for move_from, move_to in moves:
        d[move_to] = d[move_from]
        del d[move_from]


with open('input.txt') as f:
    d = {}
    for y, line in enumerate(f.read().splitlines()):
        for x, val in enumerate(line):
            if val != '.':
                d[(x, y)] = val

    xsize = max(x for (x, y) in d.keys()) + 1
    ysize = max(y for (x, y) in d.keys()) + 1

    for move_num in count():
        valid_move = lambda move: d.get(move[1]) is None
        xmoves = list(filter(valid_move, starmap(lambda x, y: ((x, y), ((x + 1) % xsize, y)),
                                                 filter(lambda k: d[k] == '>', d.keys()))))
        apply_moves(d, xmoves)
        ymoves = list(filter(valid_move, starmap(lambda x, y: ((x, y), (x, (y + 1) % ysize)),
                                                 filter(lambda k: d[k] == 'v', d.keys()))))
        apply_moves(d, ymoves)
        if not xmoves and not ymoves:
            print(f"No more moves after {move_num + 1}")
            break
