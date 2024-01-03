import re
import string
import numpy as np

# Sample Input 1
# start_pos = (1, 1)
# start_shape = 'F'
# Sample Input 2
# start_pos = (4, 12)
# start_shape = 'F'
# Sample Input 3
# start_pos = (0, 4)
# start_shape = '7'
# Actual Input
start_pos = (92, 43)
start_shape = '-'

# with open('Day10Part2SampleInput.txt') as f:
# with open('Day10Part2SampleInput2.txt') as f:
# with open('Day10Part2SampleInput3.txt') as f:
with open('Day10Input.txt') as f:
    data = f.read()



data = data.split('\n')[:-1]
data_arr = np.array([list(x) for x in data])
# data_arr = [list(x) for x in data]
instructions = data[0]
lines = data[2:]


def get_initial_direction(pos, nrows, ncols):
    # Choose initial direction as the direction towards the nearest edge
    # (with a default order of up, right, down, left if there's a tie)
    distance_to_top = pos[0]
    distance_to_bottom = nrows - 1 - pos[0]
    distance_to_left = pos[1]
    distance_to_right = ncols - 1 - pos[1]

    if (pos[0] < 0) or (pos[0] > nrows-1):
        print('ERROR: Position outside of grid')
        return
    if (pos[1] < 0) or (pos[1] > ncols-1):
        print('ERROR: Position outside of grid')
        return

    distances = [distance_to_top, distance_to_right, distance_to_bottom, distance_to_left]
    min_index = min(range(len(distances)), key=distances.__getitem__)
    if min_index == 0:
        return 'U'
    if min_index == 1:
        return 'R'
    if min_index == 2:
        return 'D'
    if min_index == 3:
        return 'L'
    print('ERROR  in get_initial_direction')


def get_next_direction(direction, dir_history):
    dir_history = set(dir_history)
    all_dirs = {'U', 'D', 'L', 'R'}

    remaining_dirs = all_dirs.difference(dir_history)

    if (direction == 'U') and ('R' in remaining_dirs):
        return 'R'
    if (direction == 'R') and ('D' in remaining_dirs):
        return 'D'
    if (direction == 'D') and ('L' in remaining_dirs):
        return 'L'
    if (direction == 'L') and ('U' in remaining_dirs):
        return 'U'
    return 'HELP!'


def get_new_position(pos, direction):
    if direction == 'U':
        return (pos[0] - 1, pos[1])
    if direction == 'R':
        return (pos[0], pos[1] + 1)
    if direction == 'D':
        return (pos[0] + 1, pos[1])
    if direction == 'L':
        return (pos[0], pos[1] - 1)


def is_position_on_edge_of_grid(position, nrows, ncols):
    if (position[0] == 0) or (position[0] == nrows - 1) or (position[1] == 0) or (position[1] == ncols - 1):
        return True
    return False


nrows = data_arr.shape[0]
ncols = data_arr.shape[1]

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

main_loop_positions = []
prev_pos = start_pos
main_loop_positions.append(prev_pos)
curr_pos = connections[prev_pos][0]
main_loop_positions.append(curr_pos)
steps = 1
while curr_pos != start_pos:
    if connections[curr_pos][0] != prev_pos:
        prev_pos = curr_pos
        curr_pos = connections[curr_pos][0]
    else:
        prev_pos = curr_pos
        curr_pos = connections[curr_pos][1]
    main_loop_positions.append(curr_pos)
    steps += 1
    # print(curr_pos)

# Don't really care about start position anymore, so just replace 'S' with whatever type of pipe it really is
data_arr[start_pos] = start_shape
# Treat any pipe not on the main loop the same as ground with no pipes
for i in range(0, nrows):
    for j in range(0, ncols):
        if (i, j) not in main_loop_positions:
            data_arr[(i, j)] = '.'

# Simplified array where X represents a pipe, . represents not a pipe
pipe_arr = data_arr.copy()
# List of positions that are pipes
pipe_positions = []
# List of positions that are on the edge of the grid
edge_positions = []
for i in range(0, nrows):
    for j in range(0, ncols):
        if pipe_arr[i, j] != '.':
            pipe_arr[i, j] = 'X'
            pipe_positions.append((i, j))
        if is_position_on_edge_of_grid((i, j), nrows, ncols):
            edge_positions.append((i, j))

