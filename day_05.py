import copy
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