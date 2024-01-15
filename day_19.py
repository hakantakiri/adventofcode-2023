# --- Day 19: Aplenty ---
# The Elves of Gear Island are thankful for your help and send you on your way. They even have a hang glider that someone stole from Desert Island; since you're already going that direction, it would help them a lot if you would use it to get down there and return it to them.

# As you reach the bottom of the relentless avalanche of machine parts, you discover that they're already forming a formidable heap. Don't worry, though - a group of Elves is already here organizing the parts, and they have a system.

# To start, each part is rated in each of four categories:

# x: Extremely cool looking
# m: Musical (it makes a noise when you hit it)
# a: Aerodynamic
# s: Shiny
# Then, each part is sent through a series of workflows that will ultimately accept or reject the part. Each workflow has a name and contains a list of rules; each rule specifies a condition and where to send the part if the condition is true. The first rule that matches the part being considered is applied immediately, and the part moves on to the destination described by the rule. (The last rule in each workflow has no condition and always applies if reached.)

# Consider the workflow ex{x>10:one,m<20:two,a>30:R,A}. This workflow is named ex and contains four rules. If workflow ex were considering a specific part, it would perform the following steps in order:

# Rule "x>10:one": If the part's x is more than 10, send the part to the workflow named one.
# Rule "m<20:two": Otherwise, if the part's m is less than 20, send the part to the workflow named two.
# Rule "a>30:R": Otherwise, if the part's a is more than 30, the part is immediately rejected (R).
# Rule "A": Otherwise, because no other rules matched the part, the part is immediately accepted (A).
# If a part is sent to another workflow, it immediately switches to the start of that workflow instead and never returns. If a part is accepted (sent to A) or rejected (sent to R), the part immediately stops any further processing.

# The system works, but it's not keeping up with the torrent of weird metal shapes. The Elves ask if you can help sort a few parts and give you the list of workflows and some part ratings (your puzzle input). For example:

# px{a<2006:qkq,m>2090:A,rfg}
# pv{a>1716:R,A}
# lnx{m>1548:A,A}
# rfg{s<537:gd,x>2440:R,A}
# qs{s>3448:A,lnx}
# qkq{x<1416:A,crn}
# crn{x>2662:A,R}
# in{s<1351:px,qqz}
# qqz{s>2770:qs,m<1801:hdj,R}
# gd{a>3333:R,R}
# hdj{m>838:A,pv}

# {x=787,m=2655,a=1222,s=2876}
# {x=1679,m=44,a=2067,s=496}
# {x=2036,m=264,a=79,s=2244}
# {x=2461,m=1339,a=466,s=291}
# {x=2127,m=1623,a=2188,s=1013}
# The workflows are listed first, followed by a blank line, then the ratings of the parts the Elves would like you to sort. All parts begin in the workflow named in. In this example, the five listed parts go through the following workflows:

# {x=787,m=2655,a=1222,s=2876}: in -> qqz -> qs -> lnx -> A
# {x=1679,m=44,a=2067,s=496}: in -> px -> rfg -> gd -> R
# {x=2036,m=264,a=79,s=2244}: in -> qqz -> hdj -> pv -> A
# {x=2461,m=1339,a=466,s=291}: in -> px -> qkq -> crn -> R
# {x=2127,m=1623,a=2188,s=1013}: in -> px -> rfg -> A
# Ultimately, three parts are accepted. Adding up the x, m, a, and s rating for each of the accepted parts gives 7540 for the part with x=787, 4623 for the part with x=2036, and 6951 for the part with x=2127. Adding all of the ratings for all of the accepted parts gives the sum total of 19114.

# Sort through all of the parts you've been given; what do you get if you add together all of the rating numbers for all of the parts that ultimately get accepted?

# Your puzzle answer was 397134.

# --- Part Two ---
# Even with your help, the sorting process still isn't fast enough.

# One of the Elves comes up with a new plan: rather than sort parts individually through all of these workflows, maybe you can figure out in advance which combinations of ratings will be accepted or rejected.

# Each of the four ratings (x, m, a, s) can have an integer value ranging from a minimum of 1 to a maximum of 4000. Of all possible distinct combinations of ratings, your job is to figure out which ones will be accepted.

# In the above example, there are 167409079868000 distinct combinations of ratings that will be accepted.

# Consider only your list of workflows; the list of part ratings that the Elves wanted you to sort is no longer relevant. How many distinct combinations of ratings will be accepted by the Elves' workflows?

# Your puzzle answer was 127517902575337.

import copy
f = open('inputs/doc_day_19.txt')
lines = f.read()
work_raw = lines.split('\n\n')[0]
parts_raw = lines.split('\n\n')[1]

def get_work(work_raw):
    work = {}
    names = [line.split('{')[0] for line in work_raw.splitlines()]
    conditions = [ line.split('{')[1].split('}')[0].split(',') for line in work_raw.splitlines()]
    for i, name in enumerate(names):
        work[name] = conditions[i]
    return  work

def get_part_groups(parts_raw):
    return [ line.split('{')[1].split('}')[0].split(',')for line in parts_raw.splitlines()]


