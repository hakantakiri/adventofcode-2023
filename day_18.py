# --- Day 18: Lavaduct Lagoon ---
# Thanks to your efforts, the machine parts factory is one of the first factories up and running since the lavafall came back. However, to catch up with the large backlog of parts requests, the factory will also need a large supply of lava for a while; the Elves have already started creating a large lagoon nearby for this purpose.

# However, they aren't sure the lagoon will be big enough; they've asked you to take a look at the dig plan (your puzzle input). For example:

# R 6 (#70c710)
# D 5 (#0dc571)
# L 2 (#5713f0)
# D 2 (#d2c081)
# R 2 (#59c680)
# D 2 (#411b91)
# L 5 (#8ceee2)
# U 2 (#caa173)
# L 1 (#1b58a2)
# U 2 (#caa171)
# R 2 (#7807d2)
# U 3 (#a77fa3)
# L 2 (#015232)
# U 2 (#7a21e3)
# The digger starts in a 1 meter cube hole in the ground. They then dig the specified number of meters up (U), down (D), left (L), or right (R), clearing full 1 meter cubes as they go. The directions are given as seen from above, so if "up" were north, then "right" would be east, and so on. Each trench is also listed with the color that the edge of the trench should be painted as an RGB hexadecimal color code.

# When viewed from above, the above example dig plan would result in the following loop of trench (#) having been dug out from otherwise ground-level terrain (.):

# #######
# #.....#
# ###...#
# ..#...#
# ..#...#
# ###.###
# #...#..
# ##..###
# .#....#
# .######
# At this point, the trench could contain 38 cubic meters of lava. However, this is just the edge of the lagoon; the next step is to dig out the interior so that it is one meter deep as well:

# #######
# #######
# #######
# ..#####
# ..#####
# #######
# #####..
# #######
# .######
# .######
# Now, the lagoon can contain a much more respectable 62 cubic meters of lava. While the interior is dug out, the edges are also painted according to the color codes in the dig plan.

# The Elves are concerned the lagoon won't be large enough; if they follow their dig plan, how many cubic meters of lava could it hold?

# Your puzzle answer was 49061.

# --- Part Two ---
# The Elves were right to be concerned; the planned lagoon would be much too small.

# After a few minutes, someone realizes what happened; someone swapped the color and instruction parameters when producing the dig plan. They don't have time to fix the bug; one of them asks if you can extract the correct instructions from the hexadecimal codes.

# Each hexadecimal code is six hexadecimal digits long. The first five hexadecimal digits encode the distance in meters as a five-digit hexadecimal number. The last hexadecimal digit encodes the direction to dig: 0 means R, 1 means D, 2 means L, and 3 means U.

# So, in the above example, the hexadecimal codes can be converted into the true instructions:

# #70c710 = R 461937
# #0dc571 = D 56407
# #5713f0 = R 356671
# #d2c081 = D 863240
# #59c680 = R 367720
# #411b91 = D 266681
# #8ceee2 = L 577262
# #caa173 = U 829975
# #1b58a2 = L 112010
# #caa171 = D 829975
# #7807d2 = L 491645
# #a77fa3 = U 686074
# #015232 = L 5411
# #7a21e3 = U 500254
# Digging out this loop and its interior produces a lagoon that can hold an impressive 952408144115 cubic meters of lava.

# Convert the hexadecimal color codes into the correct instructions; if the Elves follow this new dig plan, how many cubic meters of lava could the lagoon hold?

# Your puzzle answer was 92556825427032.

f = open('inputs/doc_day_18.txt')
lines = f.read()
lines = lines.splitlines()

#################################### PART 1 // OBSOLETE
# def get_dig_path(plan):
#     current = [0,0]
#     holes = []
#     holes.append(current)
#     for ins in plan:
#         i = 1
#         while i <=  ins[1]:
#             dir = ins[0]
#             if dir == 'R':
#                 current = [current[0], current[1]+1]
#                 holes.append(current)
#             if dir == 'L':
#                 current = [current[0], current[1]-1]
#                 holes.append(current)
#             if dir == 'U':
#                 current = [current[0]-1, current[1]]
#                 holes.append(current)
#             if dir == 'D':
#                 current = [current[0]+1, current[1]]
#                 holes.append(current)
#             i += 1

