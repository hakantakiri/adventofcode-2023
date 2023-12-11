# --- Day 10: Pipe Maze ---
# You use the hang glider to ride the hot air from Desert Island all the way up to the floating metal island. This island is surprisingly cold and there definitely aren't any thermals to glide on, so you leave your hang glider behind.

# You wander around for a while, but you don't find any people or animals. However, you do occasionally find signposts labeled "Hot Springs" pointing in a seemingly consistent direction; maybe you can find someone at the hot springs and ask them where the desert-machine parts are made.

# The landscape here is alien; even the flowers and trees are made of metal. As you stop to admire some metal grass, you notice something metallic scurry away in your peripheral vision and jump into a big pipe! It didn't look like any animal you've ever seen; if you want a better look, you'll need to get ahead of it.

# Scanning the area, you discover that the entire field you're standing on is densely packed with pipes; it was hard to tell at first because they're the same metallic silver color as the "ground". You make a quick sketch of all of the surface pipes you can see (your puzzle input).

# The pipes are arranged in a two-dimensional grid of tiles:

# | is a vertical pipe connecting north and south.
# - is a horizontal pipe connecting east and west.
# L is a 90-degree bend connecting north and east.
# J is a 90-degree bend connecting north and west.
# 7 is a 90-degree bend connecting south and west.
# F is a 90-degree bend connecting south and east.
# . is ground; there is no pipe in this tile.
# S is the starting position of the animal; there is a pipe on this tile, but your sketch doesn't show what shape the pipe has.
# Based on the acoustics of the animal's scurrying, you're confident the pipe that contains the animal is one large, continuous loop.

# For example, here is a square loop of pipe:

# .....
# .F-7.
# .|.|.
# .L-J.
# .....
# If the animal had entered this loop in the northwest corner, the sketch would instead look like this:

# .....
# .S-7.
# .|.|.
# .L-J.
# .....
# In the above diagram, the S tile is still a 90-degree F bend: you can tell because of how the adjacent pipes connect to it.

# Unfortunately, there are also many pipes that aren't connected to the loop! This sketch shows the same loop as above:

# -L|F7
# 7S-7|
# L|7||
# -L-J|
# L|-JF
# In the above diagram, you can still figure out which pipes form the main loop: they're the ones connected to S, pipes those pipes connect to, pipes those pipes connect to, and so on. Every pipe in the main loop connects to its two neighbors (including S, which will have exactly two pipes connecting to it, and which is assumed to connect back to those two pipes).

# Here is a sketch that contains a slightly more complex main loop:

# ..F7.
# .FJ|.
# SJ.L7
# |F--J
# LJ...
# Here's the same example sketch with the extra, non-main-loop pipe tiles also shown:

# 7-F7-
# .FJ|7
# SJLL7
# |F--J
# LJ.LJ
# If you want to get out ahead of the animal, you should find the tile in the loop that is farthest from the starting position. Because the animal is in the pipe, it doesn't make sense to measure this by direct distance. Instead, you need to find the tile that would take the longest number of steps along the loop to reach from the starting point - regardless of which way around the loop the animal went.

# In the first example with the square loop:

# .....
# .S-7.
# .|.|.
# .L-J.
# .....
# You can count the distance each tile in the loop is from the starting point like this:

# .....
# .012.
# .1.3.
# .234.
# .....
# In this example, the farthest point from the start is 4 steps away.

# Here's the more complex loop again:

# ..F7.
# .FJ|.
# SJ.L7
# |F--J
# LJ...
# Here are the distances for each tile on that loop:

# ..45.
# .236.
# 01.78
# 14567
# 23...
# Find the single giant loop starting at S. How many steps along the loop does it take to get from the starting position to the point farthest from the starting position?

# Your puzzle answer was 7173.

# --- Part Two ---
# You quickly reach the farthest point of the loop, but the animal never emerges. Maybe its nest is within the area enclosed by the loop?

# To determine whether it's even worth taking the time to search for such a nest, you should calculate how many tiles are contained within the loop. For example:

# ...........
# .S-------7.
# .|F-----7|.
# .||.....||.
# .||.....||.
# .|L-7.F-J|.
# .|..|.|..|.
# .L--J.L--J.
# ...........
# The above loop encloses merely four tiles - the two pairs of . in the southwest and southeast (marked I below). The middle . tiles (marked O below) are not in the loop. Here is the same loop again with those regions marked:

# ...........
# .S-------7.
# .|F-----7|.
# .||OOOOO||.
# .||OOOOO||.
# .|L-7OF-J|.
# .|II|O|II|.
# .L--JOL--J.
# .....O.....
# In fact, there doesn't even need to be a full tile path to the outside for tiles to count as outside the loop - squeezing between pipes is also allowed! Here, I is still within the loop and O is still outside the loop:

