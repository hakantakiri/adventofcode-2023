# --- Day 13: Point of Incidence ---
# With your help, the hot springs team locates an appropriate spring which launches you neatly and precisely up to the edge of Lava Island.

# There's just one problem: you don't see any lava.

# You do see a lot of ash and igneous rock; there are even what look like gray mountains scattered around. After a while, you make your way to a nearby cluster of mountains only to discover that the valley between them is completely full of large mirrors. Most of the mirrors seem to be aligned in a consistent way; perhaps you should head in that direction?

# As you move through the valley of mirrors, you find that several of them have fallen from the large metal frames keeping them in place. The mirrors are extremely flat and shiny, and many of the fallen mirrors have lodged into the ash at strange angles. Because the terrain is all one color, it's hard to tell where it's safe to walk or where you're about to run into a mirror.

# You note down the patterns of ash (.) and rocks (#) that you see as you walk (your puzzle input); perhaps by carefully analyzing these patterns, you can figure out where the mirrors are!

# For example:

# #.##..##.
# ..#.##.#.
# ##......#
# ##......#
# ..#.##.#.
# ..##..##.
# #.#.##.#.

# #...##..#
# #....#..#
# ..##..###
# #####.##.
# #####.##.
# ..##..###
# #....#..#
# To find the reflection in each pattern, you need to find a perfect reflection across either a horizontal line between two rows or across a vertical line between two columns.

# In the first pattern, the reflection is across a vertical line between two columns; arrows on each of the two columns point at the line between the columns:

# 123456789
#     ><   
# #.##..##.
# ..#.##.#.
# ##......#
# ##......#
# ..#.##.#.
# ..##..##.
# #.#.##.#.
#     ><   
# 123456789
# In this pattern, the line of reflection is the vertical line between columns 5 and 6. Because the vertical line is not perfectly in the middle of the pattern, part of the pattern (column 1) has nowhere to reflect onto and can be ignored; every other column has a reflected column within the pattern and must match exactly: column 2 matches column 9, column 3 matches 8, 4 matches 7, and 5 matches 6.

# The second pattern reflects across a horizontal line instead:

# 1 #...##..# 1
# 2 #....#..# 2
# 3 ..##..### 3
# 4v#####.##.v4
# 5^#####.##.^5
# 6 ..##..### 6
# 7 #....#..# 7
# This pattern reflects across the horizontal line between rows 4 and 5. Row 1 would reflect with a hypothetical row 8, but since that's not in the pattern, row 1 doesn't need to match anything. The remaining rows match: row 2 matches row 7, row 3 matches row 6, and row 4 matches row 5.

# To summarize your pattern notes, add up the number of columns to the left of each vertical line of reflection; to that, also add 100 multiplied by the number of rows above each horizontal line of reflection. In the above example, the first pattern's vertical line has 5 columns to its left and the second pattern's horizontal line has 4 rows above it, a total of 405.

# Find the line of reflection in each of the patterns in your notes. What number do you get after summarizing all of your notes?

# Your puzzle answer was 32723.

# --- Part Two ---
# You resume walking through the valley of mirrors and - SMACK! - run directly into one. Hopefully nobody was watching, because that must have been pretty embarrassing.

# Upon closer inspection, you discover that every mirror has exactly one smudge: exactly one . or # should be the opposite type.

# In each pattern, you'll need to locate and fix the smudge that causes a different reflection line to be valid. (The old reflection line won't necessarily continue being valid after the smudge is fixed.)

# Here's the above example again:

# #.##..##.
# ..#.##.#.
# ##......#
# ##......#
# ..#.##.#.
# ..##..##.
# #.#.##.#.

# #...##..#
# #....#..#
# ..##..###
# #####.##.
# #####.##.
# ..##..###
# #....#..#
# The first pattern's smudge is in the top-left corner. If the top-left # were instead ., it would have a different, horizontal line of reflection:

# 1 ..##..##. 1
# 2 ..#.##.#. 2
# 3v##......#v3
# 4^##......#^4
# 5 ..#.##.#. 5
# 6 ..##..##. 6
# 7 #.#.##.#. 7
# With the smudge in the top-left corner repaired, a new horizontal line of reflection between rows 3 and 4 now exists. Row 7 has no corresponding reflected row and can be ignored, but every other row matches exactly: row 1 matches row 6, row 2 matches row 5, and row 3 matches row 4.

