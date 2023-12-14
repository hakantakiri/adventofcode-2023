# --- Day 14: Parabolic Reflector Dish ---
# You reach the place where all of the mirrors were pointing: a massive parabolic reflector dish attached to the side of another large mountain.

# The dish is made up of many small mirrors, but while the mirrors themselves are roughly in the shape of a parabolic reflector dish, each individual mirror seems to be pointing in slightly the wrong direction. If the dish is meant to focus light, all it's doing right now is sending it in a vague direction.

# This system must be what provides the energy for the lava! If you focus the reflector dish, maybe you can go where it's pointing and use the light to fix the lava production.

# Upon closer inspection, the individual mirrors each appear to be connected via an elaborate system of ropes and pulleys to a large metal platform below the dish. The platform is covered in large rocks of various shapes. Depending on their position, the weight of the rocks deforms the platform, and the shape of the platform controls which ropes move and ultimately the focus of the dish.

# In short: if you move the rocks, you can focus the dish. The platform even has a control panel on the side that lets you tilt it in one of four directions! The rounded rocks (O) will roll when the platform is tilted, while the cube-shaped rocks (#) will stay in place. You note the positions of all of the empty spaces (.) and rocks (your puzzle input). For example:

# O....#....
# O.OO#....#
# .....##...
# OO.#O....O
# .O.....O#.
# O.#..O.#.#
# ..O..#O..O
# .......O..
# #....###..
# #OO..#....
# Start by tilting the lever so all of the rocks will slide north as far as they will go:

# OOOO.#.O..
# OO..#....#
# OO..O##..O
# O..#.OO...
# ........#.
# ..#....#.#
# ..O..#.O.O
# ..O.......
# #....###..
# #....#....
# You notice that the support beams along the north side of the platform are damaged; to ensure the platform doesn't collapse, you should calculate the total load on the north support beams.

# The amount of load caused by a single rounded rock (O) is equal to the number of rows from the rock to the south edge of the platform, including the row the rock is on. (Cube-shaped rocks (#) don't contribute to load.) So, the amount of load caused by each rock in each row is as follows:

# OOOO.#.O.. 10
# OO..#....#  9
# OO..O##..O  8
# O..#.OO...  7
# ........#.  6
# ..#....#.#  5
# ..O..#.O.O  4
# ..O.......  3
# #....###..  2
# #....#....  1
# The total load is the sum of the load caused by all of the rounded rocks. In this example, the total load is 136.

# Tilt the platform so that the rounded rocks all roll north. Afterward, what is the total load on the north support beams?

# Your puzzle answer was 109596.

# --- Part Two ---
# The parabolic reflector dish deforms, but not in a way that focuses the beam. To do that, you'll need to move the rocks to the edges of the platform. Fortunately, a button on the side of the control panel labeled "spin cycle" attempts to do just that!

# Each cycle tilts the platform four times so that the rounded rocks roll north, then west, then south, then east. After each tilt, the rounded rocks roll as far as they can before the platform tilts in the next direction. After one cycle, the platform will have finished rolling the rounded rocks in those four directions in that order.

# Here's what happens in the example above after each of the first few cycles:

# After 1 cycle:
# .....#....
# ....#...O#
# ...OO##...
# .OO#......
# .....OOO#.
# .O#...O#.#
# ....O#....
# ......OOOO
# #...O###..
# #..OO#....

# After 2 cycles:
# .....#....
# ....#...O#
# .....##...
# ..O#......
# .....OOO#.
# .O#...O#.#
# ....O#...O
# .......OOO
# #..OO###..
# #.OOO#...O

# After 3 cycles:
# .....#....
# ....#...O#
# .....##...
# ..O#......
# .....OOO#.
# .O#...O#.#
# ....O#...O
# .......OOO
# #...O###.O
# #.OOO#...O
# This process should work if you leave it running long enough, but you're still worried about the north support beams. To make sure they'll survive for a while, you need to calculate the total load on the north support beams after 1000000000 cycles.

# In the above example, after 1000000000 cycles, the total load on the north support beams is 64.

# Run the spin cycle for 1000000000 cycles. Afterward, what is the total load on the north support beams?

# Your puzzle answer was 96105.

f = open('inputs/doc_day_14.txt')
lines = f.read()
lines = lines.splitlines()

def get_cols(lines):
    cols = []
    x = 0
    while x<(len(lines[0])):
        col = ''
        for row in lines:
            col = col + row[x]
        cols.append(col)
        x+=1
    return cols

def collapse(cols):
    new_cols = []
    for col in cols:
        dots = ''
        rocks = ''
        new_col = ''
        for c in col:
            if c == '.':
                dots = dots + c
            if c == 'O':
                rocks = rocks + c
            if c == '#':
                new_col = new_col+rocks+dots+'#'
                dots = ''
                rocks = ''

        if len(dots) >0 or len(rocks)> 0:
            new_col = new_col+rocks+dots
        new_cols.append(new_col)
    return new_cols

def get_weight(cols):
    y = 0
    sum = 0
    while y<=(len(cols[0])-1):
        count = 0
        for col in cols:
            if(col[y] == 'O'):
                count += 1
        count = count*(len(cols)-y)
        sum = sum + count
        y+=1
    return sum

def rotate(cols):
    new_cols = []
    i = 0
    while i <= len(cols[0])-1:
        new_col = ''
        for col in cols:
            new_col = new_col+col[i]
        new_cols.insert(0, new_col)
        i+=1
    return new_cols

def infere_weight_at_cycle(cols, cicles):
    reps = set()
    loop = []
    candidate_start = []
    w = 0
    ready_to_infer = False
    
    north = cols
    i = 1
    while i<= cicles:
        north_collapsed = collapse(north)
        west = rotate(north_collapsed) 
        west_collapsed = collapse(west)
        south = rotate(west_collapsed)
        south_collapsed = collapse(south)
        east = rotate(south_collapsed)
        east_collapsed = collapse(east)
        north = rotate(east_collapsed)
        w = get_weight(north)
        if w in reps:
            if(len(loop) == 0):
                candidate_start = [i, north]
            else:
                if north == candidate_start[1]:
                    ready_to_infer = True
                    break
            loop.append([i, w])
        else:
            reps.add(w)
            loop = []
        i+=1
        
    if ready_to_infer == False:
        return w
    else:
        w = loop[(cicles-(candidate_start[0]))%len(loop)][1]
        return w


################################################### EXECUTION

cols = get_cols(lines)
collapsed_north = collapse(cols)
weight = get_weight(collapsed_north)
print(f'Solution 1: {weight}')

weight_after = infere_weight_at_cycle(cols, 1000000000)
print(f'Solution 2: {weight_after}')

# Solution 1: 109596
# Solution 2: 96105