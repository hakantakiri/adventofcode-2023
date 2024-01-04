import time
import copy
import math

f = open('inputs/doc_day_17.txt')
lines = f.read()
lines = lines.splitlines()

WIDTH = len(lines[0])-1
HEIGHT = len(lines)-1
print(f'width: {WIDTH}, height: {HEIGHT}')

def print_grid(grid, separator):
    for line in grid:
        print(separator.join([str(n) for n in line]))

def print_grid_with_path(grid, path, separator, indicator):
    for y, line in enumerate(grid):
        formated_line = []
        for  x, c in enumerate(line):
            formated_line.append(indicator+str(c) if [y,x] in path else str(c))
        print(separator.join(formated_line))

def get_grid(lines):
    grid = []
    for line in lines:
        grid.append([int(n) for n in line])
    return grid

def fill_heat_from_extreme(start, grid, dir):
    heats = copy.deepcopy(grid)
    seen = [start]
    currents = [start]
    while(len(currents)>0):
        # time.sleep(1)
        # print('\n')
        # print_grid(heats)
        currents = next_heat(currents, seen, heats, grid, dir)
    return heats

def next_heat(currents, seen,  heats, grid, dir):
    new_currents = []
    for current in currents:
        y = current[0]
        x = current[1]
        nexts = [[y+1, x], [y, x+1]] if dir == 0 else [[y-1, x], [y, x-1]]
        for next in (nexts):
            p = next[0]
            q = next[1]
            if(p>=0 and q>=0 and p <= len(heats)-1 and q <= len(heats[0])-1):
                if next not in seen:
                    heats[p][q] = grid[p][q]+ heats[y][x]
                    seen.append(next)
                    new_currents.append(next)
                else:
                    if ( grid[p][q]+ heats[y][x]) < heats[p][q]:
                        heats[p][q] = grid[p][q]+ heats[y][x]
                        if next not in seen:
                            seen.append(next)
                        if next not in new_currents:
                            new_currents.append(next)
    return new_currents

def find_shortest(heats, start, end):
    path = [start]
    while path[-1] != end:
        y = path[-1][0]
        x = path[-1][1]
        mins = math.inf
        min_coord = None
        for next in ([y-1, x], [y+1, x] ,[y, x-1],[y, x+1] ):
            p = next[0]
            q = next[1]
            if( p >= 0 and q >= 0 and p <= len(heats)-1 and q <= (len(heats[0])-1)):
                if heats[p][q] < mins:
                    mins = heats[p][q]
                    min_coord = next
                elif heats[p][q] == mins:
                    print(f'Found bifurcation at {path[-1]}')
        path.append(min_coord)
    return path

def get_sides(path):
    start = 0
    lines = []
    for i in range(1, len(path)-1):
        prev = path[i-1]
        next = path[i+1]
        if prev[0]!=next[0] and prev[1]!=next[1]: #corner
            lines.append([start, i])
            start = i
    lines.append([start, i+1])
    return lines

def count_valid_sides(path, max_length):
    sides = get_sides(path)
    count = 0
    for side in sides:
        if side[1]-side[0]+1 <= max_length:
            count += 1
    return count
def count_invalid_sides(path, max_length):
    sides = get_sides(path)
    count = 0
    for side in sides:
        if side[1]-side[0]+1 > max_length:
            count += 1
    return count


def heatloss(grid, path):
    sum = 0
    for p in path:
        sum = sum + grid[p[0]][p[1]]
    return sum

def adjust_path (grid, path, banned):
    lines = get_sides(path)
    corners =  []
    for i in range(0, len(lines)-1):
        prev = path[lines[i][1]-1]
        curr = path[lines[i][1]]
        next = path[lines[i][1]+1]
        corners.append({
            'idx': lines[i][1] ,
            'new': [next[0], prev[1] ] if prev[0] == curr[0] else  [prev[0], next[1]],
            'replaces': curr,
            'lines': [lines[i], lines[i+1]]
        })
    
    candidates_lines = [] # To expand
    for line in lines:
        if line[1]-line[0]+1<=10 and line[1]-line[0]+1 > 4:
            candidates_lines.append(line)
    if(len(candidates_lines)>0):
        print(f'----- Should try sides')

    min_augmentation = math.inf
    min = {}

    for corn in corners:
        if corn['new'] not in banned  and \
        grid[corn['new'][0]][corn['new'][1]]-grid[corn['replaces'][0]][corn['replaces'][1]] < min_augmentation:
            test_path = copy.deepcopy(path)
            test_path[corn['idx']] = corn['new']
            if(count_invalid_sides(test_path, 4) <= count_invalid_sides(path, 4)):
                min = corn
                min_augmentation = grid[corn['new'][0]][corn['new'][1]]
    path[min['idx']] = min['new']
    banned.append(min['replaces'])

    return path



################################## EXECUTION

start = [0, 0]
end = [HEIGHT, WIDTH]
grid = get_grid(lines)
# print_grid(grid)

heat_from_end = fill_heat_from_extreme(end, grid, 1)
print_grid(heat_from_end, '\t')

path  = find_shortest(heat_from_end, start, end)
print('\n')
print_grid_with_path(grid, path, '\t', '#')

lines = get_sides(path)
print(f'Lines:')
print(lines)
print(f'Heatloss: {heatloss(grid, path)}')

banned = []
for i in range(0, 100 ):
    print(f'\nAdjusted path, iteration: {i+1}')
    adjust_path(grid, path, banned)
    print(f'New heatloss: {heatloss(grid, path)}')
    print(f'Banned: {len(banned)}')
    # print(get_valid_lines(adjust_path(grid, path)))
    print_grid_with_path(grid, path, '\t', '#')
    time.sleep(1)