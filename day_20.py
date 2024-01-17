# --- Day 20: Pulse Propagation ---
# With your help, the Elves manage to find the right parts and fix all of the machines. Now, they just need to send the command to boot up the machines and get the sand flowing again.

# The machines are far apart and wired together with long cables. The cables don't connect to the machines directly, but rather to communication modules attached to the machines that perform various initialization tasks and also act as communication relays.

# Modules communicate using pulses. Each pulse is either a high pulse or a low pulse. When a module sends a pulse, it sends that type of pulse to each module in its list of destination modules.

# There are several different types of modules:

# Flip-flop modules (prefix %) are either on or off; they are initially off. If a flip-flop module receives a high pulse, it is ignored and nothing happens. However, if a flip-flop module receives a low pulse, it flips between on and off. If it was off, it turns on and sends a high pulse. If it was on, it turns off and sends a low pulse.

# Conjunction modules (prefix &) remember the type of the most recent pulse received from each of their connected input modules; they initially default to remembering a low pulse for each input. When a pulse is received, the conjunction module first updates its memory for that input. Then, if it remembers high pulses for all inputs, it sends a low pulse; otherwise, it sends a high pulse.

# There is a single broadcast module (named broadcaster). When it receives a pulse, it sends the same pulse to all of its destination modules.

# Here at Desert Machine Headquarters, there is a module with a single button on it called, aptly, the button module. When you push the button, a single low pulse is sent directly to the broadcaster module.

# After pushing the button, you must wait until all pulses have been delivered and fully handled before pushing it again. Never push the button if modules are still processing pulses.

# Pulses are always processed in the order they are sent. So, if a pulse is sent to modules a, b, and c, and then module a processes its pulse and sends more pulses, the pulses sent to modules b and c would have to be handled first.

# The module configuration (your puzzle input) lists each module. The name of the module is preceded by a symbol identifying its type, if any. The name is then followed by an arrow and a list of its destination modules. For example:

# broadcaster -> a, b, c
# %a -> b
# %b -> c
# %c -> inv
# &inv -> a
# In this module configuration, the broadcaster has three destination modules named a, b, and c. Each of these modules is a flip-flop module (as indicated by the % prefix). a outputs to b which outputs to c which outputs to another module named inv. inv is a conjunction module (as indicated by the & prefix) which, because it has only one input, acts like an inverter (it sends the opposite of the pulse type it receives); it outputs to a.

# By pushing the button once, the following pulses are sent:

# button -low-> broadcaster
# broadcaster -low-> a
# broadcaster -low-> b
# broadcaster -low-> c
# a -high-> b
# b -high-> c
# c -high-> inv
# inv -low-> a
# a -low-> b
# b -low-> c
# c -low-> inv
# inv -high-> a
# After this sequence, the flip-flop modules all end up off, so pushing the button again repeats the same sequence.

# Here's a more interesting example:

# broadcaster -> a
# %a -> inv, con
# &inv -> b
# %b -> con
# &con -> output
# This module configuration includes the broadcaster, two flip-flops (named a and b), a single-input conjunction module (inv), a multi-input conjunction module (con), and an untyped module named output (for testing purposes). The multi-input conjunction module con watches the two flip-flop modules and, if they're both on, sends a low pulse to the output module.

# Here's what happens if you push the button once:

# button -low-> broadcaster
# broadcaster -low-> a
# a -high-> inv
# a -high-> con
# inv -low-> b
# con -high-> output
# b -high-> con
# con -low-> output
# Both flip-flops turn on and a low pulse is sent to output! However, now that both flip-flops are on and con remembers a high pulse from each of its two inputs, pushing the button a second time does something different:

# button -low-> broadcaster
# broadcaster -low-> a
# a -low-> inv
# a -low-> con
# inv -high-> b
# con -high-> output
# Flip-flop a turns off! Now, con remembers a low pulse from module a, and so it sends only a high pulse to output.

# Push the button a third time:

# button -low-> broadcaster
# broadcaster -low-> a
# a -high-> inv
# a -high-> con
# inv -low-> b
# con -low-> output
# b -low-> con
# con -high-> output
# This time, flip-flop a turns on, then flip-flop b turns off. However, before b can turn off, the pulse sent to con is handled first, so it briefly remembers all high pulses for its inputs and sends a low pulse to output. After that, flip-flop b turns off, which causes con to update its state and send a high pulse to output.

# Finally, with a on and b off, push the button a fourth time:

