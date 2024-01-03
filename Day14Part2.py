import re
import string
import numpy as np
import scipy

# with open('Day14SampleInput.txt') as f:
# with open('Day13SampleInput2.txt') as f:
with open('Day14Input.txt') as f:
    raw_data = f.read()

raw_data = np.array([list(x) for x in raw_data.strip('\n').split('\n')])

x, y = np.where(raw_data == '#')
# fixed_rocks = [(i, j) for (i, j) in zip(x, y)]


def tilt(data, dir):
    # total_load = 0
    nrows, ncols = data.shape
    tilted_array = data.copy()

    if dir == 'N':
        outer_loop_limit = ncols
        inner_loop_limit = nrows
        direction_factor = 1
    elif dir == 'W':
        outer_loop_limit = nrows
        inner_loop_limit = ncols
        direction_factor = 1
    elif dir == 'S':
        outer_loop_limit = ncols
        inner_loop_limit = nrows
        direction_factor = -1
    elif dir == 'E':
        outer_loop_limit = nrows
        inner_loop_limit = ncols
        direction_factor = -1

    for j in range(0, outer_loop_limit):
        if dir in ['N', 'S']:
            col = data[:, j]
        else:
            col = data[j]
        fixed_rock_idxs = np.where(col == '#')[0]
        tilted_col_squashed = col[col != '.']

        # load = 0
        new_round_rock_positions = []

        if direction_factor == 1:
            start = 0
            end = len(tilted_col_squashed)
            actual_row = 0
            fixed_rock_num = 0
        else:
            start = len(tilted_col_squashed) - 1
            end = -1
            actual_row = len(col) - 1
            fixed_rock_num = len(fixed_rock_idxs) - 1

        # for i in range(0, len(tilted_col_squashed)):
        for i in range(start, end, direction_factor):
            if tilted_col_squashed[i] == '#':
                actual_row = fixed_rock_idxs[fixed_rock_num]
                fixed_rock_num += direction_factor
            else:
                # load += (outer_loop_limit - actual_row)
                new_round_rock_positions.append(actual_row)
            actual_row += direction_factor

        tilted_col = ['.' for i in range(0, inner_loop_limit)]
        for i in fixed_rock_idxs:
            tilted_col[i] = '#'
        for i in new_round_rock_positions:
            tilted_col[i] = '0'
        # print(f"Column {j}: {load=}")
        # total_load += load
        if dir in ['N', 'S']:
            tilted_array[:, j] = tilted_col
        else:
            tilted_array[j] = tilted_col
        # print(total_load)

    return tilted_array

# new_data = tilt()
new_data = raw_data.copy()

cycle_end_patterns = []
first_repetition_cycle = -1
total_cycles = 1000000000
for cycle in range(0, total_cycles):#1000000000)
    if first_repetition_cycle != -1:
        break
    # previous_cycle_end = new_data.copy()
    new_data = tilt(new_data, 'N')
    new_data = tilt(new_data, 'W')
    new_data = tilt(new_data, 'S')
    new_data = tilt(new_data, 'E')
    # if np.array_equal(new_data, previous_cycle_end):
    #     print(f"Converged after cycle {cycle}")
    #     break
    cycle_end_patterns.append(new_data.copy())
    # if first_repetition_cycle == -1:
    for i in range(0, cycle):
        for j in range(0, i):
            if np.array_equal(cycle_end_patterns[i], cycle_end_patterns[j]):
                pattern_repeat_cycle = i - j
                first_repetition_cycle = j
                break
    print('')

print(f"Pattern repeats every {pattern_repeat_cycle} cycles, starting from cycle {first_repetition_cycle}")

num_full_patterns = (total_cycles - first_repetition_cycle) // pattern_repeat_cycle
final_pattern_reset = first_repetition_cycle + (num_full_patterns * pattern_repeat_cycle)
final_pattern_equivalent_cycle = first_repetition_cycle + (total_cycles - final_pattern_reset)
final_pattern = cycle_end_patterns[final_pattern_equivalent_cycle-1].copy()

total_load = 0
for i in range(0, final_pattern.shape[0]):
    for j in range(0, final_pattern.shape[1]):
        if final_pattern[i, j] == '0':
            total_load += (final_pattern.shape[0] - i)

print(f"Total load after {total_cycles} cycles: {total_load}")
print('Done')



# pattern = patterns_arrays[0]
# nrows, ncols = pattern.shape
# potential_symmetry_row = -1
# potential_symmetry_col = -1
# for i in range(0, nrows):
#     for j in range(nrows-1, i, -1):
#         print(f"Compariing rows {i} and {j}")
#         rows_equal = all(pattern[i] == pattern[j])
#         print(rows_equal)

# print(total)