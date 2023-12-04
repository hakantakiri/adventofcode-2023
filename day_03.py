# --- Day 3: Gear Ratios ---
# You and the Elf eventually reach a gondola lift station; he says the gondola lift will take you up to the water source, but this is as far as he can bring you. You go inside.

# It doesn't take long to find the gondolas, but there seems to be a problem: they're not moving.

# "Aaah!"

# You turn around to see a slightly-greasy Elf with a wrench and a look of surprise. "Sorry, I wasn't expecting anyone! The gondola lift isn't working right now; it'll still be a while before I can fix it." You offer to help.

# The engineer explains that an engine part seems to be missing from the engine, but nobody can figure out which one. If you can add up all the part numbers in the engine schematic, it should be easy to work out which part is missing.

# The engine schematic (your puzzle input) consists of a visual representation of the engine. There are lots of numbers and symbols you don't really understand, but apparently any number adjacent to a symbol, even diagonally, is a "part number" and should be included in your sum. (Periods (.) do not count as a symbol.)

# Here is an example engine schematic:

# 467..114..
# ...*......
# ..35..633.
# ......#...
# 617*......
# .....+.58.
# ..592.....
# ......755.
# ...$.*....
# .664.598..
# In this schematic, two numbers are not part numbers because they are not adjacent to a symbol: 114 (top right) and 58 (middle right). Every other number is adjacent to a symbol and so is a part number; their sum is 4361.

# Of course, the actual engine schematic is much larger. What is the sum of all of the part numbers in the engine schematic?

# Your puzzle answer was 549908.

# --- Part Two ---
# The engineer finds the missing part and installs it in the engine! As the engine springs to life, you jump in the closest gondola, finally ready to ascend to the water source.

# You don't seem to be going very fast, though. Maybe something is still wrong? Fortunately, the gondola has a phone labeled "help", so you pick it up and the engineer answers.

# Before you can explain the situation, she suggests that you look out the window. There stands the engineer, holding a phone in one hand and waving with the other. You're going so slowly that you haven't even left the station. You exit the gondola.

# The missing part wasn't the only issue - one of the gears in the engine is wrong. A gear is any * symbol that is adjacent to exactly two part numbers. Its gear ratio is the result of multiplying those two numbers together.

# This time, you need to find the gear ratio of every gear and add them all up so that the engineer can figure out which gear needs to be replaced.

# Consider the same engine schematic again:

# 467..114..
# ...*......
# ..35..633.
# ......#...
# 617*......
# .....+.58.
# ..592.....
# ......755.
# ...$.*....
# .664.598..
# In this schematic, there are two gears. The first is in the top left; it has part numbers 467 and 35, so its gear ratio is 16345. The second gear is in the lower right; its gear ratio is 451490. (The * adjacent to 617 is not a gear because it is only adjacent to one part number.) Adding up all of the gear ratios produces 467835.

# What is the sum of all of the gear ratios in your engine schematic?

# Your puzzle answer was 81166799.

# Both parts of this puzzle are complete! They provide two gold stars: **
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