import operator
from functools import *

OPS = [sum, partial(reduce, operator.mul), min, max, None,
       partial(reduce, operator.gt), partial(reduce, operator.lt), partial(reduce, operator.eq)]


class LiteralPacket:
    def __init__(self, version, type_id, value):
        self.version = version
        self.type_id = type_id
        self.value = value


class OperatorPacket:
    def __init__(self, version, type_id, operand_packets):
        self.version = version
        self.type_id = type_id
        self.operand_packets = operand_packets


class BinaryStream:
    def __init__(self, binary):
        self.binary = binary
        self.offset = 0

    def take(self, n):
        val = self.binary[self.offset:self.offset + n]
        self.offset += n
        return val

    def empty(self):
        return self.offset >= len(self.binary)


def parse_literal(stream):
    literal = []
    while not stream.empty():
        part = stream.take(5)
        literal.append(part[1:])
        if part[0] == '0':
            break
    return int("".join(literal), 2)


def parse_operators(stream):
    length_type = int(stream.take(1))
    if length_type == 0:
        total_len = int(stream.take(15), 2)
        sub_stream = BinaryStream(stream.take(total_len))
        sub_values = []
        while not sub_stream.empty():
            sub_values.append(parse_packet(sub_stream))
        return sub_values
    elif length_type == 1:
        num_packets = int(stream.take(11), 2)
        return [parse_packet(stream) for _ in range(num_packets)]


def parse_packet(stream):
    version = int(stream.take(3), 2)
    type_id = int(stream.take(3), 2)
    if type_id == 4:
        return LiteralPacket(version, type_id, parse_literal(stream))
    else:
        return OperatorPacket(version, type_id, parse_operators(stream))


def version_sum(packet):
    if isinstance(packet, LiteralPacket):
        return packet.version
    else:
        return packet.version + sum(map(version_sum, packet.operand_packets))


def eval_packet(packet):
    if isinstance(packet, LiteralPacket):
        return packet.value
    else:
        return OPS[packet.type_id](list(map(eval_packet, packet.operand_packets)))


with open('input.txt') as f:
    stream = BinaryStream("".join(map(lambda c: "{:04b}".format(int(c, 16)), next(f).strip())))
    packet = parse_packet(stream)
    print(f"version sum = {version_sum(packet)}")
    print(f"result = {eval_packet(packet)}")
