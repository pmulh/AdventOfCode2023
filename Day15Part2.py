import re
import string
import numpy as np
import scipy

# with open('Day15SampleInput.txt') as f:
with open('Day15Input.txt') as f:
    data = f.read()

data = data.strip('\n').split(',')#np.array([list(x) for x in data.strip('\n').split('\n')])


def run_algorithm(input):
    value = 0

    for c in input:
        ascii_val = ord(c)
        value += ascii_val
        value = value * 17
        value = value % 256
    return value


boxes = {i: {'labels': [], 'focal_lengths': []} for i in range(0, 256)}



total = 0
for step in data:
    if '-' in step:
        label, focal_length = step.split('-')
        action = 'remove'
    else:
        label, focal_length = step.split('=')
        action = 'add'
    box_num = run_algorithm(label)

    if action == 'add':
        if label not in boxes[box_num]['labels']:
            boxes[box_num]['labels'].append(label)
            boxes[box_num]['focal_lengths'].append(int(focal_length))
        else:
            # If label already in box, we need to update the focal lengths for that label
            replacement_idxs = [index for (index, curr_label) in enumerate(boxes[box_num]['labels']) if curr_label == label]
            for idx in replacement_idxs:
                boxes[box_num]['focal_lengths'][idx] = int(focal_length)

    if action == 'remove':
        new_labels = []
        new_focal_lengths = []
        for i in range(0, len(boxes[box_num]['labels'])):
            if boxes[box_num]['labels'][i] != label:
                new_labels.append(boxes[box_num]['labels'][i])
                new_focal_lengths.append(boxes[box_num]['focal_lengths'][i])
        boxes[box_num]['labels'] = new_labels
        boxes[box_num]['focal_lengths'] = new_focal_lengths
        # boxes[box_num]['labels'] = [lens for lens in boxes[box_num] if lens[0] != label]
    print('')

# Calculate focusing power
total_focusing_power = 0
for box_num in boxes.keys():
    box_focusing_power = 0
    box = boxes[box_num]
    for slot_num in range(0, len(boxes[box_num]['focal_lengths'])):
        focal_length = boxes[box_num]['focal_lengths'][slot_num]
        lens_focusing_power = (box_num + 1) * (slot_num + 1) * focal_length
        # print(lens_focusing_power)
        box_focusing_power += lens_focusing_power
    total_focusing_power += box_focusing_power

print(total_focusing_power)