# button -low-> broadcaster
# broadcaster -low-> a
# a -low-> inv
# a -low-> con
# inv -high-> b
# con -high-> output
# This completes the cycle: a turns off, causing con to remember only low pulses and restoring all modules to their original states.

# To get the cables warmed up, the Elves have pushed the button 1000 times. How many pulses got sent as a result (including the pulses sent by the button itself)?

# In the first example, the same thing happens every time the button is pushed: 8 low pulses and 4 high pulses are sent. So, after pushing the button 1000 times, 8000 low pulses and 4000 high pulses are sent. Multiplying these together gives 32000000.

# In the second example, after pushing the button 1000 times, 4250 low pulses and 2750 high pulses are sent. Multiplying these together gives 11687500.

# Consult your module configuration; determine the number of low pulses and high pulses that would be sent after pushing the button 1000 times, waiting for all pulses to be fully handled after each push of the button. What do you get if you multiply the total number of low pulses sent by the total number of high pulses sent?

# Your puzzle answer was 806332748.

# --- Part Two ---
# The final machine responsible for moving the sand down to Island Island has a module attached named rx. The machine turns on when a single low pulse is sent to rx.

# Reset all modules to their default states. Waiting for all pulses to be fully handled after each button press, what is the fewest number of button presses required to deliver a single low pulse to the module named rx?

# Your puzzle answer was 228060006554227.

import math
f = open('inputs/doc_day_20.txt')
lines = f.read()
lines = lines.splitlines()

watch_bases = [[]]
watch_outputs = ['']
watch = {}

######################### Functions
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
    ord_modules = []
    for m in r_modules:
        fm = format_module(m)
        modules[fm['name']] = fm
        ord_modules.append(fm['name'])
    return modules

def get_all_modules(lines):
    broad_map = get_broadcaster(lines)
    modules_map = get_modules(lines)

    modules = {}
    for name in modules_map:
        t = modules_map[name]
        if t['type'] == '%':
            modules[name] = FlipFlop(name, modules_map[name]['destinations'])
        else:
            modules[name] = Conjunction(name, modules_map[name]['destinations'])
    modules['output'] = Output('output', [[m, 'low'] for m in modules if 'output' in modules[m].get_destinations()])
    modules['rx'] = Output('rx', [[m,'low'] for m in modules if 'rx' in modules[m].get_destinations()])
    for name in modules:
        if modules[name].get_type() == 'conjunction':
            for n in modules:
                if modules[n].get_type() in ['flipflop', 'conjunction']:
                    if name in modules[n].get_destinations():
                        modules[name].add_input(n, 'low')
            
    broad = Broadcaster(broad_map['destinations'])
    button = Button()
    return button, broad, modules



######################### Utils

def print_signal(type, source, destination, signal):
    # print(f'{type}{source} -{signal}-> {destination}')
    return

######################### Classes

class Button():
    def press(self, broadcaster, modules):
        print_signal('', 'button', 'broadcaster', 'low')
        h,l = broadcaster.press_button(modules)
        return h, l+1

class Broadcaster:
    def __init__(self, destinations):
        self.destinations = destinations
    
    def get_destinations(self):
        return self.destinations
    
    def press_button(self, modules):
        highs, lows= 0,0
        for d in self.destinations:
            print_signal('', 'broadcaster', d, 'low')
            modules[d].receive_signal(d, 'low', modules)
            lows+=1
        return highs, lows
    
class Output:
    def __init__(self, name, inputs):
        self.name = name
        self.inputs = inputs
        self.type = 'output'
    
    def get_type(self):
        return self.type

    def get_inputs(self):
        return self.inputs
    
    def get_destinations(self):
        return []

    def receive_signal(self, source_name, signal, modules):
        return
    
    def execute_next_instructions(self, modules, new_queue, step):
        return 0,0
    
    def pending(self):
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
    
    def get_type(self):
        return self.type

    def get_destinations(self):
        return self.destinations
    
    def receive_signal(self, source_name, signal, modules):
        if signal == 'low':
            if self.state == 'off':
                self.state = 'on'
                self.set_next_instruction('high')
            else:
                self.state = 'off'
                self.set_next_instruction('low')


    def set_next_instruction(self, signal):
        for d in self.destinations:
            self.next_instructions.append([d, signal])

    def pending(self):
        if len(self.next_instructions) > 0:
            return True
        else:
            return False
    
    def execute_next_instructions(self, modules, new_queue, step):
        highs = 0
        lows = 0
        if len(self.next_instructions) > 0:
            for next in self.next_instructions:
                print_signal('%', self.name, next[0], next[1])
                modules[next[0]].receive_signal(self.name, next[1], modules)
                if next[1] == 'high':
                    highs +=1
                else:
                    lows +=1
                new_queue.append(next[0])
            self.next_instructions = []
        return highs, lows

