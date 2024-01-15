import sys
import copy
import math
import time

f = open('inputs/doc_day_17.txt')
lines = f.read()
lines = lines.splitlines()
sys.setrecursionlimit(100000)

HEIGHT = len(lines)
WIDTH = len(lines[0])

def print_grid(grid, separator):
    for line in grid:
        print(separator.join([str(n) for n in line]))

def print_grid_with_path(grid, path, separator, indicator):
    for y, line in enumerate(grid):
        formated_line = []
        for  x, c in enumerate(line):
            formated_line.append(indicator+str(c) if (y,x) in path else str(c))
        print(separator.join(formated_line))

def get_grid(lines):
    grid = []
    for line in lines:
        grid.append([int(n) for n in line])
    return grid
grid = get_grid(lines)

def fill_heat_from_extreme(start, grid, dir):
    heats = copy.deepcopy(grid)
    seen = [start]
    currents = [start]
    while(len(currents)>0):
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


def is_straight(moves):
    y = moves[0][0]
    x = moves[0][1]
    straight_in_y = True
    straight_in_x = True
    for m in moves:
        if m[0] != y:
            straight_in_y = False
        if m[1] != x:
            straight_in_x = False
    return straight_in_y or straight_in_x


def is_path_valid(path):
    valid = True
    for i in range(0, len(path)-4):
        if not is_straight([path[i], path[i+1], path[i+2], path[i+3]]):
            valid = False
            break
    if valid:
        print(f'Validating path {path}')
    return valid
        

def h_score(p1, p2):
    y,x = p1
    p,q = p2
    return abs(p-y)+ abs(q-x)
    # return pow(p-y, 2)+ pow(q-x, 2)

def min_set(open_set):
    return min([cell for cell in open_set], key=lambda c: open_set[c]['f'])


# block = [(3,0), (3,1), (3,2), (3,3), (3,4), (3,5), (3,6), (3,7),\
#          (5,3), (5,4), (5,5), (5,6), (5,7), (5,8), (5,9), (5,10), (5,11), (5, 12)]

def a_start( start, end, heat_from_end):

    def build_path(seen):
        cell = end
        path = [end]
        while cell!= start:
            cell = seen[cell]
            path.append(cell)

        path.reverse()
        return path
         

    open_set = {}
    # open_set[start] = {
    #     'pos': start, 
    #     'f': (h_score(start, end)+0), 
    #     'g': 0}
    open_set[start] = {
        'pos': start, 
        'f': (h_score(start, end)+0), 
        'g': 0}
    seen = {}

    print(f'Before while: current open_set: {open_set}')
    while len(open_set)>0:
        current = open_set[min_set(open_set)]['pos']
        # print_grid_with_path(grid, build_path(seen), '\t', '#')
        # time.sleep(0.05)

        curr_f = open_set[current]['f']
        curr_g = open_set[current]['g']
        y,x = current
        print(f'- Current is {current}')
        print('- Open set is:')
        print(open_set)
        if current == end:
        # if current == end and is_path_valid(build_path(seen)):
        # if current == end :
            print_grid_with_path(grid, build_path(seen), '\t', '#')
            break
        
        open_set.pop(current)

        for next in [(y-1,x), (y+1,x), (y, x-1), (y, x+1)]:
            p,q = next
            # if p>=0 and q>=0 and p<HEIGHT and q<WIDTH and next not in seen and next not in block:
            if p>=0 and q>=0 and p<HEIGHT and q<WIDTH and next not in seen:
                if h_score(start, next) < 4 or (h_score(start, next) >=4 and not is_straight([next, current, seen[current], seen[seen[current]]]) ):
                # if h_score(start, next) < 4 or (h_score(start, next) >=4):
                    # prev_current = seen[current]
                    # line = [next, current, seen[current], seen[seen[current]]]
                    # temp_g = curr_g+1
                    temp_g = curr_g+grid[p][q]
                    temp_f = h_score(next, end) + temp_g

                    t_path = [next, current]
                    if current in seen:
                        t_path.append(seen[current])
                        if seen[current] in seen:
                            t_path.append(seen[seen[current]])
                            if seen[seen[current]] in seen:
                                t_path.append(seen[seen[seen[current]]])

                    print(f'At next/curr {next}/{current} Comparing: temp_f {temp_f} and curr_f {curr_f}')
                    if next in open_set:
                        if open_set[next]['f']< temp_f and (len(t_path)<5 or (len(t_path) == 5 and not is_straight(t_path))):
                            open_set[next] = {'pos': next, 'f': temp_f, 'g': temp_g}
                            seen[next] = current
                    elif (len(t_path)<5 or (len(t_path) == 5 and not is_straight(t_path))):
                        open_set[next] = {'pos': next, 'f': temp_f, 'g': temp_g}
                        seen[next] = current
            # print('\n')
            # print_grid_with_path(grid, [cell for cell in seen], '\t', '#' )
            # time.sleep(0.01)            
    return build_path(seen)

heat_from_end = fill_heat_from_extreme([HEIGHT-1, WIDTH-1], grid, 1)
start = (0, 0)
end = (HEIGHT-1, WIDTH-1)

less_path = a_start(start, end, heat_from_end)

print_grid_with_path(grid, less_path, '\t', '#' )