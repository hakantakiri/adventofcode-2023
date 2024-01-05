f = open('inputs/doc_day_18.txt')
lines = f.read()
lines = lines.splitlines()

def generate_grid(height, width):
    grid = []
    for y in range(0, height):
        line = ['.' for x in range(0, width)]
        grid.append(line)
    return grid

def print_grid(grid, separator):
    for line in grid:
        print(separator.join([str(n) for n in line]))

def print_grid_with_path(grid, path, separator, indicator, replace=None):
    replace = True if replace == None or replace == True else False
    for y, line in enumerate(grid):
        formated_line = []
        for  x, c in enumerate(line):
            if(replace == False):
                formated_line.append(indicator+str(c) if [y,x] in path else str(c))
            else:
                formated_line.append(indicator if [y,x] in path else str(c))
        print(separator.join(formated_line))

def get_plan(lines):
    plan = []
    for line in lines:
        dir = line.split(' ')[0]
        n = int(line.split(' ')[1])
        color = line.split(' ')[2]
        plan.append([dir, n, color])
    return plan

def get_dig_path(plan):
    current = [0,0]
    holes = []
    holes.append(current)
    for ins in plan:
        i = 1
        while i <=  ins[1]:
            dir = ins[0]
            if dir == 'R':
                current = [current[0], current[1]+1]
                holes.append(current)
            if dir == 'L':
                current = [current[0], current[1]-1]
                holes.append(current)
            if dir == 'U':
                current = [current[0]-1, current[1]]
                holes.append(current)
            if dir == 'D':
                current = [current[0]+1, current[1]]
                holes.append(current)
            i += 1

    return normalize(holes)[0:-1]

def normalize(vertices):
    y_min = min(vertices, key = lambda v: v[0])[0]
    x_min = min(vertices, key = lambda v: v[1])[1]
    new_vertices = []
    for v in vertices:
        new_vertices.append([v[0]+abs(y_min), v[1]+abs(x_min)])
    return new_vertices

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
    return normalize(vertices)
 
def grid_size(vertices):
    y_min = min(vertices, key = lambda v: v[0])[0]
    x_min = min(vertices, key = lambda v: v[1])[1]
    y_max = max(vertices, key = lambda v: v[0])[0]
    x_max = max(vertices, key = lambda v: v[1])[1]
    return (y_max-y_min+1, x_max-x_min+1)

def get_edges(vertices):
    edges = []
    for i in range(0, len(vertices)-1):
        edges.append([vertices[i], vertices[i+1]])
    return edges

def in_polygon( edges, dig_path, height, width):
    insides = []
    for y in range(0, height):
        for x in range(0, width):
            if( [y, x] not in dig_path):
                cross = 0
                for e, edge in enumerate(edges):
                    if (edge[1][0] != edge[0][0]): # vertical line
                        if y>min(edge[0][0], edge[1][0]) and y<max(edge[0][0], edge[1][0]) and edge[0][1] < x:
                            cross += 1
                    elif (edge[1][0] == edge[0][0] and y == edge[0][0] and x> max(edge[0][1], edge[1][1])): 
                        lvl = edge[0][0]
                        lvl1 = min (edges[e-1][0][0], edges[e-1][1][0])
                        lvl2 = min (edges[e+1][0][0], edges[e+1][1][0])
                        if (lvl1 < lvl and lvl <= lvl2) or (lvl2 < lvl and lvl <= lvl1) :
                            cross+=1
                if cross%2==1:
                    insides.append([y,x])
    return insides
            
########################### EXECUTION

plan = get_plan(lines)
# print('plan')
# print(plan)

dig_path = get_dig_path(plan)
# print(f'Dig path: {len(dig_path)}')
# print(dig_path)

vertices = get_vertices(plan)
# print('Vertices')
# print(vertices)

(height, width) = grid_size(vertices)
# print(f'GRID SIZE: Height: {height}, width: {width}')

# print('Dig path:')
# print_grid_with_path(generate_grid(height, width), dig_path, ' ', '#')

edges = get_edges(vertices)
# print('Edges')
# print(edges)


print('Wait for solution 1, it may take some minutes ...')
insides = in_polygon(edges, dig_path, height, width)
# print(f'Insides: {len(insides)}')
# print(insides)
# print_grid_with_path(generate_grid(height, width), insides, ' ', '#')

# print('Lagoon:')
# print_grid_with_path(generate_grid(height, width), dig_path+insides, ' ', '#')

print(f'Solution 1: {len(insides)+ len(dig_path)} ')