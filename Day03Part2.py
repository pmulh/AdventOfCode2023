import re
import string
import numpy as np

# with open('Day3SampleInput.txt') as f:
with open('Day3Input.txt') as f:
    data=f.read()

lines = data.split('\n')[:-1]

gears = []
for line_number in range(len(lines)):
    for col in range(0, len(lines[line_number])):
        if lines[line_number][col] == '*':
            gears.append({'line': line_number, 'col': col, 'adj_numbers': []})

line_number = 0
total_sum = 0
for line in lines:
    # numbers = re.split('\.+', line)
    line_search_start_index = 0
    # Split on non-digits
    numbers = re.split('\D+', line)
    for number in numbers:
        if not number.isnumeric():
            continue
        len_num = len(number)
        # num_start_idx = line.find(number)
        # num_start_idx = re.search('[^\d]' + number + '[^\d]', line).start() + 1
        # Negative lookbehind and lookahead assertions to avoid matching e.g. '3' with '233'
        num_start_idx = re.search('(?<![\d])' + number + '(?![\d])', line[line_search_start_index:]).start() + line_search_start_index
        num_end_idx = num_start_idx + len_num - 1
        # Can't let adjacent indexes go beyond length of line
        adj_start_idx = max(num_start_idx-1, 0)
        adj_end_idx = min(num_end_idx+1, len(line)-1)
        # print(line[num_start_idx:num_end_idx])

        # Hacky fix for handling when a number appears multiple times on the same line (which breaks the regex
        # logic above for finding start and end indices)
        line_search_start_index = adj_end_idx + 1

        adjacent = ''
        if line_number != 0:
            adjacent += lines[line_number - 1][adj_start_idx:adj_end_idx+1]
        if adj_start_idx != num_start_idx:
            adjacent += line[adj_start_idx:num_start_idx]
        if adj_end_idx != num_end_idx:
            adjacent += line[adj_end_idx]
        if line_number != len(lines) - 1:
            adjacent += lines[line_number + 1][adj_start_idx:adj_end_idx+1]

        for gear in gears:
            # Check if number is adjacent to any of the gears
            if abs(line_number - gear['line']) <= 1:
                if (gear['col'] >= adj_start_idx) and (gear['col'] <= adj_end_idx):
                    gear['adj_numbers'].append(int(number))

        regexp = re.compile(r'[^.0123456789]')
        # if '*' in adjacent:
        #     print(number)
        if regexp.search(adjacent):
            # print(number)
            total_sum += int(number)
        # else:
        #     print(f"{number} doesn't count")

    line_number += 1

adjacent_gear_sum = 0
for gear in gears:
    if len(gear['adj_numbers']) == 2:
        adjacent_gear_sum += np.prod(gear['adj_numbers'])
    else:
        print(f"{gear}")

print(adjacent_gear_sum)
