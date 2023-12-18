# --- Day 16: The Floor Will Be Lava ---
# With the beam of light completely focused somewhere, the reindeer leads you deeper still into the Lava Production Facility. At some point, you realize that the steel facility walls have been replaced with cave, and the doorways are just cave, and the floor is cave, and you're pretty sure this is actually just a giant cave.

# Finally, as you approach what must be the heart of the mountain, you see a bright light in a cavern up ahead. There, you discover that the beam of light you so carefully focused is emerging from the cavern wall closest to the facility and pouring all of its energy into a contraption on the opposite side.

# Upon closer inspection, the contraption appears to be a flat, two-dimensional square grid containing empty space (.), mirrors (/ and \), and splitters (| and -).

# The contraption is aligned so that most of the beam bounces around the grid, but each tile on the grid converts some of the beam's light into heat to melt the rock in the cavern.

# You note the layout of the contraption (your puzzle input). For example:

# .|...\....
# |.-.\.....
# .....|-...
# ........|.
# ..........
# .........\
# ..../.\\..
# .-.-/..|..
# .|....-|.\
# ..//.|....
# The beam enters in the top-left corner from the left and heading to the right. Then, its behavior depends on what it encounters as it moves:

# If the beam encounters empty space (.), it continues in the same direction.
# If the beam encounters a mirror (/ or \), the beam is reflected 90 degrees depending on the angle of the mirror. For instance, a rightward-moving beam that encounters a / mirror would continue upward in the mirror's column, while a rightward-moving beam that encounters a \ mirror would continue downward from the mirror's column.
# If the beam encounters the pointy end of a splitter (| or -), the beam passes through the splitter as if the splitter were empty space. For instance, a rightward-moving beam that encounters a - splitter would continue in the same direction.
# If the beam encounters the flat side of a splitter (| or -), the beam is split into two beams going in each of the two directions the splitter's pointy ends are pointing. For instance, a rightward-moving beam that encounters a | splitter would split into two beams: one that continues upward from the splitter's column and one that continues downward from the splitter's column.
# Beams do not interact with other beams; a tile can have many beams passing through it at the same time. A tile is energized if that tile has at least one beam pass through it, reflect in it, or split in it.

# In the above example, here is how the beam of light bounces around the contraption:

# >|<<<\....
# |v-.\^....
# .v...|->>>
# .v...v^.|.
# .v...v^...
# .v...v^..\
# .v../2\\..
# <->-/vv|..
# .|<<<2-|.\
# .v//.|.v..
# Beams are only shown on empty tiles; arrows indicate the direction of the beams. If a tile contains beams moving in multiple directions, the number of distinct directions is shown instead. Here is the same diagram but instead only showing whether a tile is energized (#) or not (.):

# ######....
# .#...#....
# .#...#####
# .#...##...
# .#...##...
# .#...##...
# .#..####..
# ########..
# .#######..
# .#...#.#..
# Ultimately, in this example, 46 tiles become energized.

# The light isn't energizing enough tiles to produce lava; to debug the contraption, you need to start by analyzing the current situation. With the beam starting in the top-left heading right, how many tiles end up being energized?

# Your puzzle answer was 8146.

# --- Part Two ---
# As you try to work out what might be wrong, the reindeer tugs on your shirt and leads you to a nearby control panel. There, a collection of buttons lets you align the contraption so that the beam enters from any edge tile and heading away from that edge. (You can choose either of two directions for the beam if it starts on a corner; for instance, if the beam starts in the bottom-right corner, it can start heading either left or upward.)

# So, the beam could start on any tile in the top row (heading downward), any tile in the bottom row (heading upward), any tile in the leftmost column (heading right), or any tile in the rightmost column (heading left). To produce lava, you need to find the configuration that energizes as many tiles as possible.

# In the above example, this can be achieved by starting the beam in the fourth tile from the left in the top row:

# .|<2<\....
# |v-v\^....
# .v.v.|->>>
# .v.v.v^.|.
# .v.v.v^...
# .v.v.v^..\
# .v.v/2\\..
# <-2-/vv|..
# .|<<<2-|.\
# .v//.|.v..
# Using this configuration, 51 tiles are energized:

# .#####....
# .#.#.#....
# .#.#.#####
# .#.#.##...
# .#.#.##...
# .#.#.##...
# .#.#####..
# ########..
# .#######..
# .#...#.#..
# Find the initial beam configuration that energizes the largest number of tiles; how many tiles are energized in that configuration?

# Your puzzle answer was 8358.

