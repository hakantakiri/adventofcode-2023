# --- Day 21: Step Counter ---
# You manage to catch the airship right as it's dropping someone else off on their all-expenses-paid trip to Desert Island! It even helpfully drops you off near the gardener and his massive farm.

# "You got the sand flowing again! Great work! Now we just need to wait until we have enough sand to filter the water for Snow Island and we'll have snow again in no time."

# While you wait, one of the Elves that works with the gardener heard how good you are at solving problems and would like your help. He needs to get his steps in for the day, and so he'd like to know which garden plots he can reach with exactly his remaining 64 steps.

# He gives you an up-to-date map (your puzzle input) of his starting position (S), garden plots (.), and rocks (#). For example:

# ...........
# .....###.#.
# .###.##..#.
# ..#.#...#..
# ....#.#....
# .##..S####.
# .##..#...#.
# .......##..
# .##.#.####.
# .##..##.##.
# ...........
# The Elf starts at the starting position (S) which also counts as a garden plot. Then, he can take one step north, south, east, or west, but only onto tiles that are garden plots. This would allow him to reach any of the tiles marked O:

# ...........
# .....###.#.
# .###.##..#.
# ..#.#...#..
# ....#O#....
# .##.OS####.
# .##..#...#.
# .......##..
# .##.#.####.
# .##..##.##.
# ...........
# Then, he takes a second step. Since at this point he could be at either tile marked O, his second step would allow him to reach any garden plot that is one step north, south, east, or west of any tile that he could have reached after the first step:

# ...........
# .....###.#.
# .###.##..#.
# ..#.#O..#..
# ....#.#....
# .##O.O####.
# .##.O#...#.
# .......##..
# .##.#.####.
# .##..##.##.
# ...........
# After two steps, he could be at any of the tiles marked O above, including the starting position (either by going north-then-south or by going west-then-east).

# A single third step leads to even more possibilities:

# ...........
# .....###.#.
# .###.##..#.
# ..#.#.O.#..
# ...O#O#....
# .##.OS####.
# .##O.#...#.
# ....O..##..
# .##.#.####.
# .##..##.##.
# ...........
# He will continue like this until his steps for the day have been exhausted. After a total of 6 steps, he could reach any of the garden plots marked O:

# ...........
# .....###.#.
# .###.##.O#.
# .O#O#O.O#..
# O.O.#.#.O..
# .##O.O####.
# .##.O#O..#.
# .O.O.O.##..
# .##.#.####.
# .##O.##.##.
# ...........
# In this example, if the Elf's goal was to get exactly 6 more steps today, he could use them to reach any of 16 garden plots.

# However, the Elf actually needs to get 64 steps today, and the map he's handed you is much larger than the example map.

# Starting from the garden plot marked S on your map, how many garden plots could the Elf reach in exactly 64 steps?

# Your puzzle answer was 3858.

# --- Part Two ---
# The Elf seems confused by your answer until he realizes his mistake: he was reading from a list of his favorite numbers that are both perfect squares and perfect cubes, not his step counter.

# The actual number of steps he needs to get today is exactly 26501365.

# He also points out that the garden plots and rocks are set up so that the map repeats infinitely in every direction.

# So, if you were to look one additional map-width or map-height out from the edge of the example map above, you would find that it keeps repeating:

