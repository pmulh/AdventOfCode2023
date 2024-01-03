import re
import string
import numpy as np


# with open('Day10SampleInput.txt') as f:
# with open('Day10SampleInput2.txt') as f:
with open('Day10Input.txt') as f:
    data = f.read()

data = data.split('\n')[:-1]
data_arr = np.array([list(x) for x in data])
# data_arr = [list(x) for x in data]
instructions = data[0]
lines = data[2:]

# start_pos = (1, 1)
# start_shape = 'F'
start_pos = (92, 43)
start_shape = '-'

nrows = data_arr.shape[0]
ncols = data_arr.shape[1]

# Initialize
# connections = np.zeroes([5, 5])
connections = np.empty([nrows, ncols], dtype=object)
for i in range(0, nrows):
    for j in range(0, ncols):
        pipe = data_arr[i, j]

        if pipe == 'S':
            pipe = start_shape

        if pipe == '.':
            connections[i, j] = ''
            continue

        if pipe == '-':
            connection1 = (i, j+1)
            connection2 = (i, j-1)
        if pipe == '|':
            connection1 = (i+1, j)
            connection2 = (i-1, j)
        if pipe == 'L':
            connection1 = (i-1, j)
            connection2 = (i, j+1)
        if pipe == '7':
            connection1 = (i+1, j)
            connection2 = (i, j-1)
        if pipe == 'J':
            connection1 = (i-1, j)
            connection2 = (i, j-1)
        if pipe == 'F':
            connection1 = (i+1, j)
            connection2 = (i, j+1)

        if ((connection1[0] < 0) or (connection1[0] >= nrows)
                or (connection1[1] < 0) or (connection1[1] >= ncols)):
            connections[i, j] = ''
            continue
        if ((connection2[0] < 0) or (connection2[0] >= nrows)
                or (connection2[1] < 0) or (connection2[1] >= ncols)):
            connections[i, j] = ''
            continue

        connections[i, j] = (connection1, connection2)


prev_pos = start_pos
curr_pos = connections[prev_pos][0]
steps = 1
while curr_pos != start_pos:
    if connections[curr_pos][0] != prev_pos:
        prev_pos = curr_pos
        curr_pos = connections[curr_pos][0]
    else:
        prev_pos = curr_pos
        curr_pos = connections[curr_pos][1]
    steps += 1
    print(curr_pos)

print(f"Total steps: {steps}")
print(f"Max Distance: {steps // 2}")
# print(total_sum)
# print(data)




