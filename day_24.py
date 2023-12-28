import math
f = open('inputs/doc_day_24.txt')
lines = f.read()
lines = lines.splitlines()
print(len(lines))

def get_hails(lines):
    hails = []
    for line in lines:
        pos = [int(n.strip()) for n in line.split('@')[0].split(',')]
        speed = [int(n.strip()) for n in line.split('@')[1].split(',')]
        a = (speed[1]/speed[0])
        hails.append({
            'pos': pos,
            'speed': speed,
            'a': a,
            'b' : pos[1] - a*pos[0]
            })
    return hails

def part1(hails, min, max):
    crossings = []
    for h, hail in enumerate(hails):
        for j in range(h+1, len(hails)):
            next = hails[j]
            if( hail['a'] == next['a'] ):
                continue
            else:
                x = (next['b'] - hail['b'])/(hail['a'] - next['a'])
                y = hail['a']*x + hail['b']
                if( x>= min and x<=max and y>=min and y<=max):
                    if (hail['speed'][0] <0 and x<hail['pos'][0]) or (hail['speed'][0] >=0 and x>=hail['pos'][0]):
                        if (next['speed'][0] <0 and x<next['pos'][0]) or (next['speed'][0] >=0 and x>=next['pos'][0]):
                            crossings.append([h, j, x, y])
    return crossings

def find_intercept(hails, n):
    founds = []
    for i, hail in enumerate(hails):
        # print(f'Comparing: {hail}')
        interceptions = []
        for j, next in enumerate(hails):
            # print(f'- - To {next}')
            if i != j and (hail['speed'][n]-next['speed'][n]) != 0:
                t = (next['pos'][n]-hail['pos'][n])/(hail['speed'][n]-next['speed'][n])
                x = (next['pos'][n]+next['speed'][n]*t)
                # print(f't: {t}')
                # print(f'x: {x}')
                if (t>0 and x>0):
                    interceptions.append({
                        'time': t,
                        'hail': next
                    })
        
        if len(interceptions) == len(hails)-1:
            interceptions = sorted( interceptions, key=(lambda x:x['time']))
            founds.append({
                'pos': hail['pos'][n] ,
                'speed': hail['speed'][n] ,
                "interceptions": interceptions
            })
    return founds

def part2(initial_direction):
    solutions = [None, None, None]
    lefts = []
    axis = 0
    if len(initial_direction[0]) > 0:
        lefts = [1,2]
    elif len(initial_direction[1]) > 0:
        lefts = [0,2]
        axis = 1
    elif len(initial_direction[2]) > 0:
        lefts = [0,1]
        axis = 2

    axisv = initial_direction[axis][0]
    pa = axisv['pos']
    sa = axisv['speed']
    solutions[axis] = {'p': pa, 's': sa}
    for l in lefts:
        interception = axisv['interceptions']
        t1 = interception[2]['time']
        t2 = interception[3]['time']
        v1 = interception[2]['hail']
        v2 = interception[3]['hail']
        #-----------
        p1 = v1['pos'][l]
        s1 = v1['speed'][l]
        p2 = v2['pos'][l]
        s2 = v2['speed'][l]

        sv = (p1+s1*t1-p2-s2*t2)/(t1-t2)
        pv = p1+s1*t1-sv*t1
        solutions[l] = {'p': pv, 's': sv}
    return solutions

min_r = 200000000000000 if len(lines) == 300 else 7
max_r = 400000000000000 if len(lines) == 300 else 27

hails = get_hails(lines)
crossings = part1(hails, min_r, max_r)
print(f'Solution 1: {len(crossings)}')

initial_direction = [find_intercept(hails, 0), find_intercept(hails, 1), find_intercept(hails, 2)]
print(initial_direction)
new_vector = part2(initial_direction)
print(f'Solution 2: {new_vector}')