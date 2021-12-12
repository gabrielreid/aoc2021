from collections import *


def traverse(adj, current, path, small_visited, all_paths):
    if current in small_visited:
        return
    if current.lower() == current:
        small_visited.add(current)
    path.append(current)
    if current == 'end':
        all_paths.append(path)
    else:
        for adjacent in adj[current]:
            traverse(adj, adjacent, path[:], small_visited.copy(), all_paths)


with open('input.txt') as f:
    adj = defaultdict(set)
    for line in f.read().splitlines():
        start, end = line.split('-')
        adj[start].add(end)
        adj[end].add(start)
    all_paths = []
    traverse(adj, 'start', [], set(), all_paths)
    print(f"There are {len(all_paths)} paths")
