import copy
import heapq

DEPTH = 4


class Room:
    def __init__(self, name, offset):
        self.name = name
        self.offset = offset
        self.contents = [None] * DEPTH

    def done(self):
        return self.contents == [self.name] * DEPTH

    def __repr__(self):
        return f"Room {self.name}: {self.contents}"

    def can_move(self):
        """Is there anything in this room which can be moved out?"""
        for v in self.contents:
            if v is not None and v != self.name:
                return True
        return False

    def can_accept(self):
        """Can an appropriate piece be moved into this room?"""
        return not (self.can_move())

    def __hash__(self):
        return hash(tuple(self.contents))

    def __eq__(self, other):
        return (self.offset, self.contents) == (other.offset, other.contents)


class Map:
    def __init__(self, hallway, rooms, energy=0):
        self.hallway = hallway
        self.rooms = rooms
        self.energy = 0

    def __lt__(self, other):
        return self.energy < other.energy

    def __hash__(self):
        return hash((tuple(self.hallway), tuple(self.rooms)))

    def __eq__(self, other):
        return (self.hallway, self.rooms) == (other.hallway, other.rooms)

    def available_hallway_slots(self):
        return [x for (x, v) in enumerate(self.hallway) if v is None]

    def done(self):
        return all(map(lambda room: room.done(), self.rooms))

    def room_for_bot(self, bot):
        return self.rooms[ord(bot) - ord('A')]

    def move_to_hallway(self, room_name, y_offset, hallway_slot):
        room = self.rooms[ord(room_name) - ord('A')]

        y_dist = DEPTH - y_offset
        x_dist = abs(room.offset - hallway_slot)
        bot = room.contents[y_offset]
        cost = {'A': 1, 'B': 10, 'C': 100, 'D': 1000}[bot] * (y_dist + x_dist)
        new_map = copy.deepcopy(self)
        new_map.rooms[ord(room_name) - ord('A')].contents[y_offset] = None
        new_map.hallway[hallway_slot] = bot
        new_map.energy += cost
        return new_map

    def move_to_room(self, hallway_slot, y_offset, room_name):
        room = self.rooms[ord(room_name) - ord('A')]
        y_dist = DEPTH - y_offset
        x_dist = abs(room.offset - hallway_slot)
        bot = self.hallway[hallway_slot]
        cost = {'A': 1, 'B': 10, 'C': 100, 'D': 1000}[bot] * (y_dist + x_dist)
        new_map = copy.deepcopy(self)
        new_map.rooms[ord(room_name) - ord('A')].contents[y_offset] = bot
        new_map.hallway[hallway_slot] = None
        new_map.energy += cost
        return new_map

    def __repr__(self):
        def format_entry(v):
            return "." if v is None else v

        lines = []
        lines.append("#" * 13)
        lines.append("#" + "".join(map(format_entry, self.hallway)) + "#")
        for y in range(DEPTH, 0, -1):
            lines.append("###" + ("#".join(map(lambda r: format_entry(r.contents[y - 1]), self.rooms))) + "###")
        lines.append("  #########")
        return "\n".join(lines)


_min_energy = 9999999999999999999999999


def gather_moves(room_map):
    alt_maps = []
    for x_offset, bot in enumerate(room_map.hallway):
        if bot is None:
            continue
        target_room = room_map.room_for_bot(bot)
        if not target_room.can_accept():
            continue
        dir = 1 if target_room.offset > x_offset else -1
        x = x_offset + dir
        while x != target_room.offset and room_map.hallway[x] is None:
            x += dir
        if x == target_room.offset:
            for y_offset in range(DEPTH):
                v = target_room.contents[y_offset]
                if v is None:
                    new_room_map = room_map.move_to_room(x_offset, y_offset, target_room.name)
                    alt_maps.append(new_room_map)
                    break

    for room in room_map.rooms:
        if not room.can_move():
            continue
        y_offset = DEPTH - 1
        while y_offset >= 0 and room.contents[y_offset] is None:
            y_offset -= 1
        if y_offset < 0:
            continue
        available_hallway_slots = room_map.available_hallway_slots()
        x = room.offset - 1
        # left_moves = 0
        while x >= 0 and x in available_hallway_slots:
            new_room_map = room_map.move_to_hallway(room.name, y_offset, x)
            alt_maps.append(new_room_map)
            if x <= 1:
                x -= 1
            else:
                x -= 2
        x = room.offset + 1
        while x <= 11 and x in available_hallway_slots:
            new_room_map = room_map.move_to_hallway(room.name, y_offset, x)
            alt_maps.append(new_room_map)
            if x >= 9:
                x += 1
            else:
                x += 2
    return alt_maps


def print_moves(room_map):
    moves, alt_maps = gather_moves(room_map)
    for move in moves:
        print(f"    {move}")


for part, depth in (('p1', 2), ('p2', 4)):
    DEPTH = depth
    with open('input.txt') as f:
        lines = f.read().splitlines()
        hallway = [None] * 11
        room_a = Room('A', 2)
        room_b = Room('B', 4)
        room_c = Room('C', 6)
        room_d = Room('D', 8)
        for y_offset, room_line in enumerate(lines[2:4]):
            y_offset = DEPTH - 1 if y_offset == 0 else 0
            for room in (room_a, room_b, room_c, room_d):
                room.contents[y_offset] = room_line[room.offset + 1]
        if DEPTH == 4:
            room_a.contents[2] = 'D'
            room_a.contents[1] = 'D'
            room_b.contents[2] = 'C'
            room_b.contents[1] = 'B'
            room_c.contents[2] = 'B'
            room_c.contents[1] = 'A'
            room_d.contents[2] = 'A'
            room_d.contents[1] = 'C'
        room_map = Map(hallway, (room_a, room_b, room_c, room_d))
        queue = []
        heapq.heappush(queue, room_map)
        reached = {}
        min_complete = 999999999999
        while queue:
            room_map = heapq.heappop(queue)
            if room_map in reached and room_map.energy >= reached[room_map]:
                continue
            reached[room_map] = room_map.energy
            if room_map.energy > min_complete:
                continue
            alt_maps = gather_moves(room_map)
            for alt_map in alt_maps:
                if alt_map.done() and alt_map.energy < min_complete:
                    min_complete = alt_map.energy
                heapq.heappush(queue, alt_map)
        print(f"{part}: {min_complete}")