import copy
import sys
f = open('inputs/doc_day_16.txt')
lines = f.read()
lines = lines.splitlines()
grid = []
for line in lines:
    g = []
    for c in line:
        g.append(c)
    grid.append(g)
    
def get_starts(grid):
    min_y =0
    max_y = len(grid)-1
    min_x = 0
    max_x = len(grid[0])-1
    starts = []

    y = min_y
    while  y<= max_y:
        starts.append([[y, min_x], 'r'])
        starts.append([[y, max_x], 'l'])
        y+=1
    
    x = min_x
    while x <= max_x:
        starts.append([[min_y, x], 'd'])
        starts.append([[max_y, x], 'u'])
        x+=1
    return starts

def calculate_dir (current, prev):
    y = current[0] - prev[0]
    x = current[1] - prev[1]
    if y ==-1 : return 'u'
    if y == 1 : return 'd'
    if x ==-1 : return 'l'
    if x == 1 : return 'r'

def find_next( current, dir):
    ns = []
    y = current[0]
    x = current[1]
    c = grid[y][x]

    if (c == '.'):
        if dir == 'r':
            ns.append([[y, x+1], dir])
        if dir == 'l':
            ns.append([[y, x-1], dir])
        if dir == 'u':
            ns.append([[y-1, x], dir])
        if dir == 'd':
            ns.append([[y+1, x], dir])
    if (c == '/'):
        if dir == 'r':
            ns.append([[y-1, x], 'u'])
        if dir == 'l':
            ns.append([[y+1, x], 'd'])
        if dir == 'u':
            ns.append([[y, x+1], 'r'])
        if dir == 'd':
            ns.append([[y, x-1], 'l'])
    if (c == '\\'):
        if dir == 'r':
            ns.append([[y+1, x], 'd'])
        if dir == 'l':
            ns.append([[y-1, x], 'u'])
        if dir == 'u':
            ns.append([[y, x-1], 'l'])
        if dir == 'd':
            ns.append([[y, x+1], 'r'])
    if (c == '|'):
        if dir == 'r':
            ns.append([[y-1, x], 'u'])
            ns.append([[y+1, x], 'd'])
        if dir == 'l':
            ns.append([[y-1, x], 'u'])
            ns.append([[y+1, x], 'd'])
        if dir == 'u':
            ns.append([[y-1, x], 'u'])
        if dir == 'd':
            ns.append([[y+1, x], 'd'])

    if (c == '-'):
        if dir == 'r':
            ns.append([[y, x+1], 'r'])
        if dir == 'l':
            ns.append([[y, x-1], 'l'])
        if dir == 'u':
            ns.append([[y, x-1], 'l'])
            ns.append([[y, x+1], 'r'])
        if dir == 'd':
            ns.append([[y, x-1], 'l'])
            ns.append([[y, x+1], 'r'])

    return ns

def draw_energy(grid, energized):
    draw = copy.deepcopy(grid)

    for e in energized:
        c = e[0]
        pos = e[1]
        draw[pos[0]][pos[1]] = '#'
    
    text = ''
    for line in draw:
        l = ''
        for c in line:
            l = l+c
        text = text + l + '\n'
    return [draw, text]

def run(current, dir, energized, unique):
    y = current[0]
    x = current[1]
    if( x >=0 and y >=0 and x <= (len(grid[0])-1) and y <= (len(grid) -1)): 
        c = grid[y][x]
        if [c, [y,x], dir] in energized:
            return
        else:
            if [y,x] not in unique:
                unique.append([y,x])
            energized.append([c, [y, x], dir])
        ns = find_next(current, dir)
        for next in ns:
            new_current = next[0]
            new_dir = next[1]
            run(new_current, new_dir, energized, unique)
    else:
        return


def part1():
    dir = 'r'
    current = [0, 0]
    energized = []
    unique = []
    run(current,  dir,  energized, unique)
    return [energized, unique]

def part2(starts):
    solutions = []
    for s in starts:
        energized = []
        unique = []
        run(s[0],  s[1],  energized, unique)
        solutions.append([energized, unique])
        print(f'- For start {s[0]}, with dir: {s[1]} energy is: {len(unique)}')
    return solutions


sys.setrecursionlimit(10000)

print(f'Wait for solution 1, it may take a while ...')
[energized, unique] = part1()
print(f'Solution 1: {len(unique)}')

print(f'Wait for solution 2, it may take a while ...')
starts = get_starts(grid)

solutions = part2(starts)
max = -1
for s in solutions:
    if len(s[1]) > max:
        max = len(s[1])

print(f'Solution 2: {max}')