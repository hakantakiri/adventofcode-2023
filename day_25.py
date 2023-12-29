f = open('inputs/doc_day_25.txt')
lines = f.read()
lines = lines.splitlines()

def get_pairs(connections):
    pairs = []
    for name in connections:
        for dest in connections[name]:
            if [name, dest] not in pairs and [dest, name] not in pairs:
                pairs.append([name, dest])
    return pairs

def get_nodes_and_connections(lines):
    components = {}
    nodes = []
    for line in lines:
        start = line.split(':')[0]
        others = [ node.strip() for node in line.split(':')[1].split(' ') if node != '']
        if start in components:
            components[start] = components[start]+others
        else:
            nodes.append(start)
            components[start] = others
        for o in others:
            if o in components:
                components[o].append(start)
            else:
                nodes.append(o)
                components[o]=[start]
    return (nodes, components)

def has_connection(n1, n2, pairs):
    if ([n1,n2] in pairs or [n2, n1] in pairs):
        return True
    else:
        return False

def reach_all(start, connections):
    seen = [start]
    currents = [start]
    next_cons = 1
    while (len(currents)>0 and (next_cons!=3)):
        (currents, next_cons) = find_next(currents, seen, connections)
        # print(f'- currents:  {len(currents)}, next: {next_cons}\t\t\t\t\t', end='\r')
    return seen

def find_next(currents, seen, connections):
    new_currents = []
    for curr in currents:
        for next in connections[curr] :
            # if(has_connection(curr, next)):
                if(next not in seen):
                    seen.append(next)
                    new_currents.append(next)
    next_cons = 0
    for n in new_currents:
        for dest in connections[n]:
            if dest not in seen:
                next_cons +=1
    return (new_currents, next_cons)

def part_1(nodes, connections):
    for i, n in enumerate(nodes):
        print(f'Testing starter node {n}. {i} out of {len(nodes)}\t\t\t\t\t\t', end='\r')
        seen = reach_all(n, connections)
        if( len(seen) != len(nodes)):
            return seen
    return []
(nodes, g_connections) = get_nodes_and_connections(lines)
print(f'Got nodes: {len(nodes)}')
print(f'Got grouped connections: {len(g_connections)}')
# pairs = get_pairs(g_connections)
# print(f'Got pairs: {len(pairs)}', end= '\r')

seen = part_1(nodes, g_connections)
print(f'\nFound groups: {len(seen)}, {(len(nodes)-len(seen))}')
print(f'Solution 1: {len(seen)*(len(nodes)-len(seen))}')
