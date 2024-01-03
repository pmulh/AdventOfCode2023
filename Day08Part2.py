import re
import string
import numpy as np


# with open('Day8Part2SampleInput.txt') as f:
with open('Day8Input.txt') as f:
    data = f.read()

data = data.split('\n')[:-1]
instructions = data[0]
lines = data[2:]

# Construct dictionary of mappings
lookup_dict = {}
for line in lines:
    element, lr = line.split(' = ')
    # Drop brackets and separate out left and right parts
    l, r = lr[1:-1].split(', ')
    lookup_dict[element] = {}
    lookup_dict[element]['L'] = l
    lookup_dict[element]['R'] = r
    print('')

nodes_ending_in_a = []
for element in lookup_dict.keys():
    if element[-1] == 'A':
        nodes_ending_in_a.append(element)

nodes_ending_in_z = []
for element in lookup_dict.keys():
    if element[-1] == 'Z':
        nodes_ending_in_z.append(element)

def check_if_nodes_end_in_letter(node_list, letter):
    for node in node_list:
        if node[-1] != letter:
            return False
    return True

# nodes_ending_in_a: ['SLA', 'AAA', 'LVA', 'NPA', 'GDA', 'RCA']
# nodes_ending_in_z: ['RPZ', 'ZZZ', 'STZ', 'CMZ', 'SFZ', 'HKZ']

# prev_positions = ['SLA'] # 11653  #nodes_ending_in_a
# prev_positions = ['AAA'] # 19783  #nodes_ending_in_a
# prev_positions = ['LVA'] # 19241  #nodes_ending_in_a
# prev_positions = ['NPA'] # 16531  #nodes_ending_in_a
# prev_positions = ['GDA'] # 12737  #nodes_ending_in_a
prev_positions = ['RCA'] # 14363  #nodes_ending_in_a

# Code below run individually for 6 prev_positions above, giving the numbers in comments for each
# Starting on each of those positions we'll end up at a position ending in Z on multiples of these numbers
# So we'll end up on positions that all end in Z after steps = lowest common multiple of the above numbers
import math
math.lcm(11653,19783, 19241, 16531, 12737, 14363) # 9177460370549


step_count = 0
# for instruction in instructions:
prev_positions_end_in_z = False
while not prev_positions_end_in_z:
    # Modular to loop back to start of instructions if needed
    instruction = instructions[step_count % len(instructions)]
    next_positions = []
    for node in prev_positions:
        next_pos = lookup_dict[node][instruction]
        next_positions.append(next_pos)

    step_count += 1
    if step_count % 100000 == 0:
        print(f"Step {step_count}: {prev_positions} - {next_positions}")
    prev_positions = next_positions
    prev_positions_end_in_z = check_if_nodes_end_in_letter(prev_positions, 'Z')

print(f"Total steps: {step_count}")
# print(total_sum)
# print(data)




