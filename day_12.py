import copy
import time
f = open('inputs/doc_day_12.txt')
lines = f.read()
lines = lines.splitlines()

def get_rows(lines):
    rows = []
    for line in lines:
        failed = line.split(' ')[0]
        groups = [int(n) for n in line.split(' ')[1].split(',')]
        rows.append([failed, groups])

    for row in rows:
        new_fail = []
        prev = ''
        for c in row[0]:
            if(c == '.' and prev != '.'):
                new_fail.append(c)
            elif(c != '.'):
                new_fail.append(c)
            prev = c
        row[0] = ''.join(new_fail)
    return rows

def get_mod_rows(lines):
    rows = []
    for line in lines:
        failed = '?'+line.split(' ')[0]
        groups = [int(n) for n in line.split(' ')[1].split(',')]
        rows.append([failed, groups])

    for row in rows:
        new_fail = []
        prev = ''
        for c in row[0]:
            if(c == '.' and prev != '.'):
                new_fail.append(c)
            elif(c != '.'):
                new_fail.append(c)
            prev = c
        row[0] = ''.join(new_fail)
    return rows


def get_rows_2(lines):
    rows = []
    for line in lines:
        failed = line.split(' ')[0]+'?'\
            +line.split(' ')[0]+'?'\
                +line.split(' ')[0]+'?'\
                    +line.split(' ')[0]+'?'\
                        +line.split(' ')[0]
        groups = [int(n) for n in line.split(' ')[1].split(',')]\
            + [int(n) for n in line.split(' ')[1].split(',')]\
                +[int(n) for n in line.split(' ')[1].split(',')]\
                    +[int(n) for n in line.split(' ')[1].split(',')]\
                        +[int(n) for n in line.split(' ')[1].split(',')]
        rows.append([failed, groups])

    for row in rows:
        new_fail = []
        prev = ''
        for c in row[0]:
            if(c == '.' and prev != '.'):
                new_fail.append(c)
            elif(c != '.'):
                new_fail.append(c)
            prev = c
        row[0] = ''.join(new_fail)
    return rows

def part1( rows):
    possibles = []
    for r in rows:
        counter = [0]
        calc(r[0], r[1], counter)
        possibles.append(counter[0])
    return possibles
        

def calculate_arrangement(row, rows_fixed):
    fails = row[0].count('?')
    # fail_len = len(row[0])
    # correct_len = sum(row[1])+len(row[1])-1
    left = sum(row[1])-row[0].count('#')
    # print(f'{i+1}: Fails: {fails}, left:{left}, fail_len:{fail_len}, correct_len:{correct_len}')
    possibles = generate_fill(left, fails)
    # print(f'For row: {row}')
    fills = []
    count = 0
    for fill in possibles:
        new_word = replace(row[0], fill)
        # print(f'- - Trying word {new_word}')
        if(is_valid(new_word, row[1])):
            count +=1
            fills.append(fill)
    # print(f'- Valid: {count}')
    permanents = get_permanents(fills)
    # print(f'- Permanents are: {permanents}')
    row_fixed = row_with_permanent(row[0], permanents)
    rows_fixed.append(row_fixed)
    return count



def get_permanents(fills):
    # print(f'- options: {len(fills)}')
    l = len(fills[0])
    ar = [0 for n in fills[0]]

    for fill in fills:
        for i in range(0, l):
            ar[i] +=( 1 if fill[i] == '#' else 0)
    # print(ar)
    for i, n in enumerate(ar):
        if n != 0 and n != len(fills):
            ar[i] = -1
        elif n == len(fills):
            ar[i] = 1
    
    return ar

def generate_fill(quant, length):
    base =  '0'*(length-quant)+'1'*quant
    limit = '1'*quant + '0'*(length-quant)
    fills = []
    for i in range(int(base, 2), int(limit, 2)+1):
        n = format(i, '0'+str(length)+'b')
        if n.count('1') == quant:
            fills.append(n.replace('1','#').replace('0','.'))
    return fills

def replace(text, fill):
    txt = list(text)
    while '?' in txt:
        i = txt.index('?')
        txt[i] = fill[0]
        fill = fill[1:]
    return ''.join(txt)

def row_with_permanent(text, permanent_fill):
    txt = list(text)
    while len(permanent_fill)>0:
        i = txt.index('?')
        if permanent_fill[0] != -1:
            txt[i] = '#' if permanent_fill[0] == 1 else '.'
        else:
            txt[i] = '&'
        permanent_fill = permanent_fill[1:]
    
    txt = ''.join(txt)
    return txt.replace('&', '?')

def is_valid(txt, group):
    # print(f'- Verifying {txt} to valid {group}')
    t_group = []
    count = 0
    for c in txt:
        if c =='#':
            count +=1
        elif c == '.' and count>0:
            t_group.append(count)
            count = 0
    if count>0 and txt[-1] == '#':
        t_group.append(count)
    
    return True if(t_group == group) else False

