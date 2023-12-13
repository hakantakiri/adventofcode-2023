f = open('inputs/doc_day_12.txt')
lines = f.read()
lines = lines.splitlines()
print(lines)

def get_rows (lines):
    rows = []   
    for i, line in enumerate(lines):
        rows.append([i, line.split(' ')[0], [int(n) for n in line.split(' ')[1].split(',')]])
    return rows

def get_space(rows):

    for r in rows:

        count = 0
        for c in list(r[1]):
            # print(f'searching c: {c} row: {r[1]}')
            if '#?'.find(c) >= 0:
                count = count+1
                # print(f'- count is: {count}')
        # print(f'- count is: {count}')        
        r.append(count)

    return rows


############################## EXECUTION
rows = get_rows(lines)
print(rows)
print('Extended')
space = get_space(rows)
print(space)
for r in space:
    print(f'{len(r[1])}, {sum(r[2])+len(r[2])-1} | {r[3]}, {sum(r[2])}')
