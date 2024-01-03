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

nrows_orig = data_arr.shape[0]
ncols_orig = data_arr.shape[1]

expanded_data_list = []
for i in range(0, nrows_orig):
    expanded_data_list.append(data_arr[i])
    # Duplicate empty rows
    if '#' not in data_arr[i]:
        expanded_data_list.append(data_arr[i])
expanded_data_arr = np.array(expanded_data_list)

expanded_data_list = []
for j in range(0, ncols_orig):
    # expanded_data_list.append(np.transpose(expanded_data_arr[j]))
    expanded_data_list.append(expanded_data_arr[:, j])
    # Duplicate empty rows
    # if '#' not in np.transpose(expanded_data_arr[j]):
    if '#' not in expanded_data_arr[:, j]:
        # expanded_data_list.append(np.transpose(expanded_data_arr[j]))
        expanded_data_list.append(expanded_data_arr[:, j])
expanded_data_arr = np.array(expanded_data_list)
expanded_data_arr = np.transpose(expanded_data_arr)

nrows_new = expanded_data_arr.shape[0]
ncols_new = expanded_data_arr.shape[1]
galaxies = {}
galaxy_num = 1
for i in range(0, nrows_new):
    for j in range(0, ncols_new):
        if expanded_data_arr[i, j] == '#':
            galaxies[galaxy_num] = (i, j)
            galaxy_num += 1

total_distance = 0
for gal_i in range(1, len(galaxies)+1):
    for gal_j in range(gal_i, len(galaxies)+1):
        distance = abs(galaxies[gal_i][0] - galaxies[gal_j][0]) + abs(galaxies[gal_i][1] - galaxies[gal_j][1])
        print(f"{gal_i} - {gal_j}: {distance}")
        total_distance += distance

print(total_distance)
print('')