fine_pipe_arr = np.zeros([nrows * 3, ncols * 3])
# def subdivide_cell(pos, orig_arr, fine_arr):

for i in range(0, nrows):
    for j in range(0, ncols):
        pos = (i, j)
        # pos = (0, 1)
        fine_arr_x_start = pos[0] * 3
        fine_arr_y_start = pos[1] * 3

        if data_arr[pos] == '|':
            # '|'
            # 010
            # 010
            # 010
            fine_pipe_arr[fine_arr_x_start + 0, fine_arr_y_start + 1] = 1
            fine_pipe_arr[fine_arr_x_start + 1, fine_arr_y_start + 1] = 1
            fine_pipe_arr[fine_arr_x_start + 2, fine_arr_y_start + 1] = 1
        if data_arr[pos] == '-':
            # '-'
            # 000
            # 111
            # 000
            fine_pipe_arr[fine_arr_x_start + 1, fine_arr_y_start + 0] = 1
            fine_pipe_arr[fine_arr_x_start + 1, fine_arr_y_start + 1] = 1
            fine_pipe_arr[fine_arr_x_start + 1, fine_arr_y_start + 2] = 1
        if data_arr[pos] == 'L':
            # 'L'
            # 010
            # 011
            # 000
            fine_pipe_arr[fine_arr_x_start + 0, fine_arr_y_start + 1] = 1
            fine_pipe_arr[fine_arr_x_start + 1, fine_arr_y_start + 1] = 1
            fine_pipe_arr[fine_arr_x_start + 1, fine_arr_y_start + 2] = 1
        if data_arr[pos] == 'J':
            # 'L'
            # 010
            # 110
            # 000
            fine_pipe_arr[fine_arr_x_start + 0, fine_arr_y_start + 1] = 1
            fine_pipe_arr[fine_arr_x_start + 1, fine_arr_y_start + 0] = 1
            fine_pipe_arr[fine_arr_x_start + 1, fine_arr_y_start + 1] = 1
        if data_arr[pos] == '7':
            # '7'
            # 000
            # 110
            # 010
            fine_pipe_arr[fine_arr_x_start + 1, fine_arr_y_start + 0] = 1
            fine_pipe_arr[fine_arr_x_start + 1, fine_arr_y_start + 1] = 1
            fine_pipe_arr[fine_arr_x_start + 2, fine_arr_y_start + 1] = 1
        if data_arr[pos] == 'F':
            # 'F'
            # 000
            # 011
            # 010
            fine_pipe_arr[fine_arr_x_start + 1, fine_arr_y_start + 1] = 1
            fine_pipe_arr[fine_arr_x_start + 1, fine_arr_y_start + 2] = 1
            fine_pipe_arr[fine_arr_x_start + 2, fine_arr_y_start + 1] = 1

fine_pipe_positions = []
fine_edge_positions = []
for i in range(0, nrows * 3):
    for j in range(0, ncols * 3):
        # if fine_pipe_arr[i, j] != '.':
        #     fine_pipe_arr[i, j] = 'X'
        if fine_pipe_arr[i, j] == 1:
            fine_pipe_positions.append((i, j))
        if is_position_on_edge_of_grid((i, j), nrows*3, ncols*3):
            fine_edge_positions.append((i, j))

print('')

# direction = 'U'
# pipe_arr[6, 2]
#
# pos = (6, 2)