def get_groups_to_section(txt, group):
    t_group = []
    count = 0
    for c in txt:
        if c == '#':
            count +=1
        elif c == '.' and count>0:
            t_group.append(count)
            count = 0
    if count > 0 and txt[-1] == '#':
        t_group.append(count)

    if len(group)< len(t_group):
        return False
    
    j = len(t_group)-1
    for i in range(0, j+1):
        if( i < j):
            if( group[i] != t_group[i]):
                return False
        elif ( i == j):
            if (t_group[i] > group[i]):
                return False
    return True

def part2(rows, first_arrangements, fixed_rows):
    new_arrangements = []
    for i, row in enumerate(rows):
        print(f'- {i+1} for row: {row}, its fixed row: {fixed_rows[i]}, first arrangement: {first_arrangements[i]}')
        fixed = fixed_rows[i]
        if fixed[-1] == '.' :
        # if fixed[-1] == '.' and fixed[0] != '#':
            new_arrangements.append(first_arrangements[i]*\
                pow(calculate_arrangement(['?'+row[0], row[1]], []), 4))
        elif fixed[0] == '.':
        # elif fixed[0] == '.' and fixed[-1] != '#':
            new_arrangements.append(\
                pow(calculate_arrangement([row[0]+'?', row[1]], []), 4)\
                *first_arrangements[i])
        else:
            # new_arrangements.append(-1)
            # if row[0][0] == '?' and row[0][-1] == '?':
            #     new_arrangements.append(
            #         calculate_arrangement([(row[0]+'??')*4+ fixed, row[1]*5], [])
            #         )
            # else:
                n_count = [0]
                calc((fixed+'?')*4+ fixed, row[1]*5, n_count)
                new_arrangements.append(n_count[0])

        print(f'- - Past arren: {first_arrangements[i]}, new_arren: {new_arrangements[i]}')
            # if row[0] == '?':
            #     print("row[0] == '?'")
            #     new_arrangements.append(first_arrangements[i]*\
            #     pow(calculate_arrangement(['?'+row[0], row[1]], []), 4))
            # elif row[-1] == '?':
            #     print("row[-1] == '?'")
            #     new_arrangements.append(\
            #         pow(calculate_arrangement([row[0]+'?', row[1]], []), 4)\
            #         *first_arrangements[i])
            # else:
            #     new_arrangements.append(calculate_arrangement([(row[0]+'?')*4+ row[0], row[1]*5], []))
    return new_arrangements


def calc(text, group, counter ):
    s = sum(group)
    p = text.find('?')
    for c in (['#', '.']):
        new = text[0:p]+c+text[p+1:]
        if get_groups_to_section(new[0: p+1], group):
            left = new.count('?')
            sharp = new.count('#')
            if new.find('?')>=0 and sharp+left>=s :
                calc(new, group, counter)
            else: 
                if (is_valid(new, group)) and sharp == s:
                    counter[0] = counter[0] + 1


def part2_2( rows):
    possibles = []
    for r in rows:
        counter = [0]
        calc((r[0]+'?')*4+r[0], r[1]*5, counter)
        possibles.append(counter[0])
    return possibles



############ EXECUTION
rows = get_rows(lines)
print('Wait some seconds for solution 1')
possibles = part1(rows)

print(f'Solution 1: {possibles}')
print(f'Solution 1: {sum(possibles)}')
print('-------------')

possibles_2 = part2_2(rows)
print(f'Solution 2: {possibles_2}')
print(f'Solution 2: {sum(possibles_2)}')

start = time.time()
counter = [0]
# calc('?.?..?..?????', [1,4], counter) # 6
calc('?.?..?..???????.?..?..?????', [1,4,1,4], counter) # 78
# calc('?.?..?..???????.?..?..???????.?..?..?????', [1,4,1,4,1,4], counter) # 1038
# calc('?.?..?..???????.?..?..???????.?..?..???????.?..?..?????', [1,4,1,4,1,4,1,4], counter) 
# calc('?.?..?..???????.?..?..???????.?..?..???????.?..?..???????.?..?..?????', [1,4,1,4,1,4,1,4,1,4], counter)
# print('Counter')
print(counter)
end = time.time()
print(end-start)

print('-------------')

start = time.time()
# print(calculate_arrangement(['?.?..?..?????', [1,4]], []))
print(calculate_arrangement(['?.?..?..???????.?..?..?????', [1,4,1,4]], []))
# print(calculate_arrangement(['?.?..?..???????.?..?..???????.?..?..?????', [1,4,1,4,1,4]], []))
# print(calculate_arrangement(['?.?..?..???????.?..?..???????.?..?..???????.?..?..?????', [1,4,1,4,1,4,1,4]], []))
# print(calculate_arrangement(['?.?..?..???????.?..?..???????.?..?..???????.?..?..???????.?..?..?????', [1,4,1,4,1,4,1,4,1,4]], []))
end = time.time()
print(end-start)