# ..........
# .S------7.
# .|F----7|.
# .||OOOO||.
# .||OOOO||.
# .|L-7F-J|.
# .|II||II|.
# .L--JL--J.
# ..........
# In both of the above examples, 4 tiles are enclosed by the loop.

# Here's a larger example:

# .F----7F7F7F7F-7....
# .|F--7||||||||FJ....
# .||.FJ||||||||L7....
# FJL7L7LJLJ||LJ.L-7..
# L--J.L7...LJS7F-7L7.
# ....F-J..F7FJ|L7L7L7
# ....L7.F7||L7|.L7L7|
# .....|FJLJ|FJ|F7|.LJ
# ....FJL-7.||.||||...
# ....L---J.LJ.LJLJ...
# The above sketch has many random bits of ground, some of which are in the loop (I) and some of which are outside it (O):

# OF----7F7F7F7F-7OOOO
# O|F--7||||||||FJOOOO
# O||OFJ||||||||L7OOOO
# FJL7L7LJLJ||LJIL-7OO
# L--JOL7IIILJS7F-7L7O
# OOOOF-JIIF7FJ|L7L7L7
# OOOOL7IF7||L7|IL7L7|
# OOOOO|FJLJ|FJ|F7|OLJ
# OOOOFJL-7O||O||||OOO
# OOOOL---JOLJOLJLJOOO
# In this larger example, 8 tiles are enclosed by the loop.

# Any tile that isn't part of the main loop can count as being enclosed by the loop. Here's another example with many bits of junk pipe lying around that aren't connected to the main loop at all:

# FF7FSF7F7F7F7F7F---7
# L|LJ||||||||||||F--J
# FL-7LJLJ||||||LJL-77
# F--JF--7||LJLJ7F7FJ-
# L---JF-JLJ.||-FJLJJ7
# |F|F-JF---7F7-L7L|7|
# |FFJF7L7F-JF7|JL---7
# 7-L-JL7||F7|L7F-7F7|
# L.L7LFJ|||||FJL7||LJ
# L7JLJL-JLJLJL--JLJ.L
# Here are just the tiles that are enclosed by the loop marked with I:

# FF7FSF7F7F7F7F7F---7
# L|LJ||||||||||||F--J
# FL-7LJLJ||||||LJL-77
# F--JF--7||LJLJIF7FJ-
# L---JF-JLJIIIIFJLJJ7
# |F|F-JF---7IIIL7L|7|
# |FFJF7L7F-JF7IIL---7
# 7-L-JL7||F7|L7F-7F7|
# L.L7LFJ|||||FJL7||LJ
# L7JLJL-JLJLJL--JLJ.L
# In this last example, 10 tiles are enclosed by the loop.

# Figure out whether you have time to search for the nest by calculating the area within the loop. How many tiles are enclosed by the loop?

# Your puzzle answer was 291.

import math
import copy

f = open('inputs/doc_day_10.txt')
lines = f.read()
lines = lines.splitlines()

def get_s_idx(lines):
    for y, line in enumerate(lines):
        if(line.find('S')>=0):
            return [y, line.index('S')]
        
def find_start(s, lines):
    y = s[0]
    x = s[1]
    if( '|F7'.find(lines[y-1][x]) >= 0 ):
        return [y-1, x]
    if( '|JL'.find(lines[y+1][x]) >= 0 ):
        return [y+1, x]
    if( '-J7'.find(lines[y][x+1]) >= 0 ):
        return [y, x+1]
    if( '-FL'.find(lines[y][x-1]) >= 0 ):
        return [y, x-1]

def find_next(current, prev, lines):
    y = current[0]
    x = current[1]
    y_prev = prev[0]
    x_prev = prev[1]

    if lines[y][x] == '-':
        if x_prev < x:
            return [y, x+1]
        else :
            return [y, x-1]
    
    if lines[y][x] == '|':
        if y_prev > y:
            return [y-1, x]
        else :
            return [y+1, x]

    if lines[y][x] == 'L':
        if (y_prev == y):
            return [y-1, x]
        else:
            return [y, x+1]

    if lines[y][x] == 'J':
        if x_prev == x:
            return [y, x-1]
        else:
            return [y-1 , x]

    if lines[y][x] == '7':
        if x_prev == x:
            return [y, x-1]
        else:
            return [y+1, x]

    if lines[y][x] == 'F':
        if x_prev == x:
            return [y, x +1]
        else:
            return [y+1, x]
    
    print(f'Error: current char: {lines[y][x]}, at position: {current},')
    print(f'Error: prev char: {lines[y_prev][x_prev]}, at position: {prev}')
    raise Exception('Cant find next, current character is')
    

    # if lines[y, x] == '.':
    #     return [ , ]

    # if lines[y, x] == 'S':
    #     return [ , ]
        
