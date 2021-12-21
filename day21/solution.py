import copy
from functools import *
from itertools import *


class GameState:
    def __init__(self, positions, play_until):
        self.positions = positions
        self.play_until = play_until
        self.scores = [0, 0]
        self.player_idx = 0
        self.turns = 0

    def __eq__(self, other):
        return (self.positions, self.scores, self.player_idx) == (other.positions, other.scores, other.player_idx)

    def __hash__(self):
        return hash((tuple(self.positions), tuple(self.scores), self.player_idx))

    def roll(self, val):
        self.turns += 1
        self.positions[self.player_idx] = (((self.positions[self.player_idx] - 1) + val) % 10) + 1
        self.scores[self.player_idx] += self.positions[self.player_idx]
        if self.scores[self.player_idx] >= self.play_until:
            return self.player_idx, self.scores[(self.player_idx + 1) % 2] * (self.turns * 3)
        self.player_idx = (self.player_idx + 1) % 2


@lru_cache(maxsize=None)
def wins(state):
    p1_wins, p2_wins = 0, 0
    for roll_value in map(sum, product((1, 2, 3), repeat=3)):
        next_state = copy.deepcopy(state)
        res = next_state.roll(roll_value)
        if res:
            if res[0] == 0:
                p1_wins += 1
            else:
                p2_wins += 1
        else:
            p1, p2 = wins(next_state)
            p1_wins += p1
            p2_wins += p2
    return p1_wins, p2_wins


with open('input.txt') as f:
    positions = list(map(int, map(lambda l: l.split(': ')[1], f.readlines())))

    # Part 1
    die = 0
    state = GameState(positions[:], play_until=1000)
    while True:
        roll = 0
        for _ in range(3):
            roll += (die + 1)
            die = (die + 1) % 100
        result = state.roll(roll)
        if result:
            print(f"p1: {result[1]}")
            break

    # Part 2
    state = GameState(positions=positions[:], play_until=21)
    p1_wins, p2_wins = wins(state)
    print(f"p2: {max(p1_wins, p2_wins)}")
