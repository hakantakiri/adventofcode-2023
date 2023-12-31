# --- Day 11: Cosmic Expansion ---
# You continue following signs for "Hot Springs" and eventually come across an observatory. The Elf within turns out to be a researcher studying cosmic expansion using the giant telescope here.

# He doesn't know anything about the missing machine parts; he's only visiting for this research project. However, he confirms that the hot springs are the next-closest area likely to have people; he'll even take you straight there once he's done with today's observation analysis.

# Maybe you can help him with the analysis to speed things up?

# The researcher has collected a bunch of data and compiled the data into a single giant image (your puzzle input). The image includes empty space (.) and galaxies (#). For example:

# ...#......
# .......#..
# #.........
# ..........
# ......#...
# .#........
# .........#
# ..........
# .......#..
# #...#.....
# The researcher is trying to figure out the sum of the lengths of the shortest path between every pair of galaxies. However, there's a catch: the universe expanded in the time it took the light from those galaxies to reach the observatory.

# Due to something involving gravitational effects, only some space expands. In fact, the result is that any rows or columns that contain no galaxies should all actually be twice as big.

# In the above example, three columns and two rows contain no galaxies:

#    v  v  v
#  ...#......
#  .......#..
#  #.........
# >..........<
#  ......#...
#  .#........
#  .........#
# >..........<
#  .......#..
#  #...#.....
#    ^  ^  ^
# These rows and columns need to be twice as big; the result of cosmic expansion therefore looks like this:

# ....#........
# .........#...
# #............
# .............
# .............
# ........#....
# .#...........
# ............#
# .............
# .............
# .........#...
# #....#.......
# Equipped with this expanded universe, the shortest path between every pair of galaxies can be found. It can help to assign every galaxy a unique number:

# ....1........
# .........2...
# 3............
# .............
# .............
# ........4....
# .5...........
# ............6
# .............
# .............
# .........7...
# 8....9.......
# In these 9 galaxies, there are 36 pairs. Only count each pair once; order within the pair doesn't matter. For each pair, find any shortest path between the two galaxies using only steps that move up, down, left, or right exactly one . or # at a time. (The shortest path between two galaxies is allowed to pass through another galaxy.)

# For example, here is one of the shortest paths between galaxies 5 and 9:

# ....1........
# .........2...
# 3............
# .............
# .............
# ........4....
# .5...........
# .##.........6
# ..##.........
# ...##........
# ....##...7...
# 8....9.......
# This path has length 9 because it takes a minimum of nine steps to get from galaxy 5 to galaxy 9 (the eight locations marked # plus the step onto galaxy 9 itself). Here are some other example shortest path lengths:

# Between galaxy 1 and galaxy 7: 15
# Between galaxy 3 and galaxy 6: 17
# Between galaxy 8 and galaxy 9: 5
# In this example, after expanding the universe, the sum of the shortest path between all 36 pairs of galaxies is 374.

# Expand the universe, then find the length of the shortest path between every pair of galaxies. What is the sum of these lengths?

# Your puzzle answer was 9521550.

# --- Part Two ---
# The galaxies are much older (and thus much farther apart) than the researcher initially estimated.

# Now, instead of the expansion you did before, make each empty row or column one million times larger. That is, each empty row should be replaced with 1000000 empty rows, and each empty column should be replaced with 1000000 empty columns.

# (In the example above, if each empty row or column were merely 10 times larger, the sum of the shortest paths between every pair of galaxies would be 1030. If each empty row or column were merely 100 times larger, the sum of the shortest paths between every pair of galaxies would be 8410. However, your universe will need to expand far beyond these values.)

# Starting with the same initial image, expand the universe according to these new rules, then find the length of the shortest path between every pair of galaxies. What is the sum of these lengths?

# Your puzzle answer was 298932923702.

f = open('inputs/doc_day_11.txt')
lines = f.read()
lines = lines.splitlines()

def get_space(lines):
    space = []
    for l in lines:
        n = []
        for c in l:
            n.append(c)
        space.append(n)
    return space


def is_x_empty(space, x):
    for l in space:
        if l[x] == '#':
            return False
    return True

def is_y_empty(space, y):
    for c in space[y]:
        if c == '#':
            return False
    return True

def expand_space(space, times):
    q = times-1
    x_len = len(space[0])

    new_space = []
    finish_space = []

    x = 0
    x_empties = []
    while x<x_len :
        if is_x_empty(space, x):
            x_empties.append(x)
        x = x + 1 

    for y, line in enumerate(space):
        new_space.append(line)
        if is_y_empty(space, y):
            k = 1
            while k<=q:
                new_space.append(['.']*x_len)
                k=k+1

    for line in new_space:
        new_line = line
        j = 0
        for x in x_empties:
            new_line = new_line[:x+j] + ['.']*q+ new_line[x+j:]
            j= j+q
        finish_space.append(new_line)
    
    return finish_space

def find_galaxies(space):
    galaxies = []
    for y,line in enumerate(space):
        for x,c in enumerate(line):
            if c == '#':
                galaxies.append([y, x])
    return galaxies

def distances(galaxies):
    combinations = []
    distances = []
    for i, g in enumerate(galaxies):
        for j,f in enumerate(galaxies):
            if j>i:
                combinations.append([g, f])

    for gs in combinations:
        distances.append(abs(gs[0][0]-gs[1][0]) + abs(gs[0][1]- gs[1][1]))

    return distances

##################################################### EXECUTION

space = get_space(lines)

expanded = expand_space(space, 2)
galaxies = find_galaxies(expanded)
ds = distances(galaxies)
print(f'Solution 1: {sum(ds)}') # Done in 38m54s91

print('Wait for solution 2, it will take a while ...')
expanded2 = expand_space(space, 1000000)
galaxies2 = find_galaxies(expanded2)
ds2 = distances(galaxies2)
print(f'Solution 2: {sum(ds2)}') # Done in 15m39s59

# Solution 1: 9521550
# Solution 2: 298932923702