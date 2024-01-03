import re
import string
import numpy as np
import scipy

# with open('Day11SampleInput.txt') as f:
# with open('Day10SampleInput2.txt') as f:
with open('Day11Input.txt') as f:
    data = f.read()

data = data.split('\n')[:-1]
data_arr = np.array([list(x) for x in data])
# data_arr = [list(x) for x in data]
instructions = data[0]
lines = data[2:]

nrows = data_arr.shape[0]
ncols = data_arr.shape[1]

empty_rows = []
for i in range(0, nrows):
    if '#' not in data_arr[i]:
        empty_rows.append(i)

empty_cols = []
for j in range(0, ncols):
    if '#' not in data_arr[:, j]:
        empty_cols.append(j)
# expanded_data_list = []
# for i in range(0, nrows_orig):
#     expanded_data_list.append(data_arr[i])
#     # Duplicate empty rows
#     if '#' not in data_arr[i]:
#         expanded_data_list.append(data_arr[i])
# expanded_data_arr = np.array(expanded_data_list)
#
# expanded_data_list = []
# for j in range(0, ncols_orig):
#     # expanded_data_list.append(np.transpose(expanded_data_arr[j]))
#     expanded_data_list.append(expanded_data_arr[:, j])
#     # Duplicate empty rows
#     # if '#' not in np.transpose(expanded_data_arr[j]):
#     if '#' not in expanded_data_arr[:, j]:
#         # expanded_data_list.append(np.transpose(expanded_data_arr[j]))
#         expanded_data_list.append(expanded_data_arr[:, j])
# expanded_data_arr = np.array(expanded_data_list)
# expanded_data_arr = np.transpose(expanded_data_arr)


galaxies = {}
galaxy_num = 1
for i in range(0, nrows):
    for j in range(0, ncols):
        if data_arr[i, j] == '#':
            galaxies[galaxy_num] = (i, j)
            galaxy_num += 1

total_distance = 0
for gal_i in range(1, len(galaxies)+1):
    for gal_j in range(gal_i, len(galaxies)+1):
        distance = abs(galaxies[gal_i][0] - galaxies[gal_j][0]) + abs(galaxies[gal_i][1] - galaxies[gal_j][1])
        print(f"{gal_i} - {gal_j}: {distance}")
        # Work out how many empty rows and cols we need to cross to get from gal_i to gal_j
        empty_row_crossings = len([x for x in np.arange(min(galaxies[gal_i][0], galaxies[gal_j][0]),
                                                        max(galaxies[gal_i][0], galaxies[gal_j][0])) if x in empty_rows])
        empty_col_crossings = len([x for x in np.arange(min(galaxies[gal_i][1], galaxies[gal_j][1]),
                                                        max(galaxies[gal_i][1], galaxies[gal_j][1])) if x in empty_cols])

        total_distance += distance + (empty_row_crossings + empty_col_crossings) * 999999

print(total_distance)
print('')


