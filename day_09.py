# --- Day 9: Mirage Maintenance ---
# You ride the camel through the sandstorm and stop where the ghost's maps told you to stop. The sandstorm subsequently subsides, somehow seeing you standing at an oasis!

# The camel goes to get some water and you stretch your neck. As you look up, you discover what must be yet another giant floating island, this one made of metal! That must be where the parts to fix the sand machines come from.

# There's even a hang glider partially buried in the sand here; once the sun rises and heats up the sand, you might be able to use the glider and the hot air to get all the way up to the metal island!

# While you wait for the sun to rise, you admire the oasis hidden here in the middle of Desert Island. It must have a delicate ecosystem; you might as well take some ecological readings while you wait. Maybe you can report any environmental instabilities you find to someone so the oasis can be around for the next sandstorm-worn traveler.

# You pull out your handy Oasis And Sand Instability Sensor and analyze your surroundings. The OASIS produces a report of many values and how they are changing over time (your puzzle input). Each line in the report contains the history of a single value. For example:

# 0 3 6 9 12 15
# 1 3 6 10 15 21
# 10 13 16 21 30 45
# To best protect the oasis, your environmental report should include a prediction of the next value in each history. To do this, start by making a new sequence from the difference at each step of your history. If that sequence is not all zeroes, repeat this process, using the sequence you just generated as the input sequence. Once all of the values in your latest sequence are zeroes, you can extrapolate what the next value of the original history should be.

# In the above dataset, the first history is 0 3 6 9 12 15. Because the values increase by 3 each step, the first sequence of differences that you generate will be 3 3 3 3 3. Note that this sequence has one fewer value than the input sequence because at each step it considers two numbers from the input. Since these values aren't all zero, repeat the process: the values differ by 0 at each step, so the next sequence is 0 0 0 0. This means you have enough information to extrapolate the history! Visually, these sequences can be arranged like this:

# 0   3   6   9  12  15
#   3   3   3   3   3
#     0   0   0   0
# To extrapolate, start by adding a new zero to the end of your list of zeroes; because the zeroes represent differences between the two values above them, this also means there is now a placeholder in every sequence above it:

# 0   3   6   9  12  15   B
#   3   3   3   3   3   A
#     0   0   0   0   0
# You can then start filling in placeholders from the bottom up. A needs to be the result of increasing 3 (the value to its left) by 0 (the value below it); this means A must be 3:

# 0   3   6   9  12  15   B
#   3   3   3   3   3   3
#     0   0   0   0   0
# Finally, you can fill in B, which needs to be the result of increasing 15 (the value to its left) by 3 (the value below it), or 18:

# 0   3   6   9  12  15  18
#   3   3   3   3   3   3
#     0   0   0   0   0
# So, the next value of the first history is 18.

# Finding all-zero differences for the second history requires an additional sequence:

# 1   3   6  10  15  21
#   2   3   4   5   6
#     1   1   1   1
#       0   0   0
# Then, following the same process as before, work out the next value in each sequence from the bottom up:

# 1   3   6  10  15  21  28
#   2   3   4   5   6   7
#     1   1   1   1   1
#       0   0   0   0
# So, the next value of the second history is 28.

# The third history requires even more sequences, but its next value can be found the same way:

# 10  13  16  21  30  45  68
#    3   3   5   9  15  23
#      0   2   4   6   8
#        2   2   2   2
#          0   0   0
# So, the next value of the third history is 68.

# If you find the next value for each history in this example and add them together, you get 114.

# Analyze your OASIS report and extrapolate the next value for each history. What is the sum of these extrapolated values?

# Your puzzle answer was 1887980197.

# --- Part Two ---
# Of course, it would be nice to have even more history included in your report. Surely it's safe to just extrapolate backwards as well, right?

# For each history, repeat the process of finding differences until the sequence of differences is entirely zero. Then, rather than adding a zero to the end and filling in the next values of each previous sequence, you should instead add a zero to the beginning of your sequence of zeroes, then fill in new first values for each previous sequence.

# In particular, here is what the third example history looks like when extrapolating back in time:

# 5  10  13  16  21  30  45
#   5   3   3   5   9  15
#    -2   0   2   4   6
#       2   2   2   2
#         0   0   0
# Adding the new values on the left side of each sequence from bottom to top eventually reveals the new left-most history value: 5.

# Doing this for the remaining example data above results in previous values of -3 for the first history and 0 for the second history. Adding all three new values together produces 2.

# Analyze your OASIS report again, this time extrapolating the previous value for each history. What is the sum of these extrapolated values?

# Your puzzle answer was 990.

f = open('inputs/doc_day_09.txt')
lines = f.read()
lines = lines.splitlines()
# print(lines)

def get_hs (lines):
    hs = [] 
    for line in lines:
        hs.append([int(x) for x in line.split(' ')])
    return hs

def iterate(hs):
    iterations = []
    for h in hs:
        # print(f'Processing history: {h}')
        rs = []
        f= False
        p = h
        while( f == False):
            r = []
            for i,n in enumerate(p):
                if (i< len(p)-1):
                    r.append(p[i+1] - n)
            # print(f' - r: {r}')
            rs.append(r)
            if sum(r) == 0:
                f = True
            else:
                p = r
        # print(f'iteration: {[h]+[rs]}')
        iterations.append([h]+[r for r in rs])
    return iterations

def get_nexts ( iterations):
    sums = []
    for iter in iterations:
        sum = 0
        for p in iter:
            # print(f'Curent sum = {sum}, adding value: {p}')
            sum = sum + p[len(p)-1]
        sums.append(sum)
    return(sums)
def get_prevs ( iterations):
    sums = []
    for iter in iterations:
        sum = 0
        for i, p in enumerate(iter):
            if(i%2):
                sum = sum - p[0]
            else:
                sum = sum + p[0]  
        sums.append(sum)
    return(sums)

## Execution
iterations = iterate(get_hs(lines))
nexts = get_nexts(iterations)
# print('iterations')
# print(iterations)
# print('nexts')
# print(nexts)
print(f'Solution 1: {sum(nexts)}') # Done in: 24m03s67

prevs = get_prevs(iterations)
# print('prevs')
# print(prevs)
print(f'Solution 2: {sum(prevs)}') # Done in: 7m13s67


# Solution 1: 1887980197
# Solution 2: 990