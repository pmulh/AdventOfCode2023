import re
import string
import numpy as np
import scipy

with open('Day14SampleInput.txt') as f:
# with open('Day13SampleInput2.txt') as f:
# with open('Day14Input.txt') as f:
    data = f.read()

data = np.array([list(x) for x in data.strip('\n').split('\n')])

x, y = np.where(data == '#')
# fixed_rocks = [(i, j) for (i, j) in zip(x, y)]

nrows, ncols = data.shape

total_load = 0
for j in range(0, ncols):
    col = data[:, j]
    fixed_rock_idxs = np.where(col == '#')[0]
    tilted_col = col[col != '.']

    actual_row = 0
    fixed_rock_num = 0
    load = 0
    for i in range(0, len(tilted_col)):
        if tilted_col[i] == '#':
            actual_row = fixed_rock_idxs[fixed_rock_num]
            fixed_rock_num += 1
        else:
            load += (ncols - actual_row)
            print(load)
        actual_row += 1

    print(f"Column {j}: {load=}")
    total_load += load
    print(total_load)




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