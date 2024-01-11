from functools import lru_cache

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

print(lines)

@lru_cache
def calc(record, groups):
    if not record:
        return 0
    if not groups:
        if '#' not in record:
            return 1
        else:
            return 0
        
    c = record[0]
    group = groups[0]
    out = 0

    def process_dot():
        # print(f'--- Jumping to next character {record}')
        return calc(record[1:], groups)
    
    def process_sharp():
        section = record[0:group]
        section = section.replace('?', '#')
        # print(f'-- verifying section: {section} to group {"#"*group}')
        
        if section == '#'*group:
            if len(groups) == 1 :
                return 1
            elif len(groups)>1 and len(record)>group and record[group] in '?.':
                return calc(record[group+1:], groups[1:])
            else:
                return 0
        else:
            return 0

    if( c == '.'):
        out += process_dot()
    elif (c == '#'):
        out += process_sharp()
    elif( c =='?'):
        out += process_sharp() + process_dot()

    # print(f'Obtained poss is: {out}')
    return out

def part_1(rows):
    sum = 0
    for r in rows:
        s=calc(r[0], tuple(r[1]))
        print(f'Processing row {r}, solution {s}')
        sum+=s
    return sum

def part_2(rows):
    sum = 0
    for r in rows:
        s=calc((r[0]+'?')*4+r[0], tuple(r[1]*5))
        # print(f'Processing row {r}, solution {s}')
        sum+=s
    return sum

rows = get_rows(lines)
print(f'Solution 1: {part_1(rows)}')
print(f'Solution 2: {part_2(rows)}')