import time
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

def fill_next(grid, currents, distances):
    new_currents = []
    for current in currents:
        y = current['pos'][0]
        x = current['pos'][1]
        dis = distances[y][x]
        # print(f'- - Validating current {current["pos"]}')
        # print(f'- - - Current dis: {dis}')
        of_seen = copy.deepcopy(current['seen'])
        for next in ([[y-1, x], [y+1,x] ,[y,x-1], [y,x+1]]):
            if next[0]>=0 and next[1]>=0 and next[0]<=len(grid)-1 and next[1]<=len(grid[0])-1:
                # print(f'- - Validating next {next}')
                p = next[0]
                q = next[1]
                if(distances[p][q] == '.'):
                    distances[p][q] = dis + 1
                    new_seen  = copy.deepcopy(of_seen)
                    new_seen.append(next)
                    new_currents.append({
                        'pos': next,
                        'seen': new_seen
                    })
                elif(grid[p][q] == '>' and x+1 == q):
                    distances[p][q] = dis + 1
                    distances[p][q+1] = dis + 2
                    new_seen  = copy.deepcopy(of_seen)
                    new_seen.append(next)
                    new_seen.append([p, q+1])
                    new_currents.append({
                        'pos': [p, q+1],
                        'seen': new_seen
                    })
                elif(grid[p][q] == '<' and x-1 == q):
                    distances[p][q] = dis + 1
                    distances[p][q-1] = dis + 2
                    new_seen  = copy.deepcopy(of_seen)
                    new_seen.append(next)
                    new_seen.append([p, q-1])
                    new_currents.append({
                        'pos': [p, q-1],
                        'seen': new_seen
                    })
                elif(grid[p][q] == '^' and y-1 == p):
                    distances[p][q] = dis + 1
                    distances[p-1][q] = dis + 2
                    new_seen  = copy.deepcopy(of_seen)
                    new_seen.append(next)
                    new_seen.append([p-1, q])
                    new_currents.append({
                        'pos': [p-1, q],
                        'seen': new_seen
                    })
                elif(grid[p][q] == 'v' and y+1 == p):
                    distances[p][q] = dis + 1
                    distances[p+1][q] = dis + 2
                    new_seen  = copy.deepcopy(of_seen)
                    new_seen.append(next)
                    new_seen.append([p+1, q])
                    new_currents.append({
                        'pos': [p+1, q],
                        'seen': new_seen
                    })
                elif(isinstance(distances[p][q], int)):
                    # print(f'- - - Number found: {dis} at [{p},{q}] with char {distances[p][q]}')
                    if (distances[p][q]<dis+1 and [p,q] not in current['seen']):
                        if( grid[p][q] == '.' or (grid[p][q] == '>' and x+1 == q) or(grid[p][q] == '<' and x-1 == q) or(grid[p][q] == '^' and y-1 == p) or(grid[p][q] == 'v' and y+1 == p) ):
                            distances[p][q] = dis+1
                            new_seen  = copy.deepcopy(of_seen)
                            new_seen.append(next)
                            new_currents.append({
                                'pos': next,
                                'seen': new_seen
                            })


    return new_currents

def fill_distances(grid, start, end):
    distances = copy.deepcopy(grid)
    current = start
    seen = [start]
    currents = [
       {
            'pos' : current,
            'seen': seen
       }
    ]
    distances[start[0]][start[1]] = 0
    # print('- currents:')
    # print(currents)
    # print(len(currents))
    while len(currents)>0 :
        # for current in currents:
        #     if current['pos'] == end:
        #         print(f'- Reached end with steps: {distances[end[0]][end[1]]} ...', end = '\r')
        currents = fill_next(grid, currents, distances)
        print(f'- Concurrent paths {len(currents)}', end = '\r')
        # time.sleep(0.2)
        # print('-----------------------------------------------------------')
        # print_grid(distances)
    return distances

######################################################### PART 2

def fill_next2(grid, currents, distances):
    new_currents = []
    for current in currents:
        y = current['pos'][0]
        x = current['pos'][1]
        dis = distances[y][x]
        of_seen = copy.deepcopy(current['seen'])
        for next in ([[y-1, x], [y+1,x] ,[y,x-1], [y,x+1]]):
            if next[0]>=0 and next[1]>=0 and next[0]<=len(grid)-1 and next[1]<=len(grid[0])-1:
                # print(f'- - Validating next {next}')
                p = next[0]
                q = next[1]
                if(distances[p][q] == '.'):
                    distances[p][q] = dis + 1
                    new_seen  = copy.deepcopy(of_seen)
                    new_seen.append(next)
                    new_currents.append({
                        'pos': next,
                        'seen': new_seen
                    })
                elif('><v^'.find(grid[p][q])>=0 ):
                    distances[p][q] = dis + 1
                    new_seen  = copy.deepcopy(of_seen)
                    new_seen.append(next)
                    new_currents.append({
                        'pos': next,
                        'seen': new_seen
                    })
                elif(isinstance(distances[p][q], int)):
                    if (distances[p][q]<dis+1 and [p,q] not in current['seen']):
                            distances[p][q] = dis+1
                            new_seen  = copy.deepcopy(of_seen)
                            new_seen.append(next)
                            new_currents.append({
                                'pos': next,
                                'seen': new_seen
                            })
    return new_currents


def fill_distances2(grid, start, end):
    distances = copy.deepcopy(grid)
    current = start
    seen = [start]
    currents = [
       {
            'pos' : current,
            'seen': seen
       }
    ]
    distances[start[0]][start[1]] = 0
    while len(currents)>0 :
        currents = fill_next2(grid, currents, distances)
        print(f'- Concurrent paths {len(currents)}', end = '\r')
    return distances

############################## Execution

grid = get_grid(lines)
(start, end) = get_start_and_end(grid)
print('Wait for solution 1, it might take a while ...')
distances  = fill_distances(grid, start, end)
print('\n')
print(f"Solution 1: {distances[end[0]][end[1]]}")
print('\n')
print('Wait for solution 1, it might take a while ...')
distances2  = fill_distances2(grid, start, end)
print('\n')
print(f"Solution 2: {distances2[end[0]][end[1]]}")
