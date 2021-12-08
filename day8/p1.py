with open('input.txt') as f:
    print(
        sum(map(lambda l: sum(1 for v in l.split(' | ')[1].split() if len(v) in (2, 4, 3, 7)), f.read().splitlines())))
