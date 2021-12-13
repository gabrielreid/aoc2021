import operator
import re

with open('input.txt') as f:
    content = f.read()
    point_section, folds = content.split("\n\n")
    points = list(map(lambda p: tuple(map(int, p.split(','))), point_section.splitlines()))
    colcount = max(map(operator.itemgetter(0), points)) + 1
    rowcount = max(map(operator.itemgetter(1), points)) + 1

    rows = [[0] * colcount for _ in range(rowcount)]

    for x, y in points:
        rows[y][x] = 1

    for i, fold in enumerate(folds.splitlines()):
        m = re.search('(\w)=(\d+)', fold)
        axis = m.group(1)
        fold_loc = int(m.group(2))

        if axis == 'y':
            n = 1
            for rownum, row in enumerate(rows[fold_loc + 1:]):
                for col, val in enumerate(row):
                    rows[fold_loc - n][col] = min(1, val + rows[fold_loc - n][col])
                n += 1
            rows = rows[:fold_loc]
        elif axis == 'x':
            for rownum, row in enumerate(rows):
                n = 1
                for val in row[fold_loc + 1:]:
                    row[fold_loc - n] = min(1, val + row[fold_loc - n])
                    n += 1
                rows[rownum] = row[:fold_loc]

        if i == 0:
            print(f"sum = {sum(map(sum, rows))}")

for row in rows:
    print("".join(map(lambda v: v == 1 and 'X' or ' ', row)))