def is_position_enclosed(start_pos, raw_start_pos, fine_pipe_arr, non_enclosed_positions, enclosed_positions):
    fine_nrows = fine_pipe_arr.shape[0]
    fine_ncols = fine_pipe_arr.shape[1]

    # if fine_pipe_arr[start_pos] == 1:#'X':
    # if pipe_arr[raw_start_pos] == 'X':
    #     print(f"Position {start_pos} is a pipe (grid shape: {(fine_nrows, fine_ncols)})")
    #     return False

    # if is_position_on_edge_of_grid(start_pos, fine_nrows, fine_ncols):
    if is_position_on_edge_of_grid(raw_start_pos, nrows, ncols):
        # print(f"Position {start_pos} is on edge of grid (grid shape: {(fine_nrows, fine_ncols)})")
        return False

    accessible_positions = set()#{}
    checked_positions = set()#[]
    # inaccessible_positions = []
    # start_pos = (6, 2)
    for i in range(start_pos[0] - 1, start_pos[0] + 2):
        for j in range(start_pos[1] - 1, start_pos[1] + 2):
            if (i, j) not in fine_pipe_positions:
                # accessible_positions.append((i, j))
                accessible_positions.add((i, j))

    prev_num_accessible_positions = 1
    num_accessible_positions = len(accessible_positions)#len(set(accessible_positions))
    while num_accessible_positions != prev_num_accessible_positions:
        # If the edge of the grid is accessible, the start position mustn't be enclosed
        # Similarly, if a position we previously found could access the edge of the grid is accessible, the start
        # position mustn't be enclosed
        # if len(set(accessible_positions).intersection(fine_edge_positions)) > 0
        if ((len(accessible_positions.intersection(fine_edge_positions)) > 0)
           or (len(accessible_positions.intersection(non_enclosed_positions)) > 0)):
            # print(f"Edge of is accessible from starting position {start_pos} (grid shape: {(fine_nrows, fine_ncols)})")
            # break
            return False
            # return False

        # If one of the accessible positions has previously been deemed as enclosed, this position must also be enclosed
        if len(accessible_positions.intersection(enclosed_positions)) > 0:
            print(f"Position {start_pos} is enclosed")
            return True

        prev_num_accessible_positions = num_accessible_positions
        # for pos in list(set(accessible_positions).difference(set(checked_positions))):
        for pos in list(accessible_positions.difference(checked_positions)):
            checked_positions.add(pos)
            for i in range(pos[0] - 1, pos[0] + 2):
                for j in range(pos[1] - 1, pos[1] + 2):
                    if (i, j) not in fine_pipe_positions:
                        # accessible_positions.append((i, j))
                        accessible_positions.add((i, j))
        # num_accessible_positions = len(set(accessible_positions))
        num_accessible_positions = len(accessible_positions)
        # print(num_accessible_positions)
        # print(accessible_positions)

    print(f"Position {start_pos} is enclosed")
    enclosed_positions.add(start_pos)
    return True

print('')

# num_enclosed_positions = 0
# for i in range(0, nrows):
#     for j in range(0, ncols):
#         if is_position_enclosed((i, j), pipe_arr):
#             num_enclosed_positions += 1

num_enclosed_positions = 0
fine_enclosed_arr = np.zeros([nrows*3, ncols*3])
# for i in range(0, nrows * 3):
#     for j in range(0, ncols * 3):