# In the second pattern, the smudge can be fixed by changing the fifth symbol on row 2 from . to #:

# 1v#...##..#v1
# 2^#...##..#^2
# 3 ..##..### 3
# 4 #####.##. 4
# 5 #####.##. 5
# 6 ..##..### 6
# 7 #....#..# 7
# Now, the pattern has a different horizontal line of reflection between rows 1 and 2.

# Summarize your notes as before, but instead use the new different reflection lines. In this example, the first pattern's new horizontal line has 3 rows above it and the second pattern's new horizontal line has 1 row above it, summarizing to the value 400.

# In each pattern, fix the smudge and find the different line of reflection. What number do you get after summarizing the new reflection line in each pattern in your notes?

# Your puzzle answer was 34536.

f = open('inputs/doc_day_13.txt')
lines = f.read()
lines = lines.splitlines()

def get_patterns(lines):
    patterns = []
    part = []
    for line in lines:
        if line != '':
            part.append(line)
        else:
            patterns.append(part)
            part = []
    patterns.append(part)
    return patterns

def get_cols(pattern):
    cols = []
    x = 0
    while x<(len(pattern[0])):
        col = ''
        for row in pattern:
            col = col + row[x]
        cols.append(col)
        x+=1
    return cols

def get_miss_match_count(string1, string2):
    l=0
    diff = 0
    while l< len(string1):
        if(string1[l] != string2[l] ):
            diff += 1
        l+=1
    return diff
        
def validate_candidate(candidate, pattern):
    i = candidate
    j = candidate+1
    used = 0
    to_fix = []
    while(i>=0 and j<=len(pattern)-1):
        if( pattern[i] != pattern[j]):
            if abs(pattern[i].count('#')- pattern[j].count('#')) != 1:
                return False
            else:
                if(get_miss_match_count(pattern[i], pattern[j]) == 1 and used == 0):
                    to_fix = [i,j]
                    used = used + 1
                else:
                    return False
        i-=1
        j+=1

    if len(to_fix) == 0: # It is a perfect mirror
        return False

    return True


def get_imperfect_reflection(pattern):
    last_count = -10
    candidates = []
    for i, p in enumerate(pattern):
        count = p.count('#')
        if abs(count - last_count) <= 1:
            candidates.append(i-1)
        last_count = count

    valid_candidates = []
    for c in candidates:
        if (validate_candidate(c, pattern)):
            valid_candidates.append(c)
    
    if len(valid_candidates) == 0: 
        return -1
    else: 
        return valid_candidates[0]
    
def get_reflection(pattern):
    l = 0
    mirror = -1
    while l<len(pattern):
        if(l<len(pattern)-1):
            if pattern[l] == pattern[l+1]:
                i = l
                j = l+1
                is_mirror = True
                while(i>=0 and j<len(pattern)):
                    if (pattern[i] != pattern[j]):
                        is_mirror =  False
                    i-=1
                    j+=1
                if is_mirror:
                    mirror = l
        l+=1
    return mirror

################################ Execution

patterns = get_patterns(lines)
h_reflections = []
for p in patterns:
    h_ref = get_reflection(p)
    if h_ref >= 0:
        h_reflections.append(h_ref)


v_reflections = []
for p in patterns:
    v_ref = get_reflection(get_cols(p))
    if v_ref >= 0:
        v_reflections.append(v_ref)

print(f'Solution 1: {(sum(h_reflections)+len(h_reflections))*100+(sum(v_reflections)+len(v_reflections))}')


h_reflections = []
for p in patterns:
    h_ref = get_imperfect_reflection(p)
    if h_ref >= 0:
        h_reflections.append(h_ref)

v_reflections = []
for p in patterns:
    v_ref = get_imperfect_reflection(get_cols(p))
    if v_ref >= 0:
        v_reflections.append(v_ref)

print(f'Solution 2: {(sum(h_reflections)+len(h_reflections))*100+(sum(v_reflections)+len(v_reflections))}')

# Solution 1: 32723
# Solution 2: 34536