def format_step(flow):
    if flow.find('>')>= 0 or flow.find('<')>= 0:
        operator = '>'
        if flow.find('<')>=0:
            operator = '<'

        num = int(flow.split(operator)[1].split(':')[0])
        
        destination = flow.split(':')[1]
        dest_type = 'rd'
        if destination == 'A':
            dest_type = 'A'
        if destination == 'R':
            dest_type = 'R'

        return {
            'step_type': 'process',
            'input_type': flow[0],
            'operator': operator,
            'num': num,
            'dest_type': dest_type,
            'destination': destination
        }
    else:
        if flow == 'A':
            return {
                'step_type': 'A',
            }
        elif flow == 'R':
            return {
                'step_type': 'R',
            }
        else:
            return {
                'step_type': 'rd',
                'destination': flow
            }
        
def get_part_by_type (parts, type):
    for part in parts:
        if part[0] == type:
            return part
        
def process_part(parts, work_id, work):
    workflow = work[work_id]
    for step in workflow:
        s = format_step(step)
        
        if s['step_type'] == 'A':
            return 'A'
        elif s['step_type'] == 'R':
            return 'R'
        elif s['step_type'] == 'rd':
            return process_part(parts, s['destination'], work)
        elif s['step_type'] == 'process':
            part = get_part_by_type(parts, s['input_type'])
            num = int(part.split('=')[1])
            if s['operator'] == '>':
                if num > s['num']:
                    if s['dest_type'] == 'A':
                        return 'A'
                    elif s['dest_type'] == "R":
                        return 'R'
                    else:
                        return process_part(parts, s['destination'], work)
            else: # s.operator == '<'
                if num < s['num']:
                    if s['dest_type'] == 'A':
                        return 'A'
                    elif s['dest_type'] == "R":
                        return 'R'
                    else:
                        return process_part(parts, s['destination'], work)

def process_parts(parts,  work):
    starting_work_id = 'in'

    status = process_part(parts, starting_work_id, work)
    sum = 0
    if (status == 'A'):
        for part in parts:
            sum += int(part.split('=')[1])

    return sum

def part_1(group_parts, work):
    sum = 0
    for parts in group_parts:
        sum += process_parts(parts, work)
    return sum

sol = []
def part_2(work):
    init_range = {'type': 'ND',
        'destination': 'in',
        'parts': {
            'x': [1,4000],
            'm': [1,4000],
            'a': [1,4000],
            's': [1,4000]
        }}
    
    process_range(init_range, 'in', work)
    sum_products = 0
    for s in sol:
        if s['type'] == 'A':
            prod = 1
            for r in s['parts']:
                prod *= (s['parts'][r][1]-s['parts'][r][0] +1)
            sum_products += prod
    return sum_products

def process_range(range_info, work_id, work):
    if(work_id == 'A' or work_id == 'R'):
        range_info['type'] = work_id
        sol.append(range_info)
        return
    
    workflow = work[work_id]

    for step in workflow:
        s = format_step(step)
        
        if s['step_type'] == 'A' or s['step_type'] == 'R':
            range_info['type'] =  s['step_type']
            process_range(range_info,  s['step_type'], work)
        elif s['step_type'] == 'rd':
            range_info['destination'] = s['destination']
            process_range(range_info, s['destination'], work)
        
        elif s['step_type'] == 'process':
            range_type = s['input_type']
            num_min, num_max = range_info['parts'][range_type][0], range_info['parts'][range_type][1]

            if s['operator'] == '>':
                if s['num'] < num_min :
                    if s['dest_type'] == 'A' or s['dest_type'] == 'R':
                        range_info['type'] = s['dest_type']
                        process_range(range_info, s['dest_type'], work)
                    else:
                        range_info['destination'] = s['destination']
                        process_range(range_info, s['destination'], work)
                elif num_min<=s['num'] and s['num']<num_max:
                    sub_range_info = copy.deepcopy(range_info)
                    sub_range_info['parts'][s['input_type']] = [s['num']+1, num_max]
                    sub_range_info['destination'] = s['destination']
                    range_info['parts'][s['input_type']] = [num_min, s['num']]
                    process_range(sub_range_info, s['destination'], work)

            else: # s.operator == '<'
                if num_max < s['num']:
                    if s['dest_type'] == 'A' or s['dest_type'] == 'R':
                        range_info['type'] = s['dest_type']
                        process_range(range_info, s['dest_type'], work)
                    else:
                        range_info['destination'] = s['destination']
                        process_range(range_info, s['destination'], work)
                elif num_min<s['num'] and s['num']<=num_max:
                    sub_range_info = copy.deepcopy(range_info)
                    sub_range_info['parts'][s['input_type']] = [num_min, s['num']-1]
                    sub_range_info['destination'] = s['destination']
                    range_info['parts'][s['input_type']] = [s['num'], num_max]
                    process_range(sub_range_info, s['destination'], work)

############################# EXECUTION

work = get_work(work_raw)
group_parts = get_part_groups(parts_raw)

print(f'Solution 1: {part_1(group_parts, work)}')
print(f'Solution 2: {part_2(work)}')

# Solution 1: 397134
# Solution 2: 127517902575337