non_enclosed_positions = set()
enclosed_positions = set()
# Just need to check the centre of every 3x3 square in the fine grid
for i in range(1, (nrows - 1) * 3, 3):
    print(f"{i} / {(nrows - 1) * 3}")
    for j in range(1, (ncols - 1) * 3, 3):
        # print(f"{i, j}")
        # Skip positions that are pipes (in raw array)
        raw_start_pos = (i // 3, j // 3)
        if pipe_arr[raw_start_pos] == 'X':
            continue

        if is_position_enclosed((i, j), raw_start_pos, fine_pipe_arr, non_enclosed_positions, enclosed_positions):
            num_enclosed_positions += 1
            fine_enclosed_arr[i, j] = 1
        else:
            non_enclosed_positions.add((i, j))

print(f"Total enclosed positions: {fine_enclosed_arr.sum()}")


# Convert back from fine grid to original grid
# enclosed_arr = np.zeros([nrows, ncols])
# for i in range(0, nrows):
#     for j in range(0, ncols):
#         fine_arr_subset = fine_enclosed_arr[i*3: i*3+3, j*3: j*3+3]
#         if fine_arr_subset.min() == 1:
#             enclosed_arr[i, j] = 1


# print(f"Total enclosed positions: {num_enclosed_positions}")
# print(f"Total enclosed positions: {enclosed_arr.sum()}")
print('')
# # For other positions, see if we can get from this position to the edge of the grid
    # dir = get_initial_direction(pos, nrows, ncols)
    # accessible_positions = []
    # curr_pos = pos
    # new_pos = ''
    # dir_history = []
    # while new_pos != pos:
    #     print(curr_pos)
    #     new_pos = get_new_position(curr_pos, dir)
    #     if is_position_on_edge_of_grid(new_pos, nrows, ncols):
    #         print(f"Can reach edge of grid from position {pos}")
    #         return False
    #
    #     if pipe_arr[new_pos] == 'X':
    #         print(f"Pipe in the way at position {pos}; trying another direction")
    #         # Add the direction we've tried to the direction history, and reset the new_pos to try again
    #         dir_history.append(dir)
    #         dir = get_next_direction(dir, dir_history)
    #         new_pos = ''
    #         continue

        # Clear the direction history
    #     dir_history = []
    #     accessible_positions.append(new_pos)
    #     curr_pos = new_pos
    #
    # print(accessible_positions)
    # return True

# accessible_positions = []
# inaccessible_positions = []
#
# start_pos = (6,2)
#
# for i in range(start_pos[0] - 1, start_pos[0] + 2):
#     for j in range(start_pos[1] - 1, start_pos[1] + 2):
#         if (i, j) not in pipe_positions:
#             accessible_positions.append((i, j))
#
# num_accessible_positions = len(set(accessible_positions))
# while num_accessible_positions != num_accessible_positions:
#     # If the edge of the grid is accessible, the start position mustn't be enclosed
#     if len(set(accessible_positions).intersection(edge_positions)) > 0:
#         print(f"Edge of is accessible from starting position {start_pos}")
#         break
#         # return False
#
#     prev_num_accessible_positions = num_accessible_positions
#     for pos in list(set(accessible_positions)):
#         for i in range(pos[0] - 1, pos[0] + 2):
#             for j in range(pos[1] - 1, pos[1] + 2):
#                 if (i, j) not in pipe_positions:
#                     accessible_positions.append((i, j))
#     num_accessible_positions = len(set(accessible_positions))
#     print(num_accessible_positions)
#
# print(f"Position {start_pos} is enclosed")

# while True:
#     acc



# is_position_enclosed((3,3), pipe_arr)



# Initialize
# connections = np.zeroes([5, 5])
# connections = np.empty([nrows, ncols], dtype=object)
# for i in range(0, nrows):
#     for j in range(0, ncols):
#         pipe = data_arr[i, j]
#
#         if pipe == 'S':
#             pipe = start_shape
#
#         if pipe == '.':
#             connections[i, j] = ''
#             continue
#
#         if pipe == '-':
#             connection1 = (i, j+1)
#             connection2 = (i, j-1)
#         if pipe == '|':
#             connection1 = (i+1, j)
#             connection2 = (i-1, j)
#         if pipe == 'L':
#             connection1 = (i-1, j)
#             connection2 = (i, j+1)
#         if pipe == '7':
#             connection1 = (i+1, j)
#             connection2 = (i, j-1)
#         if pipe == 'J':
#             connection1 = (i-1, j)
#             connection2 = (i, j-1)
#         if pipe == 'F':
#             connection1 = (i+1, j)
#             connection2 = (i, j+1)
#
#         if ((connection1[0] < 0) or (connection1[0] >= nrows)
#                 or (connection1[1] < 0) or (connection1[1] >= ncols)):
#             connections[i, j] = ''
#             continue
#         if ((connection2[0] < 0) or (connection2[0] >= nrows)
#                 or (connection2[1] < 0) or (connection2[1] >= ncols)):
#             connections[i, j] = ''
#             continue
#
#         connections[i, j] = (connection1, connection2)
#
#
# prev_pos = start_pos
# curr_pos = connections[prev_pos][0]
# steps = 1
# while curr_pos != start_pos:
#     if connections[curr_pos][0] != prev_pos:
#         prev_pos = curr_pos
#         curr_pos = connections[curr_pos][0]
#     else:
#         prev_pos = curr_pos
#         curr_pos = connections[curr_pos][1]
#     steps += 1
#     print(curr_pos)
#
# print(f"Total steps: {steps}")
# print(f"Max Distance: {steps // 2}")
# # print(total_sum)
# # print(data)




