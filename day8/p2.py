def get_1(vals):
    return next(v for v in vals if len(v) == 2)


def get_2(vals):
    v3 = get_3(vals)
    v5 = get_5(vals)
    return next(v for v in vals if len(v) == 5 and v != v3 and v != v5)


def get_3(vals):
    v1 = get_1(vals)
    return next(v for v in vals if len(v) == 5 and v >= v1)


def get_4(vals):
    return next(v for v in vals if len(v) == 4)


def get_5(vals):
    v3 = get_3(vals)
    v4 = get_4(vals)
    return next(v for v in vals if len(v) == 5 and v != v3 and len(v4 - v) == 1)


def get_6(vals):
    v7 = get_7(vals)
    return next(v for v in vals if len(v) == 6 and len(v7 - v) == 1)


def get_7(vals):
    return next(v for v in vals if len(v) == 3)


def get_8(vals):
    return next(v for v in vals if len(v) == 7)


def get_9(vals):
    v4 = get_4(vals)
    return next(v for v in vals if len(v) == 6 and v >= v4)


def get_0(vals):
    v6 = get_6(vals)
    v9 = get_9(vals)
    return next(v for v in vals if len(v) == 6 and v != v6 and v != v9)


with open('input.txt') as f:
    total = 0
    for line in f.read().splitlines():
        pre, post = line.split(' | ')
        pre_vals = [frozenset(v) for v in pre.split()]
        post_vals = [frozenset(v) for v in post.split()]
        val_map = {
            get_1(pre_vals): 1,
            get_2(pre_vals): 2,
            get_3(pre_vals): 3,
            get_4(pre_vals): 4,
            get_5(pre_vals): 5,
            get_6(pre_vals): 6,
            get_7(pre_vals): 7,
            get_8(pre_vals): 8,
            get_9(pre_vals): 9,
            get_0(pre_vals): 0,
        }
        total += int("".join(map(str, map(lambda s: val_map[s], post_vals))))
    print(f"total = {total}")
