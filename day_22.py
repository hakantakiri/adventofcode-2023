import copy
f = open('inputs/doc_day_22.txt')
lines = f.read()
lines = lines.splitlines()
# print(lines)

def get_bricks(lines):
    return [ [[int(n) for n in line.split('~')[0].split(',')], [ int(n) for n in line.split('~')[1].split(',')]] for line in lines ]

<<<<<<< HEAD
def order_bricks_z(bricks):
    new = copy.deepcopy(bricks)
    new.sort(key=lambda b: min(b[0][2], b[1][2]))
    return new

# def get_direction(bricks):
#     for  brick in bricks:
#         straight = 0
#         if brick[1][0]!=brick[0][0]:
#             straight+=1
#         if brick[1][1]!=brick[0][1]:
#             straight+=1
#         if brick[1][2]!=brick[0][2]:
#             straight+=1
        
#         if(straight ==0):
#             print(brick)
        

# def get_floating(bricks):
#     floating = []
#     for b in bricks:
#         belows =  [x for x in bricks if (min(b[0][2], b[1][2]) == max(x[0][2], x[1][2]) + 1)]
#         if len(belows) == 0:
#             floating.append(b)
#         else:
#             intercepts = False
#             for cand in belows:
#                 if b[0][2] == b[1][2]: # line
#                     if cand[0][2] != cand[1][2]: # dot
#                         if (b[0][0] <= cand[0][0] and cand[0][0] <= b[1][0]) and (b[0][1] <= cand[0][1] and cand[0][1] <= b[1][1]):
#                             intercepts = True
#                     elif (min(b[0][0],b[1][0])<= cand[0][0] and cand[0][0] <= max(b[0][0],b[1][0])) or (min(b[0][1],b[1][1])<= cand[0][1] and cand[0][1] <= max(b[0][1],b[1][1])):
#                         intercepts = True
#                     else:
#                         continue
#                 else: # dot
#                     if cand[0][2] != cand[1][2]: # dot
#                         if b[0][0] == cand[0][0] and cand[0][1] == b[0][1]:
#                             intercepts = True
#                     elif (min(b[0][0],b[1][0])<= cand[0][0] and cand[0][0] <= max(b[0][0],b[1][0])) or (min(b[0][1],b[1][1])<= cand[0][1] and cand[0][1] <= max(b[0][1],b[1][1])):
#                         intercepts = True
#                     else:
#                         continue
#                 if intercepts == False:
#                     floating.append(b)
#     print('Floating')
#     print(floating)


def get_cubes_for_brick(b):
    if b[0][0] != b[1][0]: # straight in X
        return [ [x, b[0][1], b[0][2]] for x in range(b[0][0], b[1][0]+1)]
    elif b[0][1] != b[1][1]: # straight in Y
        return [ [b[0][0], y,  b[0][2]] for y in range(b[0][1], b[1][1]+1)]
    elif b[0][2] != b[1][2]: # straight in Z
        return [ [b[0][0], b[0][1], z] for z in range(b[0][2], b[1][2]+1)]
    else:
        print([b[0]])
        return [b[0]]

def get_all_cubes(bricks):
    cubes = []
    for b in bricks:
        cubes.append(get_cubes_for_brick(b))
    return cubes

def get_map_of_cubes(bricks_cubes):
    cube_map = {}
    for b, cubes in enumerate(bricks_cubes):
        for cube in cubes:
            cube_map[tuple(cube)] = b

    return cube_map

