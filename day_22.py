import copy
f = open('inputs/doc_day_22.txt')
lines = f.read()
lines = lines.splitlines()
# print(lines)

def get_bricks(lines):
    return [ [[int(n) for n in line.split('~')[0].split(',')], [ int(n) for n in line.split('~')[1].split(',')]] for line in lines ]


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