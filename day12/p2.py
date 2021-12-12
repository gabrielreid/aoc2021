from collections import *


def traverse(adj, current, path, small_visited, all_paths):
    if current.lower() == current:
        if max(small_visited.values(), default=0) == 2 and small_visited[current] > 0:
            return
        small_visited[current] += 1
    path.append(current)
    if current == 'end':
        all_paths.append(path)
    else:
        for adjacent in adj[current]:
            if adjacent == 'start':
                continue
            traverse(adj, adjacent, path[:], small_visited.copy(), all_paths)


with open('input.txt') as f:
    adj = defaultdict(set)
    for line in f.read().splitlines():
        start, end = line.split('-')
        adj[start].add(end)
        adj[end].add(start)
    all_paths = []
    traverse(adj, 'start', [], Counter(), all_paths)
    print(f"There are {len(all_paths)} paths")