#     return normalize(holes)[0:-1]

# def normalize(vertices):
#     y_min = min(vertices, key = lambda v: v[0])[0]
#     x_min = min(vertices, key = lambda v: v[1])[1]
#     new_vertices = []
#     for v in vertices:
#         new_vertices.append([v[0]+abs(y_min), v[1]+abs(x_min)])
#     return new_vertices
 
# def grid_size(vertices):
#     y_min = min(vertices, key = lambda v: v[0])[0]
#     x_min = min(vertices, key = lambda v: v[1])[1]
#     y_max = max(vertices, key = lambda v: v[0])[0]
#     x_max = max(vertices, key = lambda v: v[1])[1]
#     return (y_max-y_min+1, x_max-x_min+1)

# def get_edges(vertices):
#     edges = []
#     for i in range(0, len(vertices)-1):
#         edges.append([vertices[i], vertices[i+1]])
#     return edges

# def in_polygon( edges, dig_path, height, width):
#     insides = []
#     for y in range(0, height):
#         for x in range(0, width):
#             if( [y, x] not in dig_path):
#                 cross = 0
#                 for e, edge in enumerate(edges):
#                     if (edge[1][0] != edge[0][0]): # vertical line
#                         if y>min(edge[0][0], edge[1][0]) and y<max(edge[0][0], edge[1][0]) and edge[0][1] < x:
#                             cross += 1
#                     elif (edge[1][0] == edge[0][0] and y == edge[0][0] and x> max(edge[0][1], edge[1][1])): 
#                         lvl = edge[0][0]
#                         lvl1 = min (edges[e-1][0][0], edges[e-1][1][0])
#                         lvl2 = min (edges[e+1][0][0], edges[e+1][1][0])
#                         if (lvl1 < lvl and lvl <= lvl2) or (lvl2 < lvl and lvl <= lvl1) :
#                             cross+=1
#                 if cross%2==1:
#                     insides.append([y,x])
#     return insides


################################ PART 1 & 2

def get_plan(lines):
    plan = []
    for line in lines:
        dir = line.split(' ')[0]
        n = int(line.split(' ')[1])
        color = line.split(' ')[2]
        plan.append([dir, n, color])
    return plan

def get_new_plan(plan):
    new_plan = []
    dir_dict = ['R', 'D', 'L', 'U']
    for line in plan:
        p = line[2]
        dir = dir_dict[int(p[7])]
        n = int(p[2: 7], 16)
        new_plan.append([dir, n, line[2]])
    return new_plan

def get_vertices(plan):
    current = [0, 0]
    vertices = [current]
    for ins in plan:
        if ins[0] == 'L':
            current = [current[0], current[1]-ins[1]]
        if ins[0] == 'R':
            current = [current[0], current[1]+ins[1]]
        if ins[0] == 'U':
            current = [current[0]-ins[1], current[1]]
        if ins[0] == 'D':
            current = [current[0]+ins[1], current[1]]
        vertices.append(current)
    return vertices

def get_area(plan): # Uses an adaptation for the formula to calculate the area of any polygon given its vertices
    vertices = get_vertices(plan)
    sides = 0
    for p in plan:
        sides += p[1]
    a = 0
    b = 0
    for i in range(0, len(vertices)-1):
        curr = vertices[i]
        next = vertices[i+1]
        a += curr[0]*next[1]
        b += next[0]*curr[1]
    area = int(abs(a-b)/2 + sides/2 + 1)
    return area

########################### EXECUTION

plan = get_plan(lines)
print(f'Solution 1: {get_area(plan)}')
new_plan = get_new_plan(plan)
print(f'Solution 2: {get_area(new_plan)}')

# Solution 1: 49061
# Solution 2: 92556825427032