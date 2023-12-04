# --- Day 1: Trebuchet?! ---
# Something is wrong with global snow production, and you've been selected to take a look. The Elves have even given you a map; on it, they've used stars to mark the top fifty locations that are likely to be having problems.

# You've been doing this long enough to know that to restore snow operations, you need to check all fifty stars by December 25th.

# Collect stars by solving puzzles. Two puzzles will be made available on each day in the Advent calendar; the second puzzle is unlocked when you complete the first. Each puzzle grants one star. Good luck!

# You try to ask why they can't just use a weather machine ("not powerful enough") and where they're even sending you ("the sky") and why your map looks mostly blank ("you sure ask a lot of questions") and hang on did you just say the sky ("of course, where do you think snow comes from") when you realize that the Elves are already loading you into a trebuchet ("please hold still, we need to strap you in").

# As they're making the final adjustments, they discover that their calibration document (your puzzle input) has been amended by a very young Elf who was apparently just excited to show off her art skills. Consequently, the Elves are having trouble reading the values on the document.

# The newly-improved calibration document consists of lines of text; each line originally contained a specific calibration value that the Elves now need to recover. On each line, the calibration value can be found by combining the first digit and the last digit (in that order) to form a single two-digit number.

# For example:

# 1abc2
# pqr3stu8vwx
# a1b2c3d4e5f
# treb7uchet
# In this example, the calibration values of these four lines are 12, 38, 15, and 77. Adding these together produces 142.

# Consider your entire calibration document. What is the sum of all of the calibration values?

# Your puzzle answer was 57346.

# --- Part Two ---
# Your calculation isn't quite right. It looks like some of the digits are actually spelled out with letters: one, two, three, four, five, six, seven, eight, and nine also count as valid "digits".

# Equipped with this new information, you now need to find the real first and last digit on each line. For example:

# two1nine
# eightwothree
# abcone2threexyz
# xtwone3four
# 4nineeightseven2
# zoneight234
# 7pqrstsixteen
# In this example, the calibration values are 29, 83, 13, 24, 42, 14, and 76. Adding these together produces 281.

# What is the sum of all of the calibration values?

# Your puzzle answer was 57345.

# Both parts of this puzzle are complete! They provide two gold stars: **


import math
f = open('inputs/doc_day_01.txt')
lines = f.read()
lines = lines.splitlines()
# print('original lines')
# print(lines)    
def get (l):
    i = 0
    j = len(l)-1
    first=0
    last=0
    gotf = False
    gotl = False

    while((gotf==False or gotl==False) and (i<len(l) and j>=0)) :
        if (l[i]>='0' and l[i] <='9') and gotf == False:
            first = l[i]
            gotf = True
        if (l[j]>='0' and l[j] <='9') and gotl == False:
            last = l[j]
            gotl = True
        
        if gotf and gotl:
            return first+''+last
        else:
            i=i+1
            j=j-1
        
solution = 0
for line in lines:
    n = get(line) if get(line) else 0
    solution = solution+int(n)
print(f'Solution part 1 is: {solution}')

comp = ['one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine']

def find_all(text: str, sub:str):
    resp = []
    i = 0
    while(i<(len(text) - len(sub) +1)):
        if((text[i:]).find(sub) == 0):
            resp.append(i)
        i=i+1
    return resp

def duplicate_to_number(l:str):
    new_line_start = l
    new_line_end = l
    start_index = math.inf
    end_index = -math.inf
    
    for i in range(0,9,1):
        f= find_all(l, comp[i])
        if(len(f)>0):
            if ( f[0] < start_index):
                start_index = f[0]
            if(  f[len(f)-1] > end_index):
                end_index = f[len(f)-1]

    # print(f'For line {l} start index is: {start_index} and end index is: {end_index}')
    for i in range(0,9,1):
        f = find_all(l, comp[i])
        if(len(f)>0):
            if(f[0]>=0 and f[0] == start_index):
                new_line_start = new_line_start.replace(comp[i], str(i+1))
            if( f[len(f)-1] >=0 and f[len(f)-1] == end_index):
                 new_line_end = new_line_end.replace(comp[i], str(i+1) )

    if(start_index > len(l)):
        new_line_start =  l
    
    if(end_index < 0):
        new_line_end = l

    # print(f'newline must be {new_line_start+new_line_end} and end line')
    return new_line_start+new_line_end



new_lines = []
for line in lines:
    new_lines.append(duplicate_to_number(line))
# print('new lines')
# print(new_lines)
solution2 = 0
for line in new_lines:
    n = get(line) if get(line) else 0
    # print(f'Obtained number is: {n}')
    solution2 = solution2+int(n)
print(f'Solution part 2 is: {solution2}')
# Solution part 1 is: 57346
# Solution part 2 is: 57345