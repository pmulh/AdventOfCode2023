import re
import string
import numpy as np


# with open('Day8SampleInput.txt') as f:
# with open('Day8SampleInput2.txt') as f:
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

prev_pos = 'AAA'
step_count = 0
# for instruction in instructions:
while prev_pos != 'ZZZ':
    # if prev_pos == 'ZZZ':
    #     break
    # Modular to loop back to start of instructions if needed
    instruction = instructions[step_count % len(instructions)]
    next_pos = lookup_dict[prev_pos][instruction]
    step_count += 1
    print(f"Step {step_count}: {prev_pos} - {next_pos}")
    prev_pos = next_pos

print(f"Total steps: {step_count}")
# print(total_sum)
# print(data)




