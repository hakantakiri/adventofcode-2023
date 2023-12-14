import math
f = open('inputs/doc_day_12.txt')
lines = f.read()
lines = lines.splitlines()
# print(lines)

def reduce_record(record):
    left_outer = True
    repeat = False
    new = ''
    for c in record:
        if '#?'.find(c) >= 0:
            new = new + c
            left_outer = False
            repeat = False
        if c == '.':
            if left_outer == False:
                if repeat == False:
                    new = new + c
                    repeat = True
    i = len(new) - 1
    if new[i] == '.':
        while i>=0:
            if new[i] == '.':
                new = new[:-1]
            else:
                return new
            i = i - 1
    else:
        return new

def get_rows (lines):
    rows = []   
    for i, line in enumerate(lines):
        rows.append([
            i, 
            line.split(' ')[0], 
            reduce_record(line.split(' ')[0]),
            [int(n) for n in line.split(' ')[1].split(',')]
        ])
    return rows


def validate(row, instruction):
    sep =list(filter(None, row.split('.'))) 
    if (len(sep) != len(instruction)):
        return False
    else:
        for i, ins in enumerate(instruction):
            if len(sep[i]) != ins:
                return False
        return True

def build_options(row):
    print(f'\nFor row: {row}')
    count = row[2].count('#')
    expected = sum(row[3])
    dif = expected-count
    indexes = []
    for i, c in enumerate(row[2]):
        if c == '?':
            indexes.append(i)
    min  = int(math.pow(2,dif)-1)
    max = 0
    j = 0
    k = dif
    while k>=1:
        max = max + int(math.pow(2, len(indexes) -1 +j))
        j = j-1
        k = k -1
    
    options = []
    i = min
    print(f'- Trying {max-min+1} options: {min} to {max}')
    while i<=max:
        base = ("{0:0"+str(len(indexes))+"b}").format(i)
        # if base.count('1') == dif:
        #     base = base.replace('0', '.')
        #     base = base.replace('1', '#')
        #     temp =row[2]
        #     for m, idx in enumerate(indexes):
        #         temp = temp[:idx] + base[m] + temp[idx+1:]
        #     if validate(temp, row[3]) == True:
        #         options.append(temp)
        i+=1
    print(f'- Options: {len(options)}: {options}')
    return options

############################## EXECUTION

rows = get_rows(lines)
print('Wait for solution 1, it will take a while ...')
options = []
for r in rows:
    options.append(len(build_options(r)))
print(f'\nSolution 1: {sum(options)}')

for r in rows:
    r[2] = reduce_record(r[1]+'?'+r[1]+'?'+r[1]+'?'+r[1]+'?'+r[1]) 
    r[3] = r[3]+r[3]+r[3]+r[3]+r[3]

# print('new rows')
# print(rows)
print('\n\nWait for solution 2, it will take a while ...')
for r in rows:
    options.append(len(build_options(r)))
print(f'\nSolution 2: {sum(options)}')