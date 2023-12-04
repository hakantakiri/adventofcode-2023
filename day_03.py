# PART 1

f = open('inputs/doc_day_03.txt')
lines = f.read()
lines = lines.splitlines()
# print(lines)

sp = []
numbers = []
for i, line  in enumerate(lines):
    # Getting positions
    capturing = False
    new_num = ''
    start = 0
    end = 0
    for j,c in enumerate(line) :
        if('0123456789'.find(c)>=0):
            # It is a number
            # print(f'Number {c} found at [{i}, {j}]')
            if(capturing == False) : # The first digit
                new_num = '' + c
                # print(f'Started capturing with digit {new_num}')
                capturing = True
                start = j
                end = j
            else :
                new_num = new_num + '' + c
                end = j
        else:
            if(capturing == True):
                # print(f'Number adding: {[new_num, [i, [start, end]]]}')
                numbers.append([int(new_num), [i, [start, end]]])
                new_num = ''
                capturing = False
                start = 0
                end = 0
        
        if(j == (len(line)-1) and capturing == True):
            numbers.append([int(new_num), [i, [start, end]]])

        if ('0123456789.'.find(c)<0):
            # It is a symbol
            # print(f'Symbol {c} found at [{i}, {j}]')
            sp.append([i, j, c])

# print(f'Symbol positions: {sp}')
# print(f'Numbers: {numbers}')


valid_numbers  = []
for n in numbers:
    number = n[0]
    valid = False
    r_i_prev = n[1][0] - 1
    if(r_i_prev < 0):
        r_i_prev  = 0
    
    r_i_sig = n[1][0] + 1
    if(r_i_sig > 140-1):
        r_i_sig  = n[1][0]
    
    r_j_prev = n[1][1][0] - 1 
    if(r_j_prev < 0):
        r_j_prev = 0
    
    r_j_sig = n[1][1][1] + 1
    if(r_j_sig > len(lines)-1):
        r_j_sig  = n[1][1][1]

    for s in sp:
        if ((s[0]>= r_i_prev and s[0]<= r_i_sig ) and ( s[1]>= r_j_prev and s[1]<= r_j_sig)):
            valid = True        
    if valid:
        valid_numbers.append(n)

# print(f'Valid numbers: {valid_numbers}, and its sum is: {sum([n[0] for n in valid_numbers])}')
print(f'Solution 1: {sum([n[0] for n in valid_numbers])}')
# Solution 1: 549908

# Part 2:
gears = []
for s in sp:
    if( s[2] == '*'):
        r_i_prev = s[0] - 1
        if(r_i_prev < 0):
            r_i_prev  = 0
        
        r_i_sig = s[0] + 1
        if(r_i_sig > 140-1):
            r_i_sig  = s[0]
        
        r_j_prev = s[1] - 1 
        if(r_j_prev < 0):
            r_j_prev = 0
        
        r_j_sig = s[1] + 1
        if(r_j_sig > len(lines)-1):
            r_j_sig  = s[1] 
        
        ns = []
        for n in numbers:
            ni = n[1][0]
            nj1 = n[1][1][0]
            nj2 = n[1][1][1]
            if( ni>= r_i_prev and ni<= r_i_sig) and ((nj2>=r_j_prev and nj2 <= r_j_sig) or (nj1>=r_j_prev and nj1 <= r_j_sig) ):
                ns.append(n)

        gears.append([s, ns])

# print(f'Gears: {gears}')

# gear= [[sx, sy, s], [...[n, [nx, [ny_start, ny_end]]]]]
valid_gears = []
for gear in gears:
    if len(gear[1]) == 2 :
        valid_gears.append(gear)
# print(f'Valid gears: {valid_gears}')

solution = 0
for g in valid_gears:
    m = 1
    for n in g[1]:
       m = m *n[0]
    solution = solution +m

print(f'Solution 2: {solution}')
# Solution 1: 549908
# Solution 2: 81166799