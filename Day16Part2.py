import re
import string
import numpy as np
import scipy

# with open('Day16SampleInput.txt') as f:
with open('Day16Input.txt') as f:
    data = f.read()

# data = data.strip('\n').split(',')#np.array([list(x) for x in data.strip('\n').split('\n')])
data = np.array([list(x) for x in data.strip('\n').split('\n')])
nrows, ncols = data.shape


def make_beam_path(start_conditions, energized_pos_list, already_checked_new_beams):
    curr_pos = start_conditions['start_pos']
    direction = start_conditions['direction']
    new_beams_temp = []
    this_path = []

    # i = 0
    while {'pos': curr_pos, 'direction': direction} not in this_path:#True:
        this_path.append({'pos': curr_pos, 'direction': direction})
        # i+=1
        # if i%100 == 0:
        #     print(i)
        # print(curr_pos)
        energized_pos_list.append(curr_pos)
        # print(f"{curr_pos=} in this_path: {curr_pos in this_path})
        # if curr_pos in this_path:
        #     break
        # print(len(this_path))
        # Work out the next direction
        curr_pos_type = data[curr_pos]
        if curr_pos_type == '/':
            if direction == 'E':
                direction = 'N'
            elif direction == 'W':
                direction = 'S'
            elif direction == 'N':
                direction = 'E'
            else:
                direction = 'W'
        elif curr_pos_type == '\\':
            if direction == 'E':
                direction = 'S'
            elif direction == 'W':
                direction = 'N'
            elif direction == 'N':
                direction = 'W'
            else:
                direction = 'E'
        elif curr_pos_type == '-':
            if direction in ['E', 'W']:
                direction = direction
            else:
                # TODO: Need to create a new beam with direction 'W'
                direction = 'E'
                if {'start_pos': curr_pos, 'direction': 'W'} not in already_checked_new_beams:
                    new_beams_temp.append({'start_pos': curr_pos, 'direction': 'W'})
        elif curr_pos_type == '|':
            if direction in ['N', 'S']:
                direction = direction
            else:
                # TODO: Need to create a new beam with direction 'N'
                direction = 'S'
                if {'start_pos': curr_pos, 'direction': 'N'} not in already_checked_new_beams:
                    new_beams_temp.append({'start_pos': curr_pos, 'direction': 'N'})

        # Work out the next position
        if direction == 'N':
            next_pos = (curr_pos[0] - 1, curr_pos[1])
        elif direction == 'S':
            next_pos = (curr_pos[0] + 1, curr_pos[1])
        elif direction == 'W':
            next_pos = (curr_pos[0], curr_pos[1] - 1)
        elif direction == 'E':
            next_pos = (curr_pos[0], curr_pos[1] + 1)

        # print('hi2')
        if (next_pos[0] < 0) or (next_pos[0] >= nrows):
            # print('out of array')
            break
            # return new_beams_temp, energized_pos_list, checked_new_beams
        if (next_pos[1] < 0) or (next_pos[1] >= ncols):
            # print('out of array')
            break
            # return new_beams_temp, energized_pos_list, checked_new_beams

        curr_pos = next_pos

    # print('hi1')
    return new_beams_temp, energized_pos_list, already_checked_new_beams


def calc_total_energized(starting_position, starting_direction):
    energized_positions = []
    new_beams = [{'start_pos': starting_position, 'direction': starting_direction}]
    checked_new_beams = []

    while len(new_beams) > 0:
        if new_beams[0] in checked_new_beams:
            new_beams.remove(new_beams[0])
            continue
        # print(f"Running make_beam_path for {new_beams[0]}")
        x, y, z = make_beam_path(new_beams[0], energized_positions, checked_new_beams)
        new_beams.extend(x)
        energized_positions.extend(y)
        if energized_positions is not None:
            energized_positions = list(set(energized_positions))
        # checked_new_beams.extend(z)
        checked_new_beams.append(new_beams[0])
        new_beams.remove(new_beams[0])
        # new_beams
        # print(len(set(energized_positions)))
        # print('')

    energized_map = data.copy()
    energized_count = 0
    for i in range(0, nrows):
        for j in range(0, ncols):
            if (i, j) in energized_positions:
                energized_map[i, j] = '#'
                energized_count += 1
            else:
                energized_map[i, j] = '.'
    print(energized_count)
    return energized_count

starting_position_energies = []
# Starting from top row
for i in range(0, ncols):
    energy = calc_total_energized((0, i), 'S')
    # key
    starting_position_energies.append(energy)
# Starting from bottom row
for i in range(0, ncols):
    energy = calc_total_energized((nrows-1, i), 'N')
    # key
    starting_position_energies.append(energy)
# Starting from first column
for i in range(0, nrows):
    energy = calc_total_energized((i, 0), 'E')
    # key
    starting_position_energies.append(energy)
# Starting from last column
for i in range(0, nrows):
    energy = calc_total_energized((ncols-1, 0), 'W')
    # key
    starting_position_energies.append(energy)

print(max(starting_position_energies))
print('hi')