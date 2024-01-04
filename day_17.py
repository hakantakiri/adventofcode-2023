import time
import copy
import math
f = open('inputs/doc_day_17.txt')
lines = f.read()
lines = lines.splitlines()

WIDTH = len(lines[0])
HEIGHT = len(lines)
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
    print(f'Path is: {path[-1]} with heatloss: {heats[0][0]}')
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

def generate_corners(max_length, heats, path):
    dir = 'r' if(path[0][0] == path[1][0]) else 'd'
    i = 0
    dir_count = 0
    while i< len(path)-1:
        i+=1
        # print(f'Working at position {i} -> {path[i]}, dir: {dir}, dir_count: {dir_count}')
        # print(f' - With path: {path[0:i+5]} ...')
        curr = path[i]
        y = curr[0]
        x = curr[1]
        prev = path[i-1]
        py = prev[0]
        px = prev[1]
        c_dir = dir
        if y>py:#moves down
            c_dir = 'd'
        elif y<py: #moves up
            c_dir = 'u'
        elif  x> px: # moves right
            c_dir = 'r'
        elif x<px: # moving left
            c_dir = 'l'

        if(c_dir != dir):
            dir_count = 1
            dir = c_dir
        else:
            dir_count += 1

        if dir_count == max_length+1:
            min_change = math.inf
            min_coord = None
            new_path_i = None
            if dir == 'u':
                for next in [[py, x-1], [py, x+1]]:
                    if next[1] >= 0 and next[1]<= len(heats[0])-1:
                        if(heats[next[0]][next[1]]< min_change):
                            min_change = heats[next[0]][next[1]]
                            min_coord = next
                            new_path_i= [y, min_coord[1]]
            elif dir == 'd':
                for next in [[py, x-1], [py, x+1]]:
                    if next[1] >= 0 and next[1]<= len(heats[0])-1:
                        if(heats[next[0]][next[1]]< min_change):
                            min_change = heats[next[0]][next[1]]
                            min_coord = next
                            new_path_i =[y, min_coord[1]]
            elif dir == 'r':
                for next in [[y+1, px], [y-1, px]]:
                    if next[0] >= 0 and next[0]<= len(heats)-1:
                        if(heats[next[0]][next[1]]< min_change):
                            min_change = heats[next[0]][next[1]]
                            min_coord = next
                            new_path_i =[min_coord[0], x]
            elif dir == 'l':
                for next in [[y+1, px], [y-1, px]]:
                    if next[0] >= 0 and next[0]<= len(heats)-1:
                        if(heats[next[0]][next[1]]< min_change):
                            min_change = heats[next[0]][next[1]]
                            min_coord = next
                            new_path_i =[min_coord[0], x]
            else:
                print('wdf')
            path.insert(i, min_coord)
            path.insert(i+1, new_path_i)
            dir_count-=2
            i-=2

    return path

def update_heats_to_path(heats, path, grid):
    new_heats = copy.deepcopy(heats)
    for y, line in enumerate(new_heats):
        for x, n in enumerate(line):
            new_heats[y][x] = 0

    i = len(path)-1
    sum = 0
    while i>=0:
        p = path[i]
        y = p[0]
        x = p[1]
        new_heats[y][x] = grid[y][x]+sum
        sum = grid[y][x]+sum
        i-=1
    
    i = len(path)-1
    while i>=0:
        y = path[i][0]
        x = path[i][1]  
        for around in [[y-1, x], [y+1, x], [y, x-1] ,[y, x+1]]:
            p = around[0]
            q = around[1]
            if p>=0 and q>=0 and p<=len(new_heats)-1 and q<=len(new_heats[0])-1:
                if(around not in path):
                    print('Around found')
                    if( (new_heats[y][x] + grid[p][q] ) < new_heats[p][q] or new_heats[p][q] == 0):
                        print(f'-- updated suround {heats[p][q]}')
                        new_heats[p][q] = new_heats[y][x] + grid[p][q]

        i-=1

    return new_heats 

def get_weights_in_path(grid, path):
    weights_in_path = copy.deepcopy(path)
    i = 0
    while i<=len(path)-1:
        min_w = math.inf
        for span in [
            [i-3 ,i-2 ,i-1 ,i],
            [i-2 ,i-1 ,i ,i+1],
            [i-1 ,i ,i+1 ,i+2],
            [i ,i+1 ,i+2 ,i+3]
        ]:
            sum = 0
            for s in span:
                if s>=0 and s<=len(path)-1:
                    sum = sum + grid[path[s][0]][path[s][1]]
                
            if sum<min_w:
                min_w = sum
        print(f'Update weight {min_w} at indes { i} in weights')
        weights_in_path[i] = min_w
        i+=1

    grid_with_weights = copy.deepcopy(grid)
    for j, p in enumerate(path):
        grid_with_weights[p[0]][p[1]] = weights_in_path[j]

    return (grid_with_weights, weights_in_path)
################################## EXECUTION

start = [0, 0]
end = [HEIGHT-1, WIDTH-1]
grid = get_grid(lines)
# print_grid(grid)

heat_from_end = fill_heat_from_extreme(end, grid, 1)
print_grid(heat_from_end, '\t')
# heat_from_start = fill_heat_from_extreme(start, grid, 0)
# print_grid(heat_from_start, '\t')
path  = find_shortest(heat_from_end, start, end)
print('\n')
print_grid_with_path(heat_from_end, path, '\t', '#')

# print('Atered path: ')
# new_path = generate_corners(3, heat_from_end, path)
# print_grid_with_path(heat_from_end, new_path, '\t', '#')

print('Weights in path:')
(grid_with_weights, weights) = get_weights_in_path(grid, path)

# print('Updated heats: ')
# updated_heats = update_heats_to_path(heat_from_end, new_path, grid)
# print_grid_with_path(updated_heats, new_path, '\t', '#')

print('grid with weights in path: ')
print_grid_with_path(grid_with_weights, path, '\t', '#')







# shortest_path = find_shortest(heat_from_end_to_start, start, end)
# print(f'Shortes path with {len(shortest_path)} is:')
# print(shortest_path)
# print(f'grid is')
# print_grid_with_path(grid, shortest_path, '\t', '#')
# print('\n')
# print_grid_with_path(heat_from_end_to_start, shortest_path, '\t', '#')














# def fill_min(txt):
#     def lan(c):
#         if c.isdigit():
#             return c
#         else:
#             return 'A'
        
#     # m = min(txt, key=lan)
#     m = max(txt )
#     print(f'min is {m}')
#     txt = txt.replace(m, ' ')
#     return txt

# def print_state(txt, w):
#     row = ''
#     for i, c in enumerate(txt):
#         row = row + c
#         if ((i+1)%w == 0):
#             row += '\n'
#     return row

# start = [0,0]
# end = [HEIGHT-1, WIDTH-1]
# n_start = int(lines[start[0]][start[1]])
# n_end = int(lines[end[0]][end[1]])
# n_min = max([n_start, n_end])
# n_max = int(max(text))

# j = n_max
# while j> n_min:
#     text = fill_min(text)
#     j-=1

# print(print_state(text, WIDTH))