# .................................
# .....###.#......###.#......###.#.
# .###.##..#..###.##..#..###.##..#.
# ..#.#...#....#.#...#....#.#...#..
# ....#.#........#.#........#.#....
# .##...####..##...####..##...####.
# .##..#...#..##..#...#..##..#...#.
# .......##.........##.........##..
# .##.#.####..##.#.####..##.#.####.
# .##..##.##..##..##.##..##..##.##.
# .................................
# .................................
# .....###.#......###.#......###.#.
# .###.##..#..###.##..#..###.##..#.
# ..#.#...#....#.#...#....#.#...#..
# ....#.#........#.#........#.#....
# .##...####..##..S####..##...####.
# .##..#...#..##..#...#..##..#...#.
# .......##.........##.........##..
# .##.#.####..##.#.####..##.#.####.
# .##..##.##..##..##.##..##..##.##.
# .................................
# .................................
# .....###.#......###.#......###.#.
# .###.##..#..###.##..#..###.##..#.
# ..#.#...#....#.#...#....#.#...#..
# ....#.#........#.#........#.#....
# .##...####..##...####..##...####.
# .##..#...#..##..#...#..##..#...#.
# .......##.........##.........##..
# .##.#.####..##.#.####..##.#.####.
# .##..##.##..##..##.##..##..##.##.
# .................................
# This is just a tiny three-map-by-three-map slice of the inexplicably-infinite farm layout; garden plots and rocks repeat as far as you can see. The Elf still starts on the one middle tile marked S, though - every other repeated S is replaced with a normal garden plot (.).

# Here are the number of reachable garden plots in this new infinite version of the example map for different numbers of steps:

# In exactly 6 steps, he can still reach 16 garden plots.
# In exactly 10 steps, he can reach any of 50 garden plots.
# In exactly 50 steps, he can reach 1594 garden plots.
# In exactly 100 steps, he can reach 6536 garden plots.
# In exactly 500 steps, he can reach 167004 garden plots.
# In exactly 1000 steps, he can reach 668697 garden plots.
# In exactly 5000 steps, he can reach 16733044 garden plots.
# However, the step count the Elf needs is much larger! Starting from the garden plot marked S on your infinite map, how many garden plots could the Elf reach in exactly 26501365 steps?

# Your puzzle answer was 636350496972143.

import math
import copy
f = open('inputs/doc_day_21.txt')
lines = f.read()
lines = lines.splitlines()

width = len(lines[0])
height = len(lines)

def print_grid(ar):
    for row in ar:
        print((' ').join([str(x) for x in row]))    

def get_grid(steps):
    current_max_steps = int((len(lines[0])-1)/2)
    grid = []
    for line in lines:
        grid.append( [c for c in line])
    start = get_start(grid)
    clean_grid = copy.deepcopy(grid)
    clean_grid[start[0]][start[1]] = '.'
    if steps > current_max_steps:
        repetition = math.floor((steps-current_max_steps-1)/len(lines[0]))+1
        r = 1
        while r <= repetition:
            extreme = []
            for line in clean_grid:
                extreme.append(line*(2*r+1))
            base = []
            j = 0
            while j< len(grid):
                base.append(clean_grid[j%(len(clean_grid))]
                            +grid[j]
                            +clean_grid[j%(len(clean_grid))])
                j+=1
            grid = extreme + base + extreme
            r+=1

    return grid

def get_start(grid):
    start = []
    for y, line in enumerate(grid):
        for x, c in enumerate(line):
            if c == 'S':
                start = [y, x]
    return start

def get_distances(grid, start):
    distances = [[-1 for x in range(len(grid[0]))] for y  in range(len(grid))]
    dis = 0
    y_min = len(grid) -1
    x_min = len(grid[0]) -1
    edge = []
    new_edge = [start]

    while len(new_edge) > 0:
        edge = copy.deepcopy(new_edge)
        new_edge = []
        for e in edge:
            if e[0] == start[0] and e[1] == start[1]:
                distances[e[0]][e[1]] = 0
            if  e[0]-1 >=0 and distances[e[0]-1][e[1]] == -1 and grid[e[0]-1][e[1]] != '#':
                distances[e[0]-1][e[1]] = dis+1
                new_edge.append([e[0]-1,e[1]])
            if  e[0]+1 <= y_min and distances[e[0]+1][e[1]] == -1 and grid[e[0]+1][e[1]] != '#' :
                distances[e[0]+1][e[1]] = dis+1
                new_edge.append([e[0]+1,e[1]])
            if  e[1]-1 >= 0 and distances[e[0]][e[1]-1] == -1 and grid[e[0]][e[1]-1] != '#':
                distances[e[0]][e[1]-1] = dis+1
                new_edge.append([e[0],e[1]-1])
            if  e[1]+1 <= x_min and distances[e[0]][e[1]+1] == -1 and grid[e[0]][e[1]+1] != '#':
                distances[e[0]][e[1]+1] = dis+1
                new_edge.append([e[0],e[1]+1])
        dis+=1
    return distances


