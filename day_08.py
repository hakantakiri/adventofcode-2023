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