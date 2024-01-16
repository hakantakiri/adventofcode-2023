# FLIP FLOP % starts off, recieves high ignore, recieves low inverse is current state and send high if was off, send low if was on
# low  -> %off %on send high
# high -> %off %off
# low  -> %on %off send low
# high -> %on -ignore (maybe not happing)

# CONJUCTION & remembers, start with LOW, if ALL inputs are HIGH send LOW, else sen HIGH
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

high_lows = [0,0]

class Button():
    def press(self, broadcaster, modules):
        print(f'button -low-> broadcaster')
        h,l = broadcaster.press_button(modules)
        return h, l+1


class Broadcaster:
    def __init__(self, destinations):
        self.destinations = destinations # [name]
    
    def press_button(self, modules):
        highs, lows= 0,0
        for d in self.destinations:
            print(f'broadcaster -low-> {d}')
            modules[d].receive_signal(d, 'low')
            lows+=1
        return highs, lows
    
class Output:
    def __init__(self):
        self.name = 'output'
        self.destinations = []

    def receive_signal(self, source_name, signal):
        # print(f' - Output received signal {signal} from "{source_name}"')
        return
    def execute_next_instructions(self, modules):
        return [0, 0]
    
    def pending(self):
        return False
    
    def get_state(self):
        return False
    

class FlipFlop: # %
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

    def pending(self):
        if len(self.next_instructions) > 0:
            return True
        else:
            return False
    
    def execute_next_instructions(self, modules):
        highs = 0
        lows = 0
        # if self.state == 'on':
        if len(self.next_instructions) > 0:
            for next in self.next_instructions:
                print(f'%{self.name} -{next[1]}-> {next[0]}')
                modules[next[0]].receive_signal(self.name, next[1])
                if next[1] == 'high':
                    highs +=1
                else:
                    lows +=1
            self.next_instructions = []
        return highs, lows

class Conjunction: # &
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
    
    def pending(self):
        return self.has_pending

    def receive_signal(self, source_name, signal):
        # print(f'- Received at &{self.name} signal {signal} from source {source_name}')
        updated = False
        # updating input signal
        for input in self.inputs:
            if input[0] == source_name:
                input[1] = signal
                updated = True
        
        if updated == False:
            self.inputs.append([source_name, signal])

        self.has_pending = True

        # print(f'- Updated &{self.name} inputs are {self.inputs}')   

    def execute_next_instructions(self, modules):
        highs = 0
        lows = 0
        if self.has_pending == True:
            for d in self.destinations:
                print(f'&{self.name} -{self.get_result_signal()}-> {d}')
                modules[d].receive_signal(self.name, self.get_result_signal())
                if (self.get_result_signal() == 'high'):
                    highs += 1
                else:
                    lows +=1
            self.has_pending = False
        return highs, lows


################################ EXECUTION
def part_1 (lines):
    broad_map = get_broadcaster(lines)

    modules_map = get_modules(lines)

    modules = {}
    for name in modules_map:
        t = modules_map[name]
        if t['type'] == '%':
            modules[name] = FlipFlop(name, modules_map[name]['destinations'])
        else:
            modules[name] = Conjunction(name, modules_map[name]['destinations'])
    modules['output'] = Output()
    modules['rx'] = Output()
            
    broad = Broadcaster(broad_map['destinations'])
    button = Button()

    ## Execution

    highs, lows = 0,0
    button_presses = 1000
    for i in range(0, button_presses):
        print(f'\n--------------Button press {i+1}------------')
        h,l=button.press(broad, modules)
        highs+=h
        lows+=l
        next_clock = True
        while next_clock:
            # print(f'\nCycle {i+1}')
            prev_h, prev_l = highs, lows
            ms = [m_n for m_n in modules if modules[m_n].pending()]
            # print(f'Will execute {ms}')
            for module_name in ms:
                h,l= modules[module_name].execute_next_instructions(modules)
                highs+=h
                lows+=l
            
           
            
            if( prev_h == highs and prev_l == lows):
                next_clock = False
        print(f'\nHighs: {highs}, Lows: {lows}')
        for m in modules:
            print(f'-- State of module: {m}')
            print(modules[m].get_state())



part_1(lines)

# highs = 0
# lows = 0
# clock = 10000
# queue = broad.destinations
# s1 = broad.press_button(modules)
# highs += s1[0]
# lows += s1[1]


# for i in range(0, clock):
#     print(f'CLOCK: {i}')
#     print(f'queue')
#     print(queue)
#     new_queue = []
#     for name in queue:
#         for module_name in modules:
#             if module_name == name:
#                 # print(modules[module_name])
#                 sx = modules[module_name].execute_next_instructions(modules)
#                 # print('sx')
#                 # print(sx)
#                 highs += sx[0]
#                 lows += sx[1]
#                 dest = modules[module_name].destinations
#                 for d in dest:
#                     if d not in new_queue:
#                         new_queue.append(d)
#     queue = copy.deepcopy(new_queue)
#     print(f'HIGHS AND LOWS: {highs}, {lows}')

