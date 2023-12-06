#--- Day 5: If You Give A Seed A Fertilizer ---
# You take the boat and find the gardener right where you were told he would be: managing a giant "garden" that looks more to you like a farm.

# "A water source? Island Island is the water source!" You point out that Snow Island isn't receiving any water.

# "Oh, we had to stop the water because we ran out of sand to filter it with! Can't make snow with dirty water. Don't worry, I'm sure we'll get more sand soon; we only turned off the water a few days... weeks... oh no." His face sinks into a look of horrified realization.

# "I've been so busy making sure everyone here has food that I completely forgot to check why we stopped getting more sand! There's a ferry leaving soon that is headed over in that direction - it's much faster than your boat. Could you please go check it out?"

# You barely have time to agree to this request when he brings up another. "While you wait for the ferry, maybe you can help us with our food production problem. The latest Island Island Almanac just arrived and we're having trouble making sense of it."

# The almanac (your puzzle input) lists all of the seeds that need to be planted. It also lists what type of soil to use with each kind of seed, what type of fertilizer to use with each kind of soil, what type of water to use with each kind of fertilizer, and so on. Every type of seed, soil, fertilizer and so on is identified with a number, but numbers are reused by each category - that is, soil 123 and fertilizer 123 aren't necessarily related to each other.

# For example:

# seeds: 79 14 55 13

# seed-to-soil map:
# 50 98 2
# 52 50 48

# soil-to-fertilizer map:
# 0 15 37
# 37 52 2
# 39 0 15

# fertilizer-to-water map:
# 49 53 8
# 0 11 42
# 42 0 7
# 57 7 4

# water-to-light map:
# 88 18 7
# 18 25 70

# light-to-temperature map:
# 45 77 23
# 81 45 19
# 68 64 13

# temperature-to-humidity map:
# 0 69 1
# 1 0 69

# humidity-to-location map:
# 60 56 37
# 56 93 4
# The almanac starts by listing which seeds need to be planted: seeds 79, 14, 55, and 13.

# The rest of the almanac contains a list of maps which describe how to convert numbers from a source category into numbers in a destination category. That is, the section that starts with seed-to-soil map: describes how to convert a seed number (the source) to a soil number (the destination). This lets the gardener and his team know which soil to use with which seeds, which water to use with which fertilizer, and so on.

# Rather than list every source number and its corresponding destination number one by one, the maps describe entire ranges of numbers that can be converted. Each line within a map contains three numbers: the destination range start, the source range start, and the range length.

# Consider again the example seed-to-soil map:

# 50 98 2
# 52 50 48
# The first line has a destination range start of 50, a source range start of 98, and a range length of 2. This line means that the source range starts at 98 and contains two values: 98 and 99. The destination range is the same length, but it starts at 50, so its two values are 50 and 51. With this information, you know that seed number 98 corresponds to soil number 50 and that seed number 99 corresponds to soil number 51.

# The second line means that the source range starts at 50 and contains 48 values: 50, 51, ..., 96, 97. This corresponds to a destination range starting at 52 and also containing 48 values: 52, 53, ..., 98, 99. So, seed number 53 corresponds to soil number 55.

# Any source numbers that aren't mapped correspond to the same destination number. So, seed number 10 corresponds to soil number 10.

# So, the entire list of seed numbers and their corresponding soil numbers looks like this:

# seed  soil
# 0     0
# 1     1
# ...   ...
# 48    48
# 49    49
# 50    52
# 51    53
# ...   ...
# 96    98
# 97    99
# 98    50
# 99    51
# With this map, you can look up the soil number required for each initial seed number:

# Seed number 79 corresponds to soil number 81.
# Seed number 14 corresponds to soil number 14.
# Seed number 55 corresponds to soil number 57.
# Seed number 13 corresponds to soil number 13.
# The gardener and his team want to get started as soon as possible, so they'd like to know the closest location that needs a seed. Using these maps, find the lowest location number that corresponds to any of the initial seeds. To do this, you'll need to convert each seed number through other categories until you can find its corresponding location number. In this example, the corresponding types are:

# Seed 79, soil 81, fertilizer 81, water 81, light 74, temperature 78, humidity 78, location 82.
# Seed 14, soil 14, fertilizer 53, water 49, light 42, temperature 42, humidity 43, location 43.
# Seed 55, soil 57, fertilizer 57, water 53, light 46, temperature 82, humidity 82, location 86.
# Seed 13, soil 13, fertilizer 52, water 41, light 34, temperature 34, humidity 35, location 35.
# So, the lowest location number in this example is 35.

# What is the lowest location number that corresponds to any of the initial seed numbers?

# Your puzzle answer was 825516882.

# --- Part Two ---
# Everyone will starve if you only plant such a small number of seeds. Re-reading the almanac, it looks like the seeds: line actually describes ranges of seed numbers.

# The values on the initial seeds: line come in pairs. Within each pair, the first value is the start of the range and the second value is the length of the range. So, in the first line of the example above:

