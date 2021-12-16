from dijkstra import dijkstra

with open('input.txt') as f:
    print(dijkstra([list(map(int, row)) for row in f.read().splitlines()]))
