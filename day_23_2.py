import time
import copy
f = open('inputs/doc_day_23.txt')
lines = f.read()
lines = lines.splitlines()
# print(lines)

def print_grid(ar):
    for row in ar:
        print(('\t').join([str(x) for x in row]))   

def f_node(node):
    return ','.join([str(n) for n in node])

def get_grid(lines):
    grid = []
    for line in lines:
        grid.append([c for c in line])
    return grid

def get_start_and_end(grid):
    start = [0, ''.join(grid[0]).find('.')]
    end = [len(grid)-1, ''.join(grid[len(grid)-1]).find('.')]
    return (start, end)

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




grid = get_grid(lines)
(start, end) = get_start_and_end(grid)
nodes = get_nodes(grid)
print(f'width: {len(grid[0])}, height: {len(grid)}')

(connections, dists) = get_nodes_distances(start, end, nodes, grid)
# print(f'Found {len(connections)} connections')
# for con in connections:
#     print(con)
# print(connections)
routes = find_routes(connections, start, end)
print('\n')
# print(f'Found {len(routes)} routes')
# print(routes)

distances = get_length_of_routes(routes, dists)
print('- Distances:')
print(distances)
print(f'Solution 2: {max(distances)}')



                    