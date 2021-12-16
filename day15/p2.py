from dijkstra import dijkstra

with open('input.txt') as f:
    matrix = [list(map(int, row)) for row in f.read().splitlines()]
    for row in matrix:
        width = len(row)
        for expand_x in range(4):
            for v in row[width * expand_x:]:
                row.append(v + 1 if v < 9 else 1)

    height = len(matrix)
    for expand_y in range(4):
        for row in matrix[height * expand_y:]:
            matrix.append([v + 1 if v < 9 else 1 for v in row])


    print(dijkstra(matrix))