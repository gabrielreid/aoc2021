from collections import *


def map_growth(days_remaining):
    return [6, 8] if days_remaining == 0 else [days_remaining - 1]


def reproduce(fish):
    cnt = Counter()
    for days_remaining, fish_cnt in list(fish.items()):
        for v in map_growth(days_remaining):
            cnt[v] += fish_cnt
    return cnt


with open('input.txt') as f:
    fish = Counter(list(map(int, f.read().split(','))))
    for i in range(256):
        fish = reproduce(fish)
        print(f"After {i + 1} days there are {sum(fish.values())} fish")