# seeds: 79 14 55 13
# This line describes two ranges of seed numbers to be planted in the garden. The first range starts with seed number 79 and contains 14 values: 79, 80, ..., 91, 92. The second range starts with seed number 55 and contains 13 values: 55, 56, ..., 66, 67.

# Now, rather than considering four seed numbers, you need to consider a total of 27 seed numbers.

# In the above example, the lowest location number can be obtained from seed number 82, which corresponds to soil 84, fertilizer 84, water 84, light 77, temperature 45, humidity 46, and location 46. So, the lowest location number is 46.

# Consider all of the initial seed numbers listed in the ranges on the first line of the almanac. What is the lowest location number that corresponds to any of the initial seed numbers?

# Your puzzle answer was 136096660.

import math
f = open('inputs/doc_day_05.txt')
lines = f.read()
lines = lines.splitlines()
# print(lines)

seeds = ''
step = ''

seed_soil = []
soil_fertilizer = []
fertilizer_water = []
water_light = []
light_temperature = []
temperature_humidity = []
humidity_location = []
n = 1

for i, line in enumerate(lines):
    if i== 0 :
        seeds = [int(x) for x in line.split(":")[1].strip().split(' ')]
    elif line == "":
        n=n
    elif line == 'seed-to-soil map:':
        step = 'soil'
    elif line == 'soil-to-fertilizer map:':
        step = 'fertilizer'
    elif line == 'fertilizer-to-water map:':
        step = 'water'
    elif line == 'water-to-light map:':
        step = 'light'
    elif line == 'light-to-temperature map:':
        step = 'temperature'
    elif line == 'temperature-to-humidity map:':
        step = 'humidity'
    elif line == 'humidity-to-location map:':
        step = 'location'
    else:
        if step == 'soil':
            seed_soil.append( [int(x) for x in line.strip().split(' ')])
        elif step == 'fertilizer':
            soil_fertilizer.append([int(x) for x in line.strip().split(' ')])
        elif step == 'water':
            fertilizer_water.append([int(x) for x in line.strip().split(' ')])
        elif step == 'light':
            water_light.append([int(x) for x in line.strip().split(' ')])
        elif step == 'temperature':
            light_temperature.append([int(x) for x in line.strip().split(' ')])
        elif step == 'humidity':
            temperature_humidity.append([int(x) for x in line.strip().split(' ')])
        elif step == 'location':
            humidity_location.append([int(x) for x in line.strip().split(' ')])

# print('seeds')
# print(seeds)



# print(f'seed_soil:')
# print(seed_soil)
# print(f'soil_fertilizer:')
# print(soil_fertilizer)
# print(f'fertilizer_water:')
# print(fertilizer_water)
# print(f'water_light:')
# print(water_light)
# print(f'light_temperature:')
# print(light_temperature)
# print(f'temperature_humidity:')
# print(temperature_humidity)
# print(f'humidity_location:')
# print(humidity_location)

def destination(num, chunk):
    destination = num
    for range in chunk:
        if num >= range[1] and num <= range[1] +range[2]-1:
            destination = range[0] + (num - range[1])
    return destination

def getLocation(seed):
    soil = destination(seed, seed_soil)
    fertilizer = destination(soil, soil_fertilizer)
    water = destination(fertilizer, fertilizer_water)
    light = destination(water, water_light)
    temperature = destination(light, light_temperature)
    humidity = destination(temperature, temperature_humidity)
    return destination(humidity, humidity_location)

seed_locations = []
locations = []
for seed in seeds:
    location = getLocation(seed)
    locations.append(location)
    seed_locations.append([seed, location])
    # print(f'Location for seed {seed} is {location}')

# print(f'conversion: {seed_locations}')
print(f'Solution 1: {min(locations)}')

###########################################################################################################


new_seeds = []
turn = 'start'
start = 0
min_location = math.inf
for i, seed in enumerate(seeds) :
    if (turn == 'start'):
        start = seed
        turn = 'range'
    elif (turn == 'range'):
        turn = 'start'
        new_seeds.append([start, start+seed-1])
    else:
        n=n

# print('new seeds')
# print(new_seeds)

sum = 0
for l in new_seeds:
    sum = sum + l[1]-l[0]+1
# print(f'Original seed count: {sum}')

def get_ranges_from_map(map):
    ranges = []
    for m in map:
        ranges.append([m[1], m[1]+m[2]-1])
    return ranges