def coll(bricks_cubes):
    cube_map = get_map_of_cubes(bricks_cubes)  
    curr_z = 2
    max_z = max([cube[2] for cube in cube_map])
    supports = []
    while curr_z <= max_z:
        print(f'Working at z lvl: {curr_z}')
        # print('cube_map')
        # print(cube_map)
        for cube in cube_map:
            if cube in cube_map and cube[2] == curr_z:
                # print(f'cube: {cube}')
                # print(f'{cube_map[cube]}')
                cube_id = cube_map[cube]
                min_z = bricks_cubes[cube_id][0][2]
                if min_z == curr_z:
                    valid = True
                    while min_z-1 > 0 and valid == True:
                        candidates_cubes = [[x,y,z-1] for [x, y, z] in bricks_cubes[cube_id]]
                        valid = True
                        for c_cube in candidates_cubes:
                            if not (tuple(c_cube) not in cube_map or (tuple(c_cube) in cube_map and cube_map[tuple(c_cube)]== cube_id)):
                                valid = False
                                if cube_map[tuple(c_cube)]!=cube_id:
                                    print(f'{cube_map[tuple(c_cube)]} supports {cube_id}')
                                    if [cube_map[tuple(c_cube)], cube_id] not in supports:
                                        supports.append([cube_map[tuple(c_cube)], cube_id])
                                
                        if valid:
                            # print('- is valid, must reduce its z lvl')
                            # print(f'- new candiates_cubes: {candidates_cubes}')
                            # print(f'- replacing old cubes: { bricks_cubes[cube_id]}')
                            
                            # for cube in bricks_cubes[cube_id]:
                            #     cube_map[tuple(cube)] = -10
                            
                            bricks_cubes[cube_id] = candidates_cubes

                            # for cube in candidates_cubes:
                            #     cube_map[tuple(cube)] = cube_id
                            
                            cube_map = get_map_of_cubes(bricks_cubes)


                            # print('- new cube_map')
                            # print(cube_map)
                            min_z = bricks_cubes[cube_id][0][2]
                            if min_z == 1:
                                supports.append([-1, cube_id])

        curr_z+=1
    
    map_sup = {}
    for sup in supports:
        if sup[0] not in map_sup:
            map_sup[sup[0]] = [sup[1]]
        else:
            map_sup[sup[0]].append(sup[1])
    print('map sup')
    print(map_sup)

    can_delete = []
    for brick in map_sup:
        valid = False
        for next in map_sup:
            if brick!=next:
                if set(map_sup[brick]).issubset(set(map_sup[next])):
                    valid = True
                    break
        if valid:
            can_delete.append(brick)

    for brick in map_sup:
        for upper in map_sup[brick]:
            if upper not in map_sup and upper not in can_delete:
                can_delete.append(upper)


    print('can delete')
    print(can_delete)
    print(len(can_delete))

def collapse(bricks_cubes, cube_map):
    supports = []
    for i, cubes in enumerate(bricks_cubes):
        c_cubes = copy.deepcopy(cubes)
        origin_brick = cube_map[tuple(cubes[0])]
        min_z = min([cube[2] for cube in c_cubes])
        collision = False
        while min_z > 1 and collision == False:
            t_cubes = [[x, y, z-1] for [x, y, z] in c_cubes]
            for [x, y, p] in t_cubes:
                if (x,y,p) not in cube_map or \
                    ( (x,y,p) in cube_map and cube_map[(x,y,p)] == origin_brick):
                    # collision = False
                    continue
                else:
                    collision = True
                    print(f'{cube_map[(x,y,p)]} collisions with {origin_brick}' )
                    supports.append([cube_map[(x,y,p)], origin_brick])
                    # continue
            min_z = min([cube[2] for cube in t_cubes]) 
            # if min_z == 1:
            #     supports.append([-1, origin_brick])
            #     collision = True
            if not collision:
                print('Not a collision')
                for cube in c_cubes:
                    del cube_map[tuple(cube)]
                for cube in t_cubes:
                    cube_map[tuple(cube)] = origin_brick
                c_cubes = t_cubes
        min_z =  min([cube[2] for cube in c_cubes])
        if min_z == 1:
            supports.append([-1, origin_brick])
        bricks_cubes[i] = c_cubes
    return supports

def get_sup_map(supports):
    sup_map = {}
    for sup in supports:
        if sup[0] not in sup_map:
            sup_map[sup[0]]  = [sup[1]]
        else:
            if sup[1] not in sup_map[sup[0]]:
                sup_map[sup[0]].append(sup[1])
    for sup in supports:
        if sup[1] not in sup_map:
            sup_map[sup[1]] = []
    return sup_map

def find_disintigrable(sup_map):
    disintigrable = []
    for s in sup_map:
        if s != -1:
            if len(sup_map[s])>0:
                for n in sup_map:
                    if s!=n and len(sup_map[n])>0 and n!=-1:
                        if set(sup_map[s]).issubset(set(sup_map[n])):
                            disintigrable.append(s)
                            break
            elif len(sup_map[s])==0:
                if sup_map[s] not in disintigrable:
                    disintigrable.append(s)

    

    return disintigrable


