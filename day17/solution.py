import re


class Target:
    def __init__(self, xrange, yrange):
        self.xmin, self.xmax = xrange
        self.ymin, self.ymax = yrange

    def hit(self, probe):
        return self.xmin <= probe.x <= self.xmax \
               and self.ymin <= probe.y <= self.ymax

    def overshot(self, probe):
        return probe.x >= self.xmax or probe.y <= self.ymin


class Probe:
    def __init__(self, velocity_x, velocity_y):
        self.x = 0
        self.y = 0
        self.velocity_x = velocity_x
        self.velocity_y = velocity_y
        self.maxy = self.y

    def next(self):
        self.x += self.velocity_x
        self.y += self.velocity_y
        if self.velocity_x > 0:
            self.velocity_x -= 1
        elif self.velocity_x < 0:
            self.velocity_x += 1
        self.velocity_y -= 1
        self.maxy = max(self.maxy, self.y)


with open('input.txt') as f:
    groups = list(map(int, re.search(r'x=(.*)\.\.(.*), y=(.*)\.\.(.*)', next(f)).groups()))
    target = Target(groups[:2], groups[2:])
    maxy = -1
    xrange = max(map(abs, groups[:2]))
    yrange = max(map(abs, groups[2:]))
    initial_velocities = set()
    for velocity_x in range(-xrange, xrange + 1):
        for velocity_y in range(-yrange, yrange + 1):
            probe = Probe(velocity_x, velocity_y)
            while not target.hit(probe) and not target.overshot(probe):
                probe.next()
            if target.hit(probe):
                maxy = max(maxy, probe.maxy)
                initial_velocities.add((velocity_x, velocity_y))
    print(f"p1: {maxy}")
    print(f"p2: {len(initial_velocities)}")
