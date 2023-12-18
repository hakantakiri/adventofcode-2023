f = open('inputs/doc_day_17.txt')
lines = f.read()
lines = lines.splitlines()
text = ''.join(lines)

WIDTH = len(lines[0])
print(f'width is: {WIDTH}')
HEIGHT = len(lines)

def fill_min(txt):
    def lan(c):
        if c.isdigit():
            return c
        else:
            return 'A'
        
    # m = min(txt, key=lan)
    m = max(txt )
    print(f'min is {m}')
    txt = txt.replace(m, ' ')
    return txt

def print_state(txt, w):
    row = ''
    for i, c in enumerate(txt):
        row = row + c
        if ((i+1)%w == 0):
            row += '\n'
    return row

start = [0,0]
end = [HEIGHT-1, WIDTH-1]
n_start = int(lines[start[0]][start[1]])
n_end = int(lines[end[0]][end[1]])
n_min = max([n_start, n_end])
n_max = int(max(text))

j = n_max
while j> n_min:
    text = fill_min(text)
    j-=1

print(print_state(text, WIDTH))

