import heapq
from collections import *


def dijkstra(matrix):
    edges = defaultdict(set)
    risks = {}
    for y, row in enumerate(matrix):
        for x, weight in enumerate(row):
            risks[(y, x)] = weight
            for yoffset, xoffset in [[0, 1], [0, -1], [1, 0], [-1, 0]]:
                neighbor_y, neighbor_x = y + yoffset, x + xoffset
                if neighbor_y < 0 or neighbor_x < 0 or neighbor_y >= len(matrix) or neighbor_x >= len(matrix[0]):
                    continue
                edges[(y, x)].add((neighbor_y, neighbor_x))
    current = (0, 0)
    distances = {node: None for node in edges}
    distances[current] = 0
    end = (len(matrix) - 1, len(matrix[0]) - 1)

    pq = [(0, current)]
    while pq:
        dist, current = heapq.heappop(pq)
        for neighbor in edges[current]:
            neighbor_dist = dist + risks[neighbor]
            if distances[neighbor] is None or neighbor_dist < distances[neighbor]:
                distances[neighbor] = neighbor_dist
                heapq.heappush(pq, (neighbor_dist, neighbor))
        if distances[end] != None:
            return distances[end]

    return distances[end]

