import re
import string
import numpy as np
import scipy

# with open('Day13SampleInput.txt') as f:
# with open('Day13SampleInput2.txt') as f:
with open('Day13Input.txt') as f:
    data = f.read()

patterns = data.strip('\n').split('\n\n')
patterns_arrays = []
for pattern in patterns:
    pattern_array = np.array([list(x) for x in pattern.split('\n')])
    patterns_arrays.append(pattern_array)

# pattern = patterns_arrays[0]
# nrows, ncols = pattern.shape
# potential_symmetry_row = -1
# potential_symmetry_col = -1
# for i in range(0, nrows):
#     for j in range(nrows-1, i, -1):
#         print(f"Compariing rows {i} and {j}")
#         rows_equal = all(pattern[i] == pattern[j])
#         print(rows_equal)

total = 0
for pattern_i in range(0, len(patterns_arrays)):
    pattern = patterns_arrays[pattern_i]
    # potential_symmetry_row = -1
    # potential_symmetry_col = -1
    symmetry_rows = []
    symmetry_cols = []
    nrows, ncols = pattern.shape
    print(f"Pattern {pattern_i} shape: {nrows}, {ncols}")

    # symmetry_rows = []
    rows_non_symmetric_totals = {}
    for i in range(1, nrows):
        rows_non_symmetric_totals[i] = 0
        # non_symmetric_total = 0
        # potential_symmetry_row = i
        # print(f"potential_symmetry_row: {potential_symmetry_row}")
        # potential_symmetry = True
        for j in range(0, nrows):
            # print(rows_non_symmetric_totals)
            row_a = i - (j+1)
            row_b = i + j
            if (row_a < 0) or (row_b >= nrows):
                # If we've got to this stage without break out of inner loop, we've found a symmetry row
                # Update for part 2 - break at end of inner loop changed to a continue, so now need
                # to have an extra check in here
                if rows_non_symmetric_totals[i] == 0:
                    symmetry_rows.append(i)
                break
            # print(f"Comparing rows {row_a} and {row_b}")
            # non_symmetric_total += sum(pattern[row_a] == pattern[row_b])
            rows_non_symmetric_totals[i] += sum(pattern[row_a] != pattern[row_b])
            # if non_symmetric_total > 0:
            if not all(pattern[row_a] == pattern[row_b]):
                # break
                continue

    # symmetry_cols = []
    cols_non_symmetric_totals = {}
    for i in range(1, ncols):
        cols_non_symmetric_totals[i] = 0
        # potential_symmetry_col = i
        # print(f"potential_symmetry_col: {potential_symmetry_col}")
        # potential_symmetry = True
        for j in range(0, ncols):
            # print(cols_non_symmetric_totals)
            col_a = i - (j+1)
            col_b = i + j
            if (col_a < 0) or (col_b >= ncols):
                # If we've got to this stage without break out of inner loop, we've found a symmetry colum
                # Update for part 2 - break at end of inner loop changed to a continue, so now need
                # to have an extra check in here
                if cols_non_symmetric_totals[i] == 0:
                    symmetry_cols.append(i)
                break
            # print(f"Comparing cols {col_a} and {col_b}")
            cols_non_symmetric_totals[i] += sum(pattern[:, col_a] != pattern[:, col_b])
            if not all(pattern[:, col_a] == pattern[:, col_b]):
                # break
                continue

    if (len(symmetry_rows) == 0) and (len(symmetry_cols) == 0):
        print("No symmetry rows or columns found!")

    # Part 1 - use whatever is in symmetry_rows or symmetry_cols from above
    print(symmetry_rows, symmetry_cols)
    # Part 2 - change the symmetry row or col by taking the ...
    symmetry_rows = [x for x in rows_non_symmetric_totals if rows_non_symmetric_totals[x] == 1]
    symmetry_cols = [x for x in cols_non_symmetric_totals if cols_non_symmetric_totals[x] == 1]
    print(symmetry_rows, symmetry_cols)

    pattern_total = 0
    for col in symmetry_cols:
        pattern_total += col
    for row in symmetry_rows:
        pattern_total += 100 * row
    if pattern_total == 0:
        print(f"{pattern_i}: HELP!")


    total += pattern_total

print(total)