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


def look_up_map(maps, map_name, source_num, reverse=False):
    if not reverse:
        source = 'source_start'
        dest = 'dest_start'
    else:
        source = 'dest_start'
        dest = 'source_start'

    for mapping in maps[map_name]:
        source_num_minus_source_start = source_num - mapping[source]
        if ((source_num >= mapping[source])
                and (source_num_minus_source_start < mapping['range_length'])):
            dest_num = mapping[dest] + source_num_minus_source_start
            return dest_num
    dest_num = source_num

    return dest_num


def track_through_maps(maps, start_num, reverse=False):
    map_order = ['seed-to-soil', 'soil-to-fertilizer', 'fertilizer-to-water', 'water-to-light',
                 'light-to-temperature', 'temperature-to-humidity', 'humidity-to-location']
    if reverse:
        map_order.reverse()
    new_num = start_num
    for lookup_map in map_order:
        new_num = look_up_map(maps, lookup_map, new_num, reverse=reverse)

    return new_num


# seed_to_fert = {}
# special_mapping_seeds = []
#
# special_mapping_soils = []
# for soil_to_fert_map in maps['soil-to-fertilizer']:
#     for i in range(soil_to_fert_map['source_start'],
#                    soil_to_fert_map['source_start'] + soil_to_fert_map['range_length']):
#         special_mapping_soils.append(i)
# for seed_to_soil_map in maps['seed-to-soil']:
#     for i in range(seed_to_soil_map['dest_start'],
#                    seed_to_soil_map['dest_start']+seed_to_soil_map['range_length']):
#         special_mapping_soils.append(i)
#
# for soil_num in special_mapping_soils:
#     seed = look_up_map(maps, 'seed-to-soil', soil_num, reverse=True)
#     special_mapping_seeds.append(seed)
#     seed_to_fert[seed] = look_up_map(maps, 'soil-to-fertilizer', look_up_map(maps, 'seed-to-soil', seed))
# special_mapping_seeds.sort()
#
#
# def create_two_step_mapping(maps, source_map, intermediate_map):
#     final_map = {}
#     # special_mapping_seeds = []
#
#     special_mappings = []
#     for temp_map in maps[intermediate_map]:
#         for i in range(temp_map['source_start'],
#                        temp_map['source_start'] + temp_map['range_length']):
#             special_mappings.append(i)
#     for temp_map in maps[source_map]:
#         for i in range(temp_map['dest_start'],
#                        temp_map['dest_start'] + temp_map['range_length']):
#             special_mappings.append(i)
#
#     for temp_num in special_mappings:
#         source_num = look_up_map(maps, source_map, temp_num, reverse=True)
#         # special_mapping_seeds.append(seed)
#         final_map[source_num] = look_up_map(maps, intermediate_map, look_up_map(maps, source_map, source_num))
#     # special_mapping_seeds.sort()
#     return final_map
#
# print(i)


# Part 1
# min_location = None
# for seed in seeds:
#     start_location = track_through_maps(maps, seed)
#     if (min_location is None) or (start_location < min_location):
#         min_location = start_location
# print(min_location)

# Part 2
# actual_seed_nums = []
# for i in range(0, len(seeds), 2):
#     for j in range(seeds[i], seeds[i]+seeds[i+1]):
#         actual_seed_nums.append(j)

minimum_found = False
loop_start = maps['humidity-to-location'][0]

# Sort within each map so lowest dest_start comes first
sorted_maps = {}
for mapping in maps:
    sorted_maps[mapping] = sorted(maps[mapping], key=lambda d: d['dest_start'])

print('')
# Check if each location leads back to an actual seed in seed list
temp_map = sorted_maps['humidity-to-location'][0]
for location in range(0, temp_map['dest_start']+temp_map['range_length']):
# for location in range(temp_map['dest_start'], temp_map['dest_start'] + temp_map['range_length']):
    if minimum_found:
        break
    seed_number = track_through_maps(sorted_maps, location, reverse=True)
    # print(f"{location=}, {seed_number=}")
    for i in range(0, len(seeds), 2):
        if (seed_number >= seeds[i]) and (seed_number < (seeds[i] + seeds[i+1])):
        # if seed_number in actual_seed_nums:
            print(f"Seed {seed_number} <--> Location {location}")
            minimum_found = True
            break


# for start_location in range(0, 1000000000):
#     print(start_location)
#     if minimum_found:
#         break
#     seed_number = track_through_maps(maps, start_location, reverse=True)
#     for i in range(0, len(seeds), 2):
#         if (seed_number >= seeds[i]) and (seed_number < (seeds[i] + seeds[i+1])):
#         # if seed_number in actual_seed_nums:
#             print(f"Seed {seed_number} <--> Location {start_location}")
#             minimum_found = True
#             break
#
# print(start_location)
# min_location = None
# for i in range(0, len(seeds), 2):
#     for j in range(seeds[i], seeds[i]+seeds[i+1]):
#         seed = j
#         # print(seed)
#         start_location = track_through_maps(maps, seed)
#         if (min_location is None) or (start_location < min_location):
#             min_location = start_location
# print(min_location)


