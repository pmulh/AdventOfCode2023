import re
import string
import numpy as np
import scipy

# with open('Day05SampleInput.txt') as f:
with open('Day05Input.txt') as f:
    data = f.read()

data = data.strip('\n').split('\n\n')
seeds = data[0].split(': ')[1].split(' ')
seeds = [int(seed) for seed in seeds]
maps = {}
# full_maps = {}
for i in range(1, len(data)):
    map_name, mappings = data[i].split(':\n')
    map_name = map_name.strip(' map')
    mappings = mappings.split('\n')
    maps[map_name] = []
    for mapping in mappings:
        dest_start, source_start, range_length = mapping.split(' ')
        maps[map_name].append({'dest_start': int(dest_start),
                               'source_start': int(source_start),
                               'range_length': int(range_length)})


def look_up_map(maps, map_name, source_num):
    for mapping in maps[map_name]:
        source_num_minus_source_start = source_num - mapping['source_start']
        if ((source_num >= mapping['source_start'])
                and (source_num_minus_source_start < mapping['range_length'])):
            dest_num = mapping['dest_start'] + source_num_minus_source_start
            return dest_num
    dest_num = source_num

    return dest_num


def track_through_maps(maps, start_num):
    map_order = ['seed-to-soil', 'soil-to-fertilizer', 'fertilizer-to-water', 'water-to-light',
                 'light-to-temperature', 'temperature-to-humidity', 'humidity-to-location']
    new_num = start_num
    for lookup_map in map_order:
        new_num = look_up_map(maps, lookup_map, new_num)

    return new_num

# Part 1
# min_location = None
# for seed in seeds:
#     start_location = track_through_maps(maps, seed)
#     if (min_location is None) or (start_location < min_location):
#         min_location = start_location
# print(min_location)

# Part 2
min_location = None
for i in range(0, len(seeds), 2):
    for j in range(seeds[i], seeds[i]+seeds[i+1]):
        seed = j
        # print(seed)
        start_location = track_through_maps(maps, seed)
        if (min_location is None) or (start_location < min_location):
            min_location = start_location
print(min_location)


