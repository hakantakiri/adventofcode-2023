# --- Day 8: Haunted Wasteland ---
# You're still riding a camel across Desert Island when you spot a sandstorm quickly approaching. When you turn to warn the Elf, she disappears before your eyes! To be fair, she had just finished warning you about ghosts a few minutes ago.

# One of the camel's pouches is labeled "maps" - sure enough, it's full of documents (your puzzle input) about how to navigate the desert. At least, you're pretty sure that's what they are; one of the documents contains a list of left/right instructions, and the rest of the documents seem to describe some kind of network of labeled nodes.

# It seems like you're meant to use the left/right instructions to navigate the network. Perhaps if you have the camel follow the same instructions, you can escape the haunted wasteland!

# After examining the maps for a bit, two nodes stick out: AAA and ZZZ. You feel like AAA is where you are now, and you have to follow the left/right instructions until you reach ZZZ.

# This format defines each node of the network individually. For example:

# RL

# AAA = (BBB, CCC)
# BBB = (DDD, EEE)
# CCC = (ZZZ, GGG)
# DDD = (DDD, DDD)
# EEE = (EEE, EEE)
# GGG = (GGG, GGG)
# ZZZ = (ZZZ, ZZZ)
# Starting with AAA, you need to look up the next element based on the next left/right instruction in your input. In this example, start with AAA and go right (R) by choosing the right element of AAA, CCC. Then, L means to choose the left element of CCC, ZZZ. By following the left/right instructions, you reach ZZZ in 2 steps.

# Of course, you might not find ZZZ right away. If you run out of left/right instructions, repeat the whole sequence of instructions as necessary: RL really means RLRLRLRLRLRLRLRL... and so on. For example, here is a situation that takes 6 steps to reach ZZZ:

# LLR

# AAA = (BBB, BBB)
# BBB = (AAA, ZZZ)
# ZZZ = (ZZZ, ZZZ)
# Starting at AAA, follow the left/right instructions. How many steps are required to reach ZZZ?

# Your puzzle answer was 20093.

# --- Part Two ---
# The sandstorm is upon you and you aren't any closer to escaping the wasteland. You had the camel follow the instructions, but you've barely left your starting position. It's going to take significantly more steps to escape!

# What if the map isn't for people - what if the map is for ghosts? Are ghosts even bound by the laws of spacetime? Only one way to find out.

# After examining the maps a bit longer, your attention is drawn to a curious fact: the number of nodes with names ending in A is equal to the number ending in Z! If you were a ghost, you'd probably just start at every node that ends with A and follow all of the paths at the same time until they all simultaneously end up at nodes that end with Z.

# For example:

# LR

# 11A = (11B, XXX)
# 11B = (XXX, 11Z)
# 11Z = (11B, XXX)
# 22A = (22B, XXX)
# 22B = (22C, 22C)
# 22C = (22Z, 22Z)
# 22Z = (22B, 22B)
# XXX = (XXX, XXX)
# Here, there are two starting nodes, 11A and 22A (because they both end with A). As you follow each left/right instruction, use that instruction to simultaneously navigate away from both nodes you're currently on. Repeat this process until all of the nodes you're currently on end with Z. (If only some of the nodes you're on end with Z, they act like any other node and you continue as normal.) In this example, you would proceed as follows:

# Step 0: You are at 11A and 22A.
# Step 1: You choose all of the left paths, leading you to 11B and 22B.
# Step 2: You choose all of the right paths, leading you to 11Z and 22C.
# Step 3: You choose all of the left paths, leading you to 11B and 22Z.
# Step 4: You choose all of the right paths, leading you to 11Z and 22B.
# Step 5: You choose all of the left paths, leading you to 11B and 22C.
# Step 6: You choose all of the right paths, leading you to 11Z and 22Z.
# So, in this example, you end up entirely on nodes that end in Z after 6 steps.

# Simultaneously start on every node that ends with A. How many steps does it take before you're only on nodes that end with Z?

# Your puzzle answer was 22103062509257.

import math
f = open('inputs/doc_day_08.txt')
lines = f.read()
lines = lines.splitlines()
# print(lines)

def format_lines(lines):
    ins = [x for x in lines[0] ]
    nodes = []
    for i, line in enumerate(lines):
        if i >= 2:
            nodes.append([line.split(' ')[0], line.split(' ')[2][1:4], line.split(' ')[3][0:3]])
    return [ins, nodes]