def print_projection(bricks_cubes, axis):
    new_map = get_map_of_cubes(bricks_cubes)
    min_z = 0
    max_z = max([z for cube in bricks_cubes for [x,y,z] in cube])
    print(f'- print projection')
    print(f'- min_z = {min_z}, max_z = {max_z}')
    # if axis == 'x':
    #     min_y = 0
    #     max_y = max([y for x,y,z in [cubes for cubes in bricks_cubes]])
    #     for z in range(min_z, max_z+1):
    #         line = []
    #         for y in range(min_y, max_y+1):
    #             print()
                
    

        
######################### EXECUTION

bricks = get_bricks(lines)
# print(bricks)
# get_direction(bricks)
bricks = order_bricks_z(bricks)
# print(bricks)
bricks_cubes = get_all_cubes(bricks)
# print('cubes')
# print(bricks_cubes)
# print(bricks_cubes)
# coll(bricks_cubes)










cube_map = get_map_of_cubes(bricks_cubes)
# # print(cube_map)
supports = collapse(bricks_cubes, cube_map)
# # print('collapsed')
print(bricks_cubes)
# print('supports')
# print(supports)
# # print(cube_map)
sup_map = get_sup_map(supports)
# print('sup map')
# print(sup_map)
print('len sup map')
print(len(sup_map))
dis = find_disintigrable(sup_map)
print('disintigrable')
# print(dis)
# print(list(set(dis)))
print(f'Solution 1: {len(dis)}')
print(f'Solution 1: {len(list(set(dis)))}')
# # floating = get_floating(bricks)

print_projection(bricks_cubes, 'x')
=======

def order_bricks_z(bricks):
    new = copy.deepcopy(bricks)
    new.sort(key=lambda x: min(x[0][2], x[1][2]))
    return new

def get_floating(bricks):
    floating = []
    for b in bricks:
        belows =  [x for x in bricks if (min(b[0][2], b[1][2]) == max(x[0][2], x[1][2]) + 1)]
        if len(belows) == 0:
            floating.append(b)
        else:
            intercepts = False
            for cand in belows:
                if b[0][2] == b[1][2]: # line
                    if cand[0][2] != cand[1][2]: # dot
                        if (b[0][0] <= cand[0][0] and cand[0][0] <= b[1][0]) and (b[0][1] <= cand[0][1] and cand[0][1] <= b[1][1]):
                            intercepts = True
                    elif (min(b[0][0],b[1][0])<= cand[0][0] and cand[0][0] <= max(b[0][0],b[1][0])) or (min(b[0][1],b[1][1])<= cand[0][1] and cand[0][1] <= max(b[0][1],b[1][1])):
                        intercepts = True
                    else:
                        continue
                else: # dot
                    if cand[0][2] != cand[1][2]: # dot
                        if b[0][0] == cand[0][0] and cand[0][1] == b[0][1]:
                            intercepts = True
                    elif (min(b[0][0],b[1][0])<= cand[0][0] and cand[0][0] <= max(b[0][0],b[1][0])) or (min(b[0][1],b[1][1])<= cand[0][1] and cand[0][1] <= max(b[0][1],b[1][1])):
                        intercepts = True
                    else:
                        continue
                if intercepts == False:
                    floating.append(b)
    print('Floating')
    print(floating)
            
######################### EXECUTION

bricks = get_bricks(lines)
bricks = order_bricks_z(bricks)
floating = get_floating(bricks)
# print(bricks)

print('Diagonals in z')
# for b in bricks:
#     if b[0][2] != b[1][2]:
#         if b[0][0] != b[1][0] or b[0][1] != b[1][1]:
#             print(b)
# for b in bricks:
#     if b[0][0] != b[1][0] and b[0][1] != b[1][1]:
#         print(b)

# for b in bricks:
#     if b[0][0] != b[1][0]:
#         print(f'Length for b {b} in x: is {abs(b[1][0]-b[0][0])}')
#     if b[0][1] != b[1][1]:
#         print(f'Length for b {b} in y: is {abs(b[1][1]-b[0][1])}')
#     if b[0][2] != b[1][2]:
#         print(f'Length for b {b} in z: is {abs(b[1][2]-b[0][2])}')
>>>>>>> e49f7ae607f1c03cfddb864ecf172580f9f2d7ff
