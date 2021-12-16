
_DIRS = ((1, 0), (0, -1), (-1, 0), (0, 1))
_DIR_NAMES = ['E', 'S', 'W', 'N']

class Navigator:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.dir = 0

    def __repr__(self):
        return f"x={self.x}, y={self.y}, pointed {_DIR_NAMES[self.dir]}"

    def forward(self, distance: int):
        self.x += distance * _DIRS[self.dir][0]
        self.y += distance * _DIRS[self.dir][1]

    def backward(self, distance: int):
        return self.forward(-distance)

    def turn_left(self, turns: int):
        self.dir = (self.dir - turns) % len(_DIRS)

    def turn_right(self, turns: int):
        self.dir = (self.dir + turns) % len(_DIRS)

    def north(self, dist: int):
        self.y += dist

    def south(self, dist: int):
        self.y -= dist

    def east(self, dist: int):
        self.x += dist

    def west(self, dist: int):
        self.x -= dist


