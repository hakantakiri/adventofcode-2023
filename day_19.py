import time
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
    # print(f'processing flow {flow}')
    if flow.find('>')>= 0 or flow.find('<')>= 0:
        operator = '>'
        if flow.find('<')>=0:
            operator = '<'
        # print(f'- operator is {operator}')
        num = int(flow.split(operator)[1].split(':')[0])
        # print(f'- num is {num}')
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
    # sum = 0 
    for step in workflow:
        # print(f'- working parts {parts} in workflow "{work_id}" step {step} ')
        s = format_step(step)
        
        if s['step_type'] == 'A':
            # sum += num
            return 'A'
        elif s['step_type'] == 'R':
            # sum += 0
            # return 0
            return 'R'
        elif s['step_type'] == 'rd':
            return process_part(parts, s['destination'], work)
        else:
            part = get_part_by_type(parts, s['input_type'])
            part_type = part[0]
            num = int(part.split('=')[1])

            # print(f'- - Choosed part is {part} for step {step} ')
            if s['input_type'] == part_type:
                if s['operator'] == '>':
                    if num > s['num']:
                        if s['dest_type'] == 'A':
                            # sum += num
                            return 'A'
                        elif s['dest_type'] == "R":
                            # sum += 0
                            return 'R'
                        else:
                            return process_part(parts, s['destination'], work)
                    # else:
                    #     print('next step')
                    #     sum +=0
                else: # s.operator == '<'
                    if num < s['num']:
                        if s['dest_type'] == 'A':
                            # sum += num
                            return 'A'
                        elif s['dest_type'] == "R":
                            # sum += 0
                            return 'R'
                        else:
                            return process_part(parts, s['destination'], work)
                    # else:
                    #     sum+=0
                    #     print('next step')

def process_parts(parts,  work):
    starting_work_id = 'in'

    status = process_part(parts, starting_work_id, work)
    print(f'Result status for parts {parts} is {status}')
    sum = 0
    if (status == 'A'):
        for part in parts:
            sum += int(part.split('=')[1])

    return sum

def process_all_part(group_parts, work):
    sum = 0
    for parts in group_parts:
        sum += process_parts(parts, work)
    return sum


def part2(work):
    starting_work_id = 'in'
    sum_a = 0
    sum_r = 0
    for i in range(1, 4000):
        for j in range(1, 4000):
            for t in range(1, 4000):
                for r in range(1, 4000):
                    parts = ['x='+str(i),'m='+str(j),'a='+str(t),'s='+str(r)]
                    status = process_part(parts, starting_work_id, work)
                    # print(f'At id: {i},{j},{t},{r} result is {status}')
                    time.sleep(0.0001)
                    if status == 'A':
                        if sum_a == 0:
                            print(f'At combination {i},{j},{t},{r} R: {sum_r}')
                        sum_a += 1
                        sum_r = 0
                    else:
                        if sum_r == 0:
                            print(f'At combination {i},{j},{t},{r} A: {sum_a}')
                        sum_r += 1
                        sum_a = 0


############################# EXECUTION

work = get_work(work_raw)
group_parts = get_part_groups(parts_raw)
print(f'Solution 1: {process_all_part(group_parts, work)}')


print('Working on solution 2:')
print(part2(work))