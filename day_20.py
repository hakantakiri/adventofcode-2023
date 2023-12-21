# % starts off, recieves high ignore, recieves low inverse is current state and send high if was off, send low if was on
# low  -> %off %on send high
# high -> %off %off
# low  -> %on %off send low
# high -> %on -ignore (maybe not happing)

# & remembers, start with LOW, if ALL inputs are HIGH send LOW, else sen HIGH
# all HIGH -> LOW
# mix ------> HIGH
# all LOW  -> HIGH
 
# Broadcaster just REPEAT input to ALL destinations

# button module send a single LOW to Broadcaster

import copy
f = open('inputs/doc_day_20.txt')
lines = f.read()
lines = lines.splitlines()
# print(lines)

def get_broadcaster(lines):
    broad = [line for line in lines if line.find('broadcaster') >= 0][0].split(' ')[0]
    destinations = [x.strip() for x in [line for line in lines if line.find('broadcaster') >= 0][0].split('->')[1].strip().split(',')]
    return {
        'name': broad,
        'destinations': destinations
    }

def format_module(r_module):
    type = r_module[0]
    name = r_module.split('->')[0][1:].strip()
    destinations = [d.strip() for d in r_module.split('->')[1].split(',')]
    return {
        'type': type,
        'name': name,
        'destinations': destinations,
        'state': {}
    }

def get_modules(lines):
    r_modules = [line for line in lines if line.find('broadcaster') < 0]
    modules = {}
    for m in r_modules:
        fm = format_module(m)
        modules[fm['name']] = fm
    return modules

class Broadcaster:
    def __init__(self, destinations):
        self.destinations = destinations # [name]
    
    def press_button(self, modules):
        for d in self.destinations:
            modules[d].receive_signal(d, 'low')
        return [0, len(self.destinations)]
    
class Output:
    def __init__(self):
        self.name = 'output'
        self.destinations = []
    def receive_signal(self, source_name, signal):
        print(f' - Output received signal {signal} from "{source_name}"')
        return
    def execute_next_instructions(self, modules):
        return [0, 0]
    

class FlipFlop:
    def __init__(self, name, destinations):
        self.state = 'off'
        self.name = name
        self.type = 'flipflop'
        self.destinations = destinations # [name]
        self.next_instructions = [] # [[name, signal]]

    def __str__(self):
        return f'type: flipflop, name: {self.name}, sate: {self.state}, destinations: {self.destinations}, next_instructions: {self.next_instructions}'
    
    def get_state(self):
        return self.state
    
    def receive_signal(self, source_name, signal):
        # print(f'- Received signal {signal} at FlipFlop {self.name}')
        if signal == 'low':
            if self.state == 'off':
                self.state = 'on'
                self.set_next_instruction('high')
                # print(f'- - new state is {self.state}')
            else:
                self.state = 'off'
                self.set_next_instruction('low')
                # print(f'- - new state is {self.state}')

    def set_next_instruction(self, signal):
        for d in self.destinations:
            self.next_instructions.append([d, signal])

    def has_pending(self):
        if len(self.next_instructions) >= 0:
            return True
        else:
            return False
    
    def execute_next_instructions(self, modules):
        highs = 0
        lows = 0
        # if self.state == 'on':
        if len(self.next_instructions) > 0:
            for next in self.next_instructions:
                modules[next[0]].receive_signal(self.name, next[1])
                if next[1] == 'high':
                    highs +=1
                else:
                    lows +=1
            self.next_instructions = []
        return [highs, lows]

class Conjunction:
    def __init__(self, name, destinations):
        self.name = name
        self.type = 'conjunction'
        self.inputs = [] # [name: string, state: string(defaults to low)]
        self.destinations = destinations # [name]
        self.has_pending = False
    
    def __str__(self):
        return f'type: conjunction, name: {self.name}, signal: {self.get_result_signal()} , destinations: {self.destinations}, has_pending: {self.has_pending}'

    def get_result_signal(self):
        result_signal = 'low'
        for input in self.inputs:
            if input[1] == 'low':
                result_signal = 'high'
        return result_signal
    
    def get_state(self):
        return self.get_result_signal()

    def receive_signal(self, source_name, signal):
        updated = False
        # updating input signal
        for input in self.inputs:
            if input[0] == source_name:
                input[1] == signal
                updated = True
        
        if updated == False:
            self.inputs.append([source_name, signal])

        self.has_pending = True
    
    def execute_next_instructions(self, modules):
        highs = 0
        lows = 0
        if self.has_pending == True:
            for d in self.destinations:
                modules[d].receive_signal(self.name, self.get_result_signal())
                if (self.get_result_signal() == 'high'):
                    highs += 1
                else:
                    lows +=1
            self.has_pending = False
        return [highs, lows]


################################ EXECUTION

broad_map = get_broadcaster(lines)
print('broadcaster_map')
print(broad_map)

modules_map = get_modules(lines)
# print('modules_map')
# print(modules_map)

modules = {}
for name in modules_map:
    t = modules_map[name]
    if t['type'] == '%':
        modules[name] = FlipFlop(name, modules_map[name]['destinations'])
    else:
        modules[name] = Conjunction(name, modules_map[name]['destinations'])
modules['output'] = Output()
modules['rx'] = Output()
# print('a state before')
# print(modules['a'])
        
broad = Broadcaster(broad_map['destinations'])
# broad.press_button(modules)

# print('a state after')
# print(modules['a'])
highs = 0
lows = 0
clock = 100000
queue = broad.destinations
s1 = broad.press_button(modules)
highs += s1[0]
lows += s1[1]
# print('s1')
# print(s1)

for i in range(0, clock):
    print(f'CLOCK: {i}')
    print(f'queue')
    print(queue)
    new_queue = []
    for name in queue:
        for module_name in modules:
            if module_name == name:
                # print(modules[module_name])
                sx = modules[module_name].execute_next_instructions(modules)
                # print('sx')
                # print(sx)
                highs += sx[0]
                lows += sx[1]
                dest = modules[module_name].destinations
                for d in dest:
                    if d not in new_queue:
                        new_queue.append(d)
    queue = copy.deepcopy(new_queue)
    print(f'HIGHS AND LOWS: {highs}, {lows}')

