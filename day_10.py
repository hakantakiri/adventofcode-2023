import math
f = open('inputs/doc_day_10.txt')
lines = f.read()
lines = lines.splitlines()

def get_s_idx(lines):
    for i, line in enumerate(lines):
        if(line.find('S')>=0):
            return [i, line.index('S')]
        
def find_start(s, lines):
    i = s[0]
    j = s[1]
    if( '|F7'.find(lines[i, j-1])>=0):
        return [i, j -1]
    if( '|JL'.finde(lines[i, j+1]) >= 0 ):
        return [i, j+1]
    if( '-J7'.finde(lines[i+1, j]) >= 0 ):
        return [i+1, j]
    if( '-FL'.finde(lines[i-1, j]) >= 0 ):
        return [i-1, j]

def find_next(current, prev, lines):
    i = current[0]
    j = current[1]
    i_prev = prev[0]
    j_prev = prev[1]

    if lines[i, j] == '-':
        if i_prev < i:
            return [i+1, j]
        else :
            return [i-1, j]

    if lines[i, j] == 'L':
        if (j_prev == j):
            

    if lines[i, j] == 'J':
        return [ , ]

    if lines[i, j] == '7':
        return [ , ]

    if lines[i, j] == 'F':
        return [ , ]

    if lines[i, j] == '.':
        return [ , ]

    if lines[i, j] == 'S':
        return [ , ]
        
def calucalte_loop(s, lines):
    i = 0
    j = 0
    start = find_start(s)
    for i, line in enumerate(lines):
        for j, c in enumerate(line):
            if c == '|':


            if c == '-':

            if c == 'L':

            if c == 'J':

            if c == '7':

            if c == 'F':

            if c == '.':

            if c == 'S':



######## Execution


s = get_s_idx(lines)
print(f'Lines: {lines}')
print(f'S: {s}')