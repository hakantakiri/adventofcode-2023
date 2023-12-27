# --- Day 23: A Long Walk ---
# The Elves resume water filtering operations! Clean water starts flowing over the edge of Island Island.

# They offer to help you go over the edge of Island Island, too! Just hold on tight to one end of this impossibly long rope and they'll lower you down a safe distance from the massive waterfall you just created.

# As you finally reach Snow Island, you see that the water isn't really reaching the ground: it's being absorbed by the air itself. It looks like you'll finally have a little downtime while the moisture builds up to snow-producing levels. Snow Island is pretty scenic, even without any snow; why not take a walk?

# There's a map of nearby hiking trails (your puzzle input) that indicates paths (.), forest (#), and steep slopes (^, >, v, and <).

# For example:

# #.#####################
# #.......#########...###
# #######.#########.#.###
# ###.....#.>.>.###.#.###
# ###v#####.#v#.###.#.###
# ###.>...#.#.#.....#...#
# ###v###.#.#.#########.#
# ###...#.#.#.......#...#
# #####.#.#.#######.#.###
# #.....#.#.#.......#...#
# #.#####.#.#.#########v#
# #.#...#...#...###...>.#
# #.#.#v#######v###.###v#
# #...#.>.#...>.>.#.###.#
# #####v#.#.###v#.#.###.#
# #.....#...#...#.#.#...#
# #.#########.###.#.#.###
# #...###...#...#...#.###
# ###.###.#.###v#####v###
# #...#...#.#.>.>.#.>.###
# #.###.###.#.###.#.#v###
# #.....###...###...#...#
# #####################.#
# You're currently on the single path tile in the top row; your goal is to reach the single path tile in the bottom row. Because of all the mist from the waterfall, the slopes are probably quite icy; if you step onto a slope tile, your next step must be downhill (in the direction the arrow is pointing). To make sure you have the most scenic hike possible, never step onto the same tile twice. What is the longest hike you can take?

# In the example above, the longest hike you can take is marked with O, and your starting position is marked S:

# #S#####################
# #OOOOOOO#########...###
# #######O#########.#.###
# ###OOOOO#OOO>.###.#.###
# ###O#####O#O#.###.#.###
# ###OOOOO#O#O#.....#...#
# ###v###O#O#O#########.#
# ###...#O#O#OOOOOOO#...#
# #####.#O#O#######O#.###
# #.....#O#O#OOOOOOO#...#
# #.#####O#O#O#########v#
# #.#...#OOO#OOO###OOOOO#
# #.#.#v#######O###O###O#
# #...#.>.#...>OOO#O###O#
# #####v#.#.###v#O#O###O#
# #.....#...#...#O#O#OOO#
# #.#########.###O#O#O###
# #...###...#...#OOO#O###
# ###.###.#.###v#####O###
# #...#...#.#.>.>.#.>O###
# #.###.###.#.###.#.#O###
# #.....###...###...#OOO#
# #####################O#
# This hike contains 94 steps. (The other possible hikes you could have taken were 90, 86, 82, 82, and 74 steps long.)

# Find the longest hike you can take through the hiking trails listed on your map. How many steps long is the longest hike?

# Your puzzle answer was 2222.

# --- Part Two ---
# As you reach the trailhead, you realize that the ground isn't as slippery as you expected; you'll have no problem climbing up the steep slopes.

# Now, treat all slopes as if they were normal paths (.). You still want to make sure you have the most scenic hike possible, so continue to ensure that you never step onto the same tile twice. What is the longest hike you can take?

# In the example above, this increases the longest hike to 154 steps:

# #S#####################
# #OOOOOOO#########OOO###
# #######O#########O#O###
# ###OOOOO#.>OOO###O#O###
# ###O#####.#O#O###O#O###
# ###O>...#.#O#OOOOO#OOO#
# ###O###.#.#O#########O#
# ###OOO#.#.#OOOOOOO#OOO#
# #####O#.#.#######O#O###
# #OOOOO#.#.#OOOOOOO#OOO#
# #O#####.#.#O#########O#
# #O#OOO#...#OOO###...>O#
# #O#O#O#######O###.###O#
# #OOO#O>.#...>O>.#.###O#
# #####O#.#.###O#.#.###O#
# #OOOOO#...#OOO#.#.#OOO#
# #O#########O###.#.#O###
# #OOO###OOO#OOO#...#O###
# ###O###O#O###O#####O###
# #OOO#OOO#O#OOO>.#.>O###
# #O###O###O#O###.#.#O###
# #OOOOO###OOO###...#OOO#
# #####################O#
# Find the longest hike you can take through the surprisingly dry hiking trails listed on your map. How many steps long is the longest hike?

# Your puzzle answer was 6590.

import copy
f = open('inputs/doc_day_23.txt')
lines = f.read()
lines = lines.splitlines()

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
        of_seen = copy.deepcopy(current['seen'])
        for next in ([[y-1, x], [y+1,x] ,[y,x-1], [y,x+1]]):
            if next[0]>=0 and next[1]>=0 and next[0]<=len(grid)-1 and next[1]<=len(grid[0])-1:
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
    while len(currents)>0 :
        currents = fill_next(grid, currents, distances)
        print(f'- Concurrent paths {len(currents)}', end = '\r')
    return distances

