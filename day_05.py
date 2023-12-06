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



def destination(num, chunk):
    destination = num
    for range in chunk:
        if num >= range[1] and num <= range[1] +range[2]-1:
            destination = range[0] + (num - range[1])
    return destination

def destination_by_range(r, chunk):
    destinations = copy.deepcopy(range)
    for range in chunk:
        s_start = range[1]
        s_end = range[1] +range[2]-1
        d_start = range[0]

        if (r[1]>= s_start and r[1] <= s_end) or (r[0]>= s_start and r[0] <= s_end):

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

new_seeds = []
turn = 'start'
start = 0
min_location = math.inf
for i, seed in enumerate(seeds) :
    if (turn == 'start'):
        start = seed
        turn = 'range'
    elif (turn == 'range'):
        for x in range(start, start+seed, 1):
            location = getLocation(x)
            print(f'New seed {x}, its locations is {location}')
            if location < min_location:
                min_location = location
            # new_seeds.append(x)
        turn = 'start'
    else:
        n=n

print(f'Min location: {min_location}')

# turn = 'start'
# start = 0
# new_locations = []
# new_seed_locations = []getLocation
# m  = []
# for i, seed in enumerate(seeds):
#     if( i %2 == 0):
#         end = seed + seeds[i+1] -1
#         # m.append([seed, end])
#         m.append([seed, end])

# print('seeds')
# print(m)
# intersections = []
# for seed in m:        
#     for range in m:
#         if (seed[0]< range[0] and range[0]< seed[1] )or (seed[0]< range[1] and range[1]< seed[1] ):
#             intersections.append([min( range[0], seed[0]), max( range[1], seed[1]) ])

# # print('intersections')
# # print(intersections)
# n_m = []
# for ar in m:
#     n_m.append(ar[0])

# # print('starts')
# # print(n_m)
# n_m.sort()
# # print(n_m)

# ordered = []
# for c in n_m:
#     for s in m:
#         if c == s[0]:
#             ordered.append(s)

# print("ordered")
# print(ordered)
# # for seed in m:

# // CORRECT BUT LONG

# new_seeds = []
# turn = 'start'
# start = 0
# for i, seed in enumerate(seeds) :
#     if (turn == 'start'):
#         start = seed
#         turn = 'range'
#     elif (turn == 'range'):
#         for x in range(start, start+seed, 1):
#             new_seeds.append(x)
#         turn = 'start'
#     else:
#         n=n

# print('new_seeds')
# print(new_seeds)

# new_locations = []
# new_seed_locations = []
# for seed in new_seeds:
#     soil = destination(seed, seed_soil)
#     fertilizer = destination(soil, soil_fertilizer)
#     water = destination(fertilizer, fertilizer_water)
#     light = destination(water, water_light)
#     temperature = destination(light, light_temperature)
#     humidity = destination(temperature, temperature_humidity)
#     location  = destination(humidity, humidity_location)
    
#     new_locations.append(location)
#     new_seed_locations.append([seed, location])

# # print(f'conversion: {new_seed_locations}')
# print(f'Solution 2: {min(new_locations)}')


# for c in m:
#         if (seed[1]>c[0] and  seed[1]<c[1]) or (seed[0]<c[1] and  seed[0]>c[0]) :
#             x = min([seed[0], seed[1], c[0], c[1]])
#             y = max([seed[0], seed[1], c[0], c[1]])
#             print(f' Intercepts {seed} and {c}: new range {x}, {y}')

# for i, seed in enumerate(seeds) :
#     if (turn == 'start'):
#         start = seed
#         turn = 'range'
#     elif (turn == 'range'):
#         for x in range(start, start+seed, 1):
#             soil = destination(x, seed_soil)
#             fertilizer = destination(soil, soil_fertilizer)
#             water = destination(fertilizer, fertilizer_water)
#             light = destination(water, water_light)
#             temperature = destination(light, light_temperature)
#             humidity = destination(temperature, temperature_humidity)
#             location  = destination(humidity, humidity_location)
            
#             new_locations.append(location)
#             new_seed_locations.append([seed, location])
#         turn = 'start'
#     else:
#         n=n

# # print(f'conversion: {new_seed_locations}')
# print(f'Solution 2: {min(new_locations)}')



# // END OF CORRECT BUT LONG
# print(f'Solution 2: {min(locations)}')
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
    