# print(f'seed_soil:')
# print(get_ranges_from_map(seed_soil))
# print(f'soil_fertilizer:')
# print(get_ranges_from_map(soil_fertilizer))
# print(f'fertilizer_water:')
# print(get_ranges_from_map(fertilizer_water))
# print(f'water_light:')
# print(get_ranges_from_map(water_light))
# print(f'light_temperature:')
# print(get_ranges_from_map(light_temperature))
# print(f'temperature_humidity:')
# print(get_ranges_from_map(temperature_humidity))
# print(f'humidity_location:')
# print(get_ranges_from_map(humidity_location))

 
def get_intersection(range, dest):
    new_ranges = []

    # range inside dest
    if ((dest[0] <= range[0] and range[0] <= dest[1])and (dest[0] <= range[1] and range[1] <= dest[1])):
        # new_ranges.append([dest[0], range[0]-1])
        new_ranges.append(range)
        # new_ranges.append([range[1]+1, dest[1]])
    # range is in right of dest
    elif ( (dest[0] <= range[0] and range[0] <= dest[1]) ):
        # new_ranges.append([dest[0], range[0]-1])
        new_ranges.append([range[0], dest[1]])
        new_ranges.append([dest[1]+1, range[1]])

    # range is in left of dest
    elif ( (dest[0] <= range[1] and range[1] <= dest[1]) ):
        new_ranges.append([range[0], dest[0]-1])
        new_ranges.append([dest[0], range[1]])
        # new_ranges.append([range[1]+1, dest[1]])

    # range larger that dest
    elif (range[0]<= dest[0] and dest[1]<= range[1]):
        new_ranges.append([range[0],dest[0]-1])
        new_ranges.append(dest)
        new_ranges.append([dest[1]+1,range[1]])
    
    # range outside dest
    else:
        new_ranges.append(range)

    return new_ranges

def expand(list, position, new_elements):
    list[position:position+1] = new_elements

## Modify ranges praring it for its destination
def prepare_ranges(origin, destination):
    # print('original ranges:')
    # print(origin)
    i = 0
    while i < len(origin):
        updated=False
        for dest in destination:
            # print(f'i: {i}')
            new_ranges = get_intersection(origin[i], dest)
            # print(f'- Looking for range {origin[i]} in dest {dest}')
            if(len(new_ranges)>1):
                expand(origin, i, new_ranges)
                updated = True
                # print(f'- - Intersections found: {new_ranges}')
                # print(f'- - New origin: {origin}')
            # else:
                # print(f'- - No itersections found.')
                # print(f'- - Kept origin: {origin}')
        if updated == False: 
            i = i +1
    # print('new ranges:')
    # print(origin)

# seed = [start , end]
def destinationByRange(seed, chunk):
    destination1 = seed[0]
    destination2 = seed[1]
    for range in chunk:
        if seed[0] >= range[1] and seed[0] <= range[1] +range[2]-1:
            destination1 = range[0] + (seed[0] - range[1])
        if seed[1] >= range[1] and seed[1] <= range[1] +range[2]-1:
            destination2 = range[0] + (seed[1] - range[1])
    return [destination1, destination2]

# seeds = [start, end]
def getLocation(seed):
    
    soil = destinationByRange(seed, seed_soil)
    fertilizer = destinationByRange(soil, soil_fertilizer)
    water = destinationByRange(fertilizer, fertilizer_water)
    light = destinationByRange(water, water_light)
    temperature = destinationByRange(light, light_temperature)
    humidity = destinationByRange(temperature, temperature_humidity)
    return destinationByRange(humidity, humidity_location)

def getLocationByRanges(seeds):
    prepare_ranges(seeds, get_ranges_from_map(seed_soil))
    convert = []
    for seed in seeds:
        convert.append(destinationByRange(seed, seed_soil))
    seeds = convert

    prepare_ranges(seeds, get_ranges_from_map(soil_fertilizer))
    convert = []
    for seed in seeds:
        convert.append(destinationByRange(seed, soil_fertilizer))
    seeds = convert

    prepare_ranges(seeds, get_ranges_from_map(fertilizer_water))
    convert = []
    for seed in seeds:
        convert.append(destinationByRange(seed, fertilizer_water))
    seeds = convert

    prepare_ranges(seeds, get_ranges_from_map(water_light))
    convert = []
    for seed in seeds:
        convert.append(destinationByRange(seed, water_light))
    seeds = convert

    prepare_ranges(seeds, get_ranges_from_map(light_temperature))
    convert = []
    for seed in seeds:
        convert.append(destinationByRange(seed, light_temperature))
    seeds = convert

    prepare_ranges(seeds, get_ranges_from_map(temperature_humidity))
    convert = []
    for seed in seeds:
        convert.append(destinationByRange(seed, temperature_humidity))
    seeds = convert

    prepare_ranges(seeds, get_ranges_from_map(humidity_location))
    convert = []
    for seed in seeds:
        convert.append(destinationByRange(seed, humidity_location))
    seeds = convert

    # print('output')
    # print(seeds)
    return seeds
    
locations = getLocationByRanges(new_seeds)
# print('output')
# print(locations)

min = math.inf
sum = 0
for l in locations:
    sum = sum + l[1]-l[0]+1
    if l[0] < min:
        min = l[0]
# print(f'seeds count: {sum}')
print(f'Solution 2: {min}')

# Solution 1: 825516882
# Solution 2: 136096660