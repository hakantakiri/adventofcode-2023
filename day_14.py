import copy
f = open('inputs/doc_day_14.txt')
lines = f.read()
lines = lines.splitlines()

def get_cols(lines):
    cols = []
    x = 0
    while x<(len(lines[0])):
        col = ''
        for row in lines:
            col = col + row[x]
        cols.append(col)
        x+=1
    return cols

# def swap_chars(string, i, j):
#     return string[:i]+string[j]+string[i+1: j] + string[i]+ string[j+1:]

def collapse(cols):
    new_cols = []
    for col in cols:
        dots = ''
        rocks = ''
        new_col = ''
        for c in col:
            if c == '.':
                dots = dots + c
            if c == 'O':
                rocks = rocks + c
            if c == '#':
                new_col = new_col+rocks+dots+'#'
                dots = ''
                rocks = ''

        if len(dots) >0 or len(rocks)> 0:
            new_col = new_col+rocks+dots
        new_cols.append(new_col)
    return new_cols

def weight(cols):
    y = 0
    sum = 0
    while y<=(len(cols[0])-1):
        count = 0
        for col in cols:
            if(col[y] == 'O'):
                count += 1

        count = count*(len(cols)-y)
        sum = sum + count
        y+=1
    return sum


############### EXECUTION

cols = get_cols(lines)
print('cols')
print(cols)
new_cols = collapse(cols)

print('new_cols')
print(new_cols)

print('weight')
weight = weight(cols)
print(weight)