import sys
import copy
import math
import time

f = open('inputs/doc_day_17.txt')
lines = f.read()
lines = lines.splitlines()
sys.setrecursionlimit(100000)

WIDTH = len(lines[0])
HEIGHT = len(lines)
# print(lines)
# print(f'width: {WIDTH}, height: {HEIGHT}')

def print_grid(grid, separator):
    for line in grid:
        print(separator.join([str(n) for n in line]))

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


def print_grid_with_path(grid, path, separator, indicator):
    for y, line in enumerate(grid):
        formated_line = []
        for  x, c in enumerate(line):
            formated_line.append(indicator+str(c) if [y,x] in path else str(c))
        print(separator.join(formated_line))

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

def order(next):
    p = next[0]
    q = next[1]
    if (p<HEIGHT and q<WIDTH and p >= 0 and q >= 0 ) :
        return heat_from_end[p][q]
    else :
        return math.inf

grid = get_grid(lines)
heat_from_end = fill_heat_from_extreme([HEIGHT-1, WIDTH-1], grid, 1)
# conc = [0]
min_loss = [math.inf]
def move(pos, loss, path):
    # conc[0]+=1
    # print(f'- Evaluating concurrents {conc[0]}\t\t\t', end='\r')
    y = pos[0]
    x = pos[1]
    # for next in ([ [y+1, x],  [y-1, x], [y, x-1] ,[y, x+1]  ]):
    for next in (sorted([  [y+1, x],  [y-1, x], [y, x-1] ,[y, x+1] ], key= order)):
        # print(f'Trying next {next}')
        p = next[0]
        q = next[1]
        if (p<HEIGHT and q<WIDTH and p >= 0 and q >= 0 ) :
            if next not in path:
                # print(f'Is not previous')
                ver = [next]
                ver.append(pos)
                if len(path)>=2:
                    ver.append(path[-2])
                if len(path)>= 3:
                    ver.append(path[-3])
                if len(path)>= 4:
                    ver.append(path[-4])
                # print(f'-- path to verify {ver}')
                if len(ver)<=4 or ( len(ver)==5 and not is_straight(ver)):
                    # print(f'--- Is not straight')
                    # if( loss + heat_from_end[p][q] < min_loss[0]):
                    # n=[]
                    # for cur in path:
                    #     n.append(grid[cur[0]][cur[1]])
                    # loss = sum(n)
                    if( loss+heat_from_end[p][q]  < min_loss[0]):
                        new_path = copy.deepcopy(path)
                        new_path.append(next)
                        n_loss = loss + int(grid[p][q])
                        if next == [HEIGHT-1, WIDTH-1]:
                            if n_loss < min_loss[0]:
                                min_loss[0] = n_loss
                                # print(f'- Found a path with loss: {loss} to path: {new_path}')
                                print('\n')
                                print(f'Current loss: {n_loss}, min is: {min_loss[0]}')
                                # print(new_path)
                                # print_grid_with_path(lines, new_path, '\t', '#')
                                # time.sleep(0.1)
                                # return (new_path, loss)
                                # continue
                                return
                        else:
                            move(next, n_loss, new_path)

def part_1():
    move([0,0], 0, [[0,0]])
    # print(f'Found path: {path} with loss: {loss}')
    return 

# print_grid(heat_from_end, '\t')

print(f'Solution 1: {part_1()}')

# print('\n')
# path = [[0, 0], [0, 1], [0, 2], [0, 3], [1, 3], [1, 4], [2, 4], [2, 5], [2, 6], [2, 7], [3, 7], [3, 8], [3, 9], [3, 10], [4, 10], [4, 11], [4, 12], [5, 12], [6, 12], [7, 12], [7, 11], [8, 11], [9, 11], [9, 12], [10, 12], [11, 12], [12, 12]]
# print_grid_with_path(lines, path, '\t', '#')
# print('\n')
# print_grid(grid, '\t')