def calculate_loop(s, lines):
    start = find_start(s, lines)
    current = start
    prev = s
    completed_loop = False
    steps = 1
    loop = [s, start]
    while completed_loop == False:
        next = find_next(current, prev, lines)
        steps = steps + 1 
        if lines[next[0]][next[1]] == 'S':
            completed_loop = True
        else:
            loop.append(next)
            prev = current
            current = next
    
    # print(f'FINISH: Steps to loop {steps}')
    return loop

## For part 2

def get_cleaned_lines(loop, lines):
    new_lines = copy.deepcopy(lines)

    c = loop[0]
    b = loop[len(loop)-1]
    a = loop[1]
    n,s,e,w = False, False, False, False
    if (b[0] == c[0] and b[1] == c[1] + 1) or (a[0] == c[0] and a[1] == c[1] + 1):
        e = True
    if (b[0] == c[0] - 1 and b[1] == c[1]) or (a[0] == c[0] - 1 and a[1] == c[1]):
        n = True
    if (b[0] == c[0] and b[1] == c[1] - 1) or (a[0] == c[0] and a[1] == c[1] - 1):
        w = True
    if (b[0] == c[0] + 1 and b[1] == c[1]) or (a[0] == c[0] + 1 and a[1] == c[1]):
        s = True
    

    if(n and e):
        new_lines[c[0]] = new_lines[c[0]][:c[1]] + "L" + new_lines[c[0]][c[1]+1:]
    if(w and n):
        new_lines[c[0]] = new_lines[c[0]][:c[1]] + "J" + new_lines[c[0]][c[1]+1:]
    if(w and s):
        new_lines[c[0]] = new_lines[c[0]][:c[1]] + "7" + new_lines[c[0]][c[1]+1:]
    if(s and e):
        new_lines[c[0]] = new_lines[c[0]][:c[1]] + "F" + new_lines[c[0]][c[1]+1:]
    return new_lines

def inside_loop_area(position, loop, new_lines):
    # FJ : +1
    # L7 : +1
    # FSJ : +1
    # L$7 : +1
 
    # |:
    # S: +1
    # |

    # LJ : 0
    # F7 : 0
    # LSJ : 0
    # FS7 : 0
    prev = ''
    sum = 0

    y = position[0]
    x = 0

    while x<position[1]:
        char = new_lines[y][x]
        # print(f'- INSIDE LOOP: Analysis for char: {char} at position [{y}, {x}]')
        if [y,x] in loop: # in loop
            if char== '|':
                sum = sum+1
            if('J7'.find(char)>=0): 
                if char == 'J' and prev == 'F':
                    sum = sum + 1
                    prev = char
                if char == '7' and prev == 'L':
                    sum = sum + 1
                    prev = char
            
            if 'FL'.find(char) >= 0:
                    prev = char
        x = x+1

    if sum%2 == 1:
        return True
    else:
        return False



def count_inner_tiles(loop, lines):
    y_min = math.inf
    y_max = (-1) * math.inf
    x_min = math.inf
    x_max = (-1) * math.inf
    for l in loop:
        if l[0]< y_min:
            y_min = l[0]
        if l[0]> y_max:
            y_max = l[0]
        
        if l[1]< x_min:
            x_min = l[1]
        if l[1]> x_max:
            x_max = l[1]
    
    # print(f'min y and min x: [{y_min}, {x_min}]')
    # print(f'max y and max x: [{y_max}, {x_max}]')
    x = x_min
    y = y_min
    sum = 0
    while y <= y_max:
        while x <= x_max:
            # print(f'INNER: for [y,x] [{y}, {x}]')
            if [y, x] not in loop:
                # print('INNER: --- Not in loop')
                inside = inside_loop_area([y,x], loop, lines)
                # print(f'-- Is inside: {inside}')
                if inside:
                    sum = sum +1
            x = x + 1
        x = x_min
        y = y +1

    return sum
######## ######## ######## ######## ######## ######## Execution


# print(f'Lines: {lines}')
s_position = get_s_idx(lines)
# print(f'S: {s}')
loop = calculate_loop(s_position, lines)
print(f'Solution 1: {int(len(loop)/2)}')
# print(f'Loop:')
# print(loop)
cleaned_lines = get_cleaned_lines(loop, lines)
print('Wait for solution 2, it will take a while ...')
print(f'Solution 2: {count_inner_tiles(loop, cleaned_lines)}')

# Solution 1: 7173
# Solution 2: 291