def get_spaces(steps):   
    grid = get_grid(steps)
    start = get_start(grid) 
    distances = get_distances(grid, start)
    even = True
    if steps%2 == 1:
        even = False
    count = 0
    for y,row in enumerate(distances):
        for x, d in enumerate(row):
            if d >=0 and d <=steps:
                if (even == True):
                    if d%2 == 0:
                        count +=1
                else:
                    if d%2 == 1:
                        count +=1
    return count


print(f'Solution 1: {get_spaces(64)}')

steps = 26501365

# for s in range(1, steps+1):
#     if(s == int((width-1)/2)) or (s-int((width-1)/2))%width == 0:
#         print(f'{s}\t{get_spaces(s)}')

# for s in range(1, steps):
#     print(f'{s}\t{get_spaces(s)}')


## Solution 2 for sample
# base =  [1146,1196,1256,1324,1383,1464,1528,1594,1653,1735,1805]
# comp = [707,718,732,748,762,780,796,812,826,844,860]
# iterator = 162
# b = base[(steps-43)%width]
# c = comp[(steps-43)%width]
# t = math.floor((steps-43)/width)
# print(f'base {b}')
# print(f'comp {c}')
# print(f'times {t}')

# pos = int(b+ c*t + ((t*(t-1))/2)*iterator)
# print(f'{steps}\t{pos}')
    
## Solution 2
base =  [3943,4122,4211,4394,4461,4638,4723,4896,4988,5174,5270,5444,5552,5723,5837,6019,6134,6316,6430,6624,6740,6926,7053,7251,7382,7574,7715,7905,8049,8242,8383,8590,8733,8934,9080,9288,9442,9649,9811,10018,10199,10405,10587,10798,10973,11188,11365,11599,11778,11995,12182,12413,12606,12830,13030,13269,13481,13704,13927,14157,14380,14628,14849,15082,15304,15537,15779,16013,16254,16480,16746,16988,17255,17499,17761,17989,18278,18509,18801,19025,19329,19554,19847,20073,20385,20613,20916,21155,21453,21718,22023,22291,22597,22851,23156,23414,23731,24004,24319,24592,24919,25193,25519,25801,26120,26396,26750,27022,27386,27661,28027,28275,28642,28908,29291,29550,29931,30192,30593,30853,31261,31515,31939,32195,32646,32868,33330,33550,34074,34337,34871]
comp = [31183,31537,31707,32061,32205,32525,32674,32986,33153,33462,33635,33933,34114,34401,34585,34873,35055,35335,35522,35814,35999,36271,36471,36756,36954,37228,37439,37693,37903,38160,38369,38637,38846,39103,39309,39571,39776,40036,40243,40499,40724,40979,41202,41457,41667,41922,42131,42401,42606,42858,43064,43331,43543,43800,44013,44280,44501,44744,44977,45222,45453,45710,45938,46176,46401,46635,46876,47107,47343,47563,47821,48053,48306,48540,48782,49001,49262,49480,49738,49946,50212,50419,50676,50878,51151,51349,51611,51816,52069,52294,52551,52776,53030,53241,53495,53702,53963,54176,54433,54642,54906,55115,55376,55590,55846,56052,56327,56529,56809,57011,57289,57469,57748,57939,58223,58409,58689,58876,59164,59350,59639,59814,60117,60294,60605,60761,61080,61225,61576,61754,62111]
iterator = 31098
b = base[(steps-65)%width]
c = comp[(steps-65)%width]
t = math.floor((steps-65)/width)
pos = int(b+ c*t + ((t*(t-1))/2)*iterator)

print(f'Solution 2: {pos}')