class Conjunction: # &
    def __init__(self, name, destinations):
        self.name = name
        self.type = 'conjunction'
        self.inputs = [] 
        self.destinations = destinations
        self.repetitions = 0
        self.has_pending = False
    
    def __str__(self):
        return f'type: conjunction, name: {self.name}, signal: {self.get_result_signal()} , inputs {self.inputs}, destinations: {self.destinations}, has_pending: {self.has_pending}'

    def get_type(self):
        return self.type

    def add_input(self, name, signal):
        self.inputs.append([name, signal])

    def get_inputs(self):
        return self.inputs
    
    def get_destinations(self):
        return self.destinations

    def get_result_signal(self):
        result_signal = 'low'
        for input in self.inputs:
            if input[1] == 'low':
                result_signal = 'high'
        if len(self.inputs) == 0:
            result_signal = 'high'
        return result_signal

    def update_input_state(self, input_name, next_signal):
        for i in self.inputs:
            if i[0] == input_name:
                i[1] = next_signal
    
    def pending(self):
        return self.has_pending

    def receive_signal(self, source_name, signal, modules):
        for input in self.inputs:
            if input[0] == source_name:
                input[1] = signal

        self.has_pending = True
        self.repetitions+=1

    def execute_next_instructions(self, modules, new_queue, step):

        highs = 0
        lows = 0
        for _ in range(self.repetitions):
            if self.has_pending == True:
                for d in self.destinations:
                    r_signal = self.get_result_signal()
                    print_signal('&', self.name, d, r_signal)
                    modules[d].receive_signal(self.name, r_signal, modules)
                    if (r_signal == 'high'):
                        highs += 1
                        # Next if will execute only in part 2
                        if(self.name in watch_bases[0]  and self.name not in watch and d == watch_outputs[0]):
                            watch[self.name] = step
                    else:
                        lows += 1
                    new_queue.append(d)
        self.has_pending = False
        self.repetitions = 0

        return highs, lows

######################## Execution

def part_1 (lines, button_presses):
    highs, lows = 0,0
    button, broad, modules = get_all_modules(lines)
    queue = []
    for i in range(button_presses):
        # print(f'\n--------------Button press {i+1}------------')
        h,l=button.press(broad, modules)
        queue = queue+broad.get_destinations()
        highs+=h
        lows+=l
        while len(queue)>0:
            ms = queue[0]
            if (len(queue)==1):
                queue = []
            else:
                queue = queue[1:]
            add_to_queue = []
            h,l= modules[ms].execute_next_instructions(modules, add_to_queue, i+1)
            highs +=h
            lows +=l 

            queue += add_to_queue

    return highs*lows

def part_2 (lines):
    highs, lows = 0,0
    queue = []
    button, broad, modules = get_all_modules(lines)
    if 'rx' in modules:
        # Assumption 1: There is only one source to 'rx'
        conj_source = modules['rx'].get_inputs()[0][0] 
        watch_outputs[0] = conj_source
        # Assumption 3: This layer are all conjunctions. So we need to know the lcm of when they send HIGH pulses
        watch_bases[0] =[m[0] for m in modules[conj_source].get_inputs()] 
    btn_press_count = 0
    while len(watch) != len(watch_bases[0]):
        # print(f'--------------Button press {i+1}------------\t\t\t\t', end='\r')
        h,l=button.press(broad, modules)
        queue = queue+broad.get_destinations()
        highs+=h
        lows+=l
        while len(queue)>0:
            next = queue[0]
            if (len(queue)==1):
                queue = []
            else:
                queue = queue[1:]
            add_to_queue = []
            h,l= modules[next].execute_next_instructions(modules, add_to_queue, btn_press_count+1)
            highs +=h
            lows +=l 
            queue += add_to_queue
        btn_press_count+=1

    return math.prod([watch[w] for w in watch])

print(f'Solution 1: {part_1(lines, 1000)}')
print(f'Solution 2: {part_2(lines)}')

# Solution 1: 806332748
# Solution 2: 228060006554227