def find_idx(dest, nodes):
    idx = [i for i,n in enumerate(nodes) if n[0] == dest]
    # print(f'Obtained idx for dest {dest} is {idx}')
    return idx[0]

def find_idx_starting(nodes):
    idx = [i for i,n in enumerate(nodes) if n[0][2] == 'A']
    # print(f'Obtained idx for dest {dest} is {idx}')
    return idx

def walk(ins, nodes):
    i = 0
    j = find_idx('AAA', nodes)
    found = False
    dest = ''
    steps = 0

    while (found == False):
        # print(f'Executing instruction {ins[i]} at node {nodes[j]}')
        n = nodes[j]
        # n1 = left | n2 = right
        if ins[i] == 'R':
            dest = n[2] 
        elif ins[i] == 'L':
            dest = n[1]
        else:
            print(f'ERROR: Error getting {ins[i]} for node {n}')
            raise Exception('Error ',n) 
        
        steps = steps + 1
        i = i +1
        if (i == len(ins)):
            i = 0

        j = find_idx(dest, nodes)
        if dest == 'ZZZ':
            found = True
    
    return steps

def get_lcm(nums):
    def lcm_two(a, b):
        return abs(a * b) // math.gcd(a, b)
    if (len(nums) == 1): return nums[0]
    if (len(nums) == 2): return lcm_two(nums[0], nums[1])
    if (len(nums)>2):
        i = 0
        res = 1
        while i < len(nums):
            res  = lcm_two(res, nums[i])
            i = i+1
        return res

def walk_2 (ins, nodes):
    i = 0
    starting = find_idx_starting(nodes)
    js = find_idx_starting(nodes)
    # print(f'Starting idx  {js}')
    steps = 0
    found_all = 0
    steps_to_loop = {}
    while (found_all != len(js)): 
        # print(f'New step with nodes at index {js}.')
        new_js = []
        found_all = 0
        dest = ''
        for p, j in enumerate(js):
            # print(f'- For node {nodes[j]} applying inst {ins[i]}')
            n = nodes[j]
            # n1 = left | n2 = right
            if ins[i] == 'R':
                dest = n[2] 
                # print(f'- - Picked dest: {dest}')
            elif ins[i] == 'L':
                dest = n[1]
                # print(f'- - Picked dest: {dest}')
            else:
                print(f'ERROR: Error getting {ins[i]} for node {n}')
                raise Exception('Error ',n) 
            

            j = find_idx(dest, nodes)
            new_js.append(j)
            if dest[2] == 'Z':
                print(f'For node {nodes[starting[p]]} with id {starting[p]} found finish node {dest} with steps: {steps+1}')
                steps_to_loop[nodes[starting[p]][0]] = steps+1
                if( len(steps_to_loop ) == len(starting)):
                    print(f'Found all min loops for {len(starting)} nodes that finishes with "A"')
                    print(f'Calculating LCM for min loops {[steps_to_loop[i] for i in steps_to_loop]}')
                    lcm = get_lcm([steps_to_loop[i] for i in steps_to_loop])
                    return lcm

                found_all = found_all + 1
        
        steps = steps + 1

        i = i +1
        if (i == len(ins)):
            i = 0

        js = new_js

    return steps

################################## EXECUTION

[ins, nodes] = format_lines(lines)

# print(f'Instructions: {ins}')
# print(f'Nodes: {nodes}')
steps = walk(ins, nodes)
print(f'Solution 1: {steps}')

# print('starting for solution 2')
# print(find_idx_starting(nodes))
steps2 = walk_2(ins, nodes)
print(f'Solution 2: {steps2}')

# Solution 1: 20093
# For node ['LHA', 'RFJ', 'VBJ'] with id 568 found finish node BKZ with steps: 14999
# For node ['LDA', 'BJV', 'SLG'] with id 735 found finish node XLZ with steps: 16697
# For node ['RHA', 'NQP', 'JLP'] with id 570 found finish node XNZ with steps: 17263
# For node ['AAA', 'XHV', 'KDJ'] with id 467 found finish node ZZZ with steps: 20093
# For node ['VGA', 'QGF', 'MRL'] with id 201 found finish node PQZ with steps: 20659
# For node ['CVA', 'QKR', 'HFM'] with id 678 found finish node KJZ with steps: 22357
# Found all min loops for 6 nodes that finishes with "A"
# Calculating LCM for min loops [14999, 16697, 17263, 20093, 20659, 22357]
# Solution 2: 22103062509257