######################################################### PART 2

def f_node(node):
    return ','.join([str(n) for n in node])

def get_nodes(grid):
    nodes = []
    for y,row in enumerate(grid):
        for x, c in enumerate(row):
            if c != '#':
                count = 0
                for side in ([[y-1,x], [y+1,x] ,[y,x-1] ,[y,x+1]]):
                    p = side[0]
                    q = side[1]
                    if(p>=0 and q>=0 and p<=len(grid)-1 and q<= len(grid[0])-1):
                        if('.<>^v'.find(grid[p][q])>=0):
                            count+=1
                if count >2:
                    nodes.append([y, x])
    return nodes

def get_nodes_distances(start, end, nodes, grid):
    nodes.insert(0, start)
    nodes.append(end)
    dists = []
    for ia, n in enumerate(nodes):
        for ib in range(ia+1, len(nodes)):
            a = nodes[ia]
            b = nodes[ib]
            dis = distance_between_nodes(grid, a, b)
            if dis >0:
                dists.append([a, b, dis])
    conections = {}
    for dist in dists:
        a = dist[0]
        b = dist[1]
        name_a = ','.join([str(n) for n in a])
        name_b = ','.join([str(n) for n in b])
        if name_a in conections:
            conections[name_a]['cons'].append(b)
        else:
            conections[name_a] = {
                'pos': a,
                'cons': [b]
            }
        if name_b in conections:
            conections[name_b]['cons'].append(a)
        else:
            conections[name_b] = {
                'pos': b,
                'cons': [a]
            }
    return (conections, dists)


def distance_between_nodes(grid, a, b):
    seen = [a]
    currents = [{
        'pos': a,
        'dis': 0
    }]
    currents = search_next(currents, seen, grid, True)
    while len(currents) > 0:
        currents = search_next(currents, seen, grid, False)
        for current in currents:
            if current['pos'] == b:
                return current['dis']
    return -1

def search_next(currents, seen, grid, start):
    new_current = []
    for current in currents:
        y = current['pos'][0]
        x = current['pos'][1]
        dis = current['dis']
        ram = 0
        candidate = []
        for next in ([[y-1,x], [y+1,x], [y,x-1], [y,x+1]]):
            if next[0]>=0 and next[0]<=len(grid)-1 and next[1]>=0 and next[1]<=len(grid[0])-1:
                if '>v<^.'.find(grid[next[0]][next[1]])>=0 and next not in seen:
                    ram = ram+1
                    seen.append(next)
                    candidate.append({'pos':next, 'dis': dis+1})
        if start == True or ram<=1 :
            new_current = new_current+candidate
    return new_current



def find_routes(connections, start, end):
    currents = [{
        'node': f_node(start),
        'seen': [start]
    }]
    routes = []
    while len(currents)>0:
        currents = find_next_node(currents, connections)
        print(f' - Working on {len(currents)} current paths \t\t', end='\r')
        # print(f' - Working on {len(currents)} current paths')
        for current in currents:
            # print(current)
            s = current['seen']
            if end in s:
                routes.append(s)
    
    # print('routes')
    # print(routes)
    return routes

def find_next_node(currents, connections ):
    new_currents = []
    for current in currents:
        name = current['node']
        seen = current['seen']
        # print(f'name: {name}')
        # print(f'seen: {seen}')
        cons = connections[name]['cons']
        for con in cons:
            if con not in seen:
                new_seen = copy.deepcopy(seen)
                new_seen.append(con)
                new_currents.append({
                    'node': f_node(con),
                    'seen': new_seen
                })
    return new_currents

def get_dist(a,b, dists):
    for d in dists:
        if (d[0] == a and d[1] == b) or (d[0] == b and d[1] == a):
            return d[2]
def get_length_of_routes(routes, dists):
    distances = []
    for route in routes:
        # print(f'Validating route: {route}')
        dis = 0
        for i, r in enumerate(route):
            if(i+1 <= len(route)-1):
                next_r = route[i+1]
                d = get_dist(r, next_r, dists)
                dis = dis + d
        distances.append(dis)
    return distances

############################## Execution

grid = get_grid(lines)
(start, end) = get_start_and_end(grid)
print('Wait for solution 1, it might take some minutes ...')
distances  = fill_distances(grid, start, end)
print('\n')
print(f"Solution 1: {distances[end[0]][end[1]]}")
print('\n\n\n')
print('Wait for solution 2, it might take some hours ...')
nodes = get_nodes(grid)
(connections, dists) = get_nodes_distances(start, end, nodes, grid)
routes = find_routes(connections, start, end)
print('\n')
node_distances = get_length_of_routes(routes, dists)
print(f'Solution 2: {max(node_distances)}')

# Solution 1: 2222
# Solution 2: 6590