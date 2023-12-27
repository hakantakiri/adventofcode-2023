import copy
f = open('inputs/doc_day_23.txt')
lines = f.read()
lines = lines.splitlines()
# print(lines)

def print_grid(ar):
    for row in ar:
        print(('\t').join([str(x) for x in row]))   

def get_grid(lines):
    grid = []
    for line in lines:
        grid.append([c for c in line])
    return grid

def get_start_and_end(grid):
    start = [0, ''.join(grid[0]).find('.')]
    end = [len(grid)-1, ''.join(grid[len(grid)-1]).find('.')]
    return (start, end)

def fill_distances(grid):
    distance = copy.deepcopy(grid)
    grid = copy.deepcopy(grid)
    y=start[0]
    x=start[1]
    distance[y][x] = 0
    nexts = [start]
    while len(nexts) > 0:
        nexts = fill_next(nexts, distance, grid)
    return distance


def fill_next(edges, distances, grid):
    new_edges = []
    for current in edges:
        y = current[0]
        x = current[1]
        d = distances[y][x]
        for next in ([[y-1,x], [y+1,x], [y,x-1], [y,x+1]]):
            if next[0]>=0 and next[0]<=len(distances)-1 and next[1]>=0 and next[1]<=len(distances[0])-1:
                if distances[next[0]][next[1]] == '.':
                    distances[next[0]][next[1]] = d + 1
                    new_edges.append([next[0], next[1]])
                elif '>v<^'.find(str(distances[next[0]][next[1]]))>=0:
                    if grid[next[0]][next[1]] == '>' and  next[1] == x+1:
                        distances[next[0]][next[1]] = d + 1
                        if distances[next[0]][next[1]+1] == '.':
                            distances[next[0]][next[1]+1] = d+ 2
                            new_edges.append([next[0],next[1]+1])
                    if grid[next[0]][next[1]] == '<' and  next[1] == x-1:
                        distances[next[0]][next[1]] = d + 1
                        if distances[next[0]][next[1]-1] == '.':
                            distances[next[0]][next[1]-1] = d+2
                            new_edges.append([next[0],next[1]-1])
                    if grid[next[0]][next[1]] == 'v' and  next[0] == y+1:
                        distances[next[0]][next[1]] = d+1
                        if distances[next[0]+1][next[1]] == '.':
                            distances[next[0]+1][next[1]] = d+2
                            new_edges.append([next[0]+1,next[1]])
                    if grid[next[0]][next[1]] == '^' and  next[0] == y-1:
                        distances[next[0]][next[1]] = d+1
                        if distances[next[0]-1][next[1]] == '.':
                            distances[next[0]-1][next[1]] = d+2
                            new_edges.append([next[0]-1,next[1]])
                # elif isinstance(distances[next[0]][next[1]], int):
                #     dest_n = distances[next[0]][next[1]]
                #     curr_n = d
                #     if curr_n>dest_n+1 :
                #         print(f'intersection at: {next[0]}, {next[1]}')
                #         distances[next[0]][next[1]] = d+1
                #         new_edges.append([next[0], next[1]])
    return new_edges

def run_from_end(end, distances):
    route = [end]
    find_next(end, distances, route)
    return route

def find_next(current, distances, route):
    y = current[0]
    x = current[1]
    max = 0
    max_cord = []
    for next in ([[y-1,x], [y+1,x], [y,x-1], [y,x+1]]):
        if next[0]>=0 and next[0]<=len(distances)-1 and next[1]>=0 and next[1]<=len(distances[0])-1:
            if distances[next[0]][next[1]] != '#' and distances[next[0]][next[1]] > max and next not in route:
                max = distances[next[0]][next[1]]
                max_cord = next
    if len(max_cord) > 0:
        route.append(max_cord)
        find_next(max_cord, distances, route)


########################### Execution
grid = get_grid(lines)
(start, end) = get_start_and_end(grid)

distances = fill_distances(grid)
print_grid(distances)
print(f'Shortest distance to end: {distances[end[0]][end[1]]}')
# route = run_from_end(end, distances)
# print('Route')
# print(route)
# print(f'Solution 1: {len(route)}')

# print(f'Start is {start}, end is: {end}')

