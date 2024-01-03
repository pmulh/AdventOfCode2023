import re
import string
import numpy as np

def get_differences(x):
    """
    Returns a list of dimension len(x) - 1, with values equal to the differences between
    consecutive values in x.

    Args:
        x: A list of numbers

    Returns: A list of numbers
    """
    diffs = []
    for i in range(0, len(x)-1):
        diffs.append(x[i+1] - x[i])
    return diffs


# with open('Day9SampleInput.txt') as f:
with open('Day9Input.txt') as f:
    data=f.read()

lines = data.split('\n')[:-1]

# dataarray = []
# for line in lines:
#     dataarray.append(line)
#
# for row in range(0, len(dataarray)):
#     for col in range(0, len(dataarray[0])):
#         val = dataarray[row][col]
#         if val.isnumeric():

# line_number = 0

# Sum of extrapolated values
total_sum = 0
for line in lines:
    values = line.split(' ')
    values = [int(value) for value in values]
    # values = [np.int64(value) for value in values]
    # values = [float(value) for value in values]

    values_array = [values]

    zero_values = False

    # Iterate until values stop changing
    while not zero_values:
        values_array.append(get_differences(values_array[-1]))
        if (max(values_array[-1]) == 0) and (sum(values_array[-1]) == 0):
            zero_values = True
    num_values = len(values)

    # Extrapolate - BACKWARDS!
    # Insert new value at start of row i equal to: current value at start of row i - value at end of row i+1
    # Loop backwards through rows
    for row_num in range(len(values_array)-1, -1, -1):
        # print(row_num)
        # For final row (all zeroes), just add an extra zero on to the end
        if row_num == len(values_array) - 1:
            values_array[row_num].insert(0, 0)
            continue

        # Otherwise, append new value based on current value + value from next row
        new_value = values_array[row_num][0] - values_array[row_num+1][0]
        values_array[row_num].insert(0, new_value)

    # Add extrapolated value (first value in first element in values_array) to total
    total_sum += values_array[0][0]
    # print(line)
    # print(line)
    # print(total_sum)


print(total_sum)
# print(data)




