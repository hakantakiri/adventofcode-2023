import sys
import copy
f = open('inputs/doc_day_18.txt')
lines = f.read()
lines = lines.splitlines()
# print(lines)

def get_plan(lines):
    plan = []
    for line in lines:
        dir = line.split(' ')[0]
        n = int(line.split(' ')[1])
        color = line.split(' ')[2]
        plan.append([dir, n, color])
    return plan

def get_edge(plan):
    current = [0,0]
    edge = []
    edge.append(current)
    for ins in plan:
        i = 1
        while i <=  ins[1]:
            dir = ins[0]
            if dir == 'R':
                current = [current[0], current[1]+1]
                edge.append(current)
            if dir == 'L':
                current = [current[0], current[1]-1]
                edge.append(current)
            if dir == 'U':
                current = [current[0]-1, current[1]]
                edge.append(current)
            if dir == 'D':
                current = [current[0]+1, current[1]]
                edge.append(current)
            i += 1
    min_y = min(edge, key=lambda x: x[0])[0]
    min_x = min(edge, key=lambda x: x[1])[1]
    max_y = max(edge, key=lambda x: x[0])[0]
    max_x = max(edge, key=lambda x: x[1])[1]
    # print(f' Min y {min_y}')
    # print(f' Min x {min_x}')
    # print(f' start is [{abs(min_y)}, {abs(min_x)}]')

    adjusted_edge = []
    for p in edge:
        adjusted_edge.append([p[0]+abs(min_y), p[1]+abs(min_x)])
    return [adjusted_edge, abs(min_y) +max_y + 1, abs(min_x) +max_x + 1]

# def capacity(edge, height, width):
#     if edge[0] == edge[-1]:
#         edge = edge[0:-1]
#     inside = []
#     y = 0
#     while y <= height -1:
#         x = 0
#         while x <= width - 1:
#             # print(f'Verifying position: [{y}, {x}]')
#             if [y,x] not in edge:
#                 count = 0
#                 k = 0
#                 while k < x:
#                     if [y, k] in edge:
#                         if( k >=1):
#                             if [y, k-1] in edge:
#                                 # verifing
                                 
#                             else:
#                                 count +=1
#                     k+=1

#                 if count%2 == 1:
#                     print(f' - inside: [{y}, {x}]')
#                     inside.append([y, x])
#             x+=1
#         y+=1
#         print('\n')
#     print('inside')
#     print(inside)
#     print(f'pool are {len(inside) + len(edge)}')
#     print(f'outside are {(y*x) - (len(inside) + len(edge))}')
def next (current, edge, empties, h, w, border):
    y = current[0]
    x = current[1]
    print(f'- recursion: analyzing current {current}', end = '\r')
    # print(f'- border length is {len(border)}', end = '\r')
    print(f'- empties length is {len(empties)}', end = '\r')
    empties.append(current)
    if current in border:
        border.remove(current)
    if x+1 < w and ( [y, x+1] not in edge) and ([y, x+1] not in empties) :
        next([y, x+1], edge, empties, h, w, border)
    if x-1 >= 0 and ([y, x-1] not in edge) and ([y, x-1] not in empties) :
        next([y, x-1], edge, empties, h, w, border)
    if y+1 < h and ([y+1, x] not in edge) and ([y+1, x] not in empties) :
        next([y+1, x], edge, empties, h, w, border)
    if y-1 >= 0 and ([y-1, x] not in edge) and ([y-1, x] not in empties) :
        next([y-1, x], edge, empties, h, w, border)
    return

def get_outside(edge, height, width):
    # print(f'Getting outside for height {height}, and width {width}')
    y_min = 0
    y_max = height-1
    x_min = 0
    x_max = width-1
    empties = []
    border = []
    
    for y in range(y_min, y_max):
        for x in [x_min, x_max]:
            if([y, x] not in border) and ([y,x] not in edge):
                border.append([y,x])
    for x in range(x_min, x_max):
        for y in [y_min, y_max]:
            if([y, x] not in border) and ([y,x] not in edge):
                border.append([y,x])

    # print('border')
    # print(border)
    
    i = 0
    while i < len(border)-1:
        if(border[i] not in edge) and (border[i] not in empties):
            next(border[i], edge, empties, height, width, border)
        else:
            i+=1
    

    # for y in range(y_min, y_max):
    #     for x in [x_min, x_max]:
    #         if([y, x] not in edge) and ([y,x] not in empties):
    # for x in range(x_min, x_max):
    #     for y in [y_min, y_max]:
    #             next([y,x], edge, empties, height, width)
    #         if([y, x] not in edge) and ([y,x] not in empties):
    #             next([y,x], edge, empties, height, width)
    return empties

def get_area(coords):
    clean_coords = []
    # if coords[0] == coords[-1]:
    #     clean_coords = coords[:-1]
    # else:
    clean_coords = copy.deepcopy(coords)
    
    part1 = 0
    part2 = 0
    # print(f' working with: {clean_coords}')
    for i, coord in enumerate(clean_coords):

        if i< len(clean_coords)-1:
            # print(f'adding to part 1: {coord[0]}*{clean_coords[i+1][1]}')
            part1 = part1 + (4*coord[0]*clean_coords[i+1][1])
        if i>0:
            # print(f'adding to part 2: {coord[1]}*{clean_coords[i-1][0]}')
            part2 = part2 + (4*coord[0]*clean_coords[i-1][1])

    print(f'part1: {part1}')
    print(f'part2: {part2}')
    return 0.5*abs(part2-part1)

def reverse_array(array):
    new_array= []
    j= len(array)-1
    while j>=0:
        new_array.append(array[j])
        j-=1
    return new_array

########################### EXECUTION
sys.setrecursionlimit(100000)

plan = get_plan(lines)
# print(plan)

[edge, height, width] = get_edge(plan)
print(f'height: {height}, width: {width}, edge: {len(edge)-1}')
# print(len(edge)-1)

print(get_area([[4,0], [0,0], [0,4], [4,4], [4,0]]))
print(get_area([[4,4], [0,4], [0,0], [4,0], [4,4]]))
print(get_area([[0,0], [0,4], [4,4], [4,0], [0,0]]))
print(get_area(edge))

print(get_area(reverse_array(edge)))

# empties = []
# y = 0
# while y < height -1:
#     x = 0
#     while x< width -1:
#         print(f'- Working with [{y}, {x}]', end = '\r')
#         if [y, x] not in edge:
#             empties.append([y,x])
#         x+=1
#     y+=1
# print(f'Finished for y:{y} and x: {x}')
# print(f'Empties len: {len(empties)}')

# empties = get_outside(edge, height, width)
# print(f'Solution 1: {(height*width)-len(empties)}')