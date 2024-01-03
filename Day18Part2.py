import re
import string
import numpy as np
import scipy
import sys
from random import shuffle

# with open('Day18SampleInput.txt') as f:
# with open('Day18SampleInput2.txt') as f:
with open('Day18Input.txt') as f:
    data = f.read()

lines = data.strip('\n').split('\n')

# max_width = 1
# max_height = 1
metres_in_each_direction = {'R': 0, 'L': 0, 'U': 0, 'D': 0}
required_grid_extents = {'x_min': 0, 'x_max': 0, 'y_min': 0, 'y_max': 0,
                         'x_curr': 0, 'y_curr': 0}
instructions = []
for line in lines:
    temp = line.split(' ')
    # Part 1
    # direction = temp[0]
    # metres = int(temp[1]) #* 2
    # Part 2
    metres = int(temp[2][2:-2], 16) # Converting from hexadecimal
    if temp[2][-2] == '0':
        direction = 'R'
    elif temp[2][-2] == '1':
        direction = 'D'
    elif temp[2][-2] == '2':
        direction = 'L'
    else:
        direction = 'U'
    instructions.append({'direction': direction,
                         'metres': int(metres),
                         'colour': temp[2]})
    metres_in_each_direction[direction] += int(metres)

    # if direction == 'R':
    #     required_grid_extents['x_curr'] += metres
    # elif direction == 'L':
    #     required_grid_extents['x_curr'] -= metres
    # elif direction == 'D':
    #     required_grid_extents['y_curr'] += metres
    # elif direction == 'U':
    #     required_grid_extents['y_curr'] -= metres
    # required_grid_extents['x_min'] = min(required_grid_extents['x_min'], required_grid_extents['x_curr'])
    # required_grid_extents['x_max'] = max(required_grid_extents['x_max'], required_grid_extents['x_curr'])
    # required_grid_extents['y_min'] = min(required_grid_extents['y_min'], required_grid_extents['y_curr'])
    # required_grid_extents['y_max'] = max(required_grid_extents['y_max'], required_grid_extents['y_curr'])

    # if temp[0] == 'R':
    #     max_width += int(temp[1])
    # elif temp[0] == 'L':
    #     max_width -= int(temp[1])
    # elif temp[0] == 'D':
    #     max_height += int(temp[1])
    # elif temp[0] == 'U':
    #     max_height -= int(temp[1])


# max_width = max(metres_in_each_direction['R'], metres_in_each_direction['L']) * 2 + 2
# max_height = max(metres_in_each_direction['U'], metres_in_each_direction['D']) * 2 + 2

# max_width = required_grid_extents['x_max'] - required_grid_extents['x_min'] + 3
# max_height = required_grid_extents['y_max'] - required_grid_extents['y_min'] + 3

# max_width = max(required_grid_extents['x_max'], abs(required_grid_extents['x_min'])) * 2 + 3
# max_height = max(required_grid_extents['y_max'], abs(required_grid_extents['y_min'])) * 2 + 3
#
# grid = np.zeros([max_height, max_width], dtype=np.int8)
# grid_str = grid.copy().astype(int).astype(str)

# Carve out boundary
# boundary_cells = []
boundary_size = 0
# start_pos = (1,1) # For sample input
# start_pos = (max_height // 2, max_width // 2) # For actual input
# start_pos = (-1 * required_grid_extents['x_min'] + 2, -1 * required_grid_extents['y_min'] + 2)
start_pos = (0, 0)
curr_pos = start_pos
vertices = [start_pos]
# boundary_cells.append(curr_pos)
for instruction in instructions:
    curr_i = curr_pos[0]
    curr_j = curr_pos[1]
    direction = instruction['direction']
    metres = instruction['metres']

    # if grid_str[curr_pos] == '>':
    #     if direction == 'U':
    #         grid_str[curr_pos] = 'J'
    #     else: # direction == 'D'
    #         grid_str[curr_pos] = '7'
    # elif grid_str[curr_pos] == '<':
    #     if direction == 'U':
    #         grid_str[curr_pos] = 'L'
    #     else: # direction == 'D'
    #         grid_str[curr_pos] = 'F'
    # elif grid_str[curr_pos] == '^':
    #     if direction == 'R':
    #         grid_str[curr_pos] = 'F'
    #     else: # direction == 'L'
    #         grid_str[curr_pos] = ' 7'
    # elif grid_str[curr_pos] == 'v':
    #     if direction == 'R':
    #         grid_str[curr_pos] = 'L'
    #     else: # direction == 'L'
    #         grid_str[curr_pos] = 'J'

    if direction == 'R':
        # grid_str[curr_i, curr_j+1: curr_j + metres + 1] = '>'#1
        curr_pos = (curr_i, curr_j + metres)
    elif direction == 'L':
        # grid_str[curr_i, curr_j - metres: curr_j] = '<'#1
        curr_pos = (curr_i, curr_j - metres)
    elif direction == 'D':
        # grid_str[curr_i+1: curr_i + metres + 1, curr_j] = 'v'#1
        curr_pos = (curr_i + metres, curr_j)
    elif direction == 'U':
        # grid_str[curr_i - metres: curr_i, curr_j] = '^'#1
        curr_pos = (curr_i - metres, curr_j)

    # if direction == 'R':
    #     # grid_str[curr_i, curr_j: curr_j + metres + 1] = '>'#1
    #     # grid[curr_i, curr_j: curr_j + metres + 1] = 1
    #     curr_pos = (curr_i, curr_j + metres)
    # elif direction == 'L':
    #     # grid_str[curr_i, curr_j - metres: curr_j] = '<'#1
    #     grid[curr_i, curr_j - metres: curr_j] = 1
    #     curr_pos = (curr_i, curr_j - metres)
    # elif direction == 'D':
    #     # grid_str[curr_i: curr_i + metres + 1, curr_j] = 'v'#1
    #     grid[curr_i: curr_i + metres + 1, curr_j] = 1
    #     curr_pos = (curr_i + metres, curr_j)
    # elif direction == 'U':
    #     # grid_str[curr_i - metres: curr_i, curr_j] = '^'#1
    #     grid[curr_i - metres: curr_i, curr_j] = 1
    #     curr_pos = (curr_i - metres, curr_j)

    boundary_size += metres
    vertices.append(curr_pos)

# for i in range(0, grid_str.shape[0]):
#     for j in range(0, grid_str.shape[1]):
#         boundary_cells.append((i, j))

# grid_big = grid.copy()


def flood_fill(full_grid, node, target_num=0, replacement_num=1):
    # Assume node to be inside
    nrow, ncol = full_grid.shape
    x, y = node
    if (x < 0) or (x >= nrow - 1) or (y < 0) or (y >= ncol - 1):
        # print('hi')
        return full_grid

    if full_grid[node] != target_num:
        # print('hello')
        return full_grid

    # print(f'replacing {node}')
    full_grid[node] = replacement_num

    full_grid = flood_fill(full_grid, (x+1, y))
    full_grid = flood_fill(full_grid, (x-1, y))
    full_grid = flood_fill(full_grid, (x, y+1))
    full_grid = flood_fill(full_grid, (x, y-1))
    return full_grid


def iterative_flood_fill(full_grid, node, target_num=0, replacement_num=1):
    # Assume node to be inside
    nrow, ncol = full_grid.shape
    x, y = node
    if (x < 0) or (x >= nrow - 1) or (y < 0) or (y >= ncol - 1):
        # print('hi')
        return #full_grid

    if full_grid[node] != target_num:
        # print('hello')
        return #full_grid

    q = []
    full_grid[node] = replacement_num
    q.append([x, y])

    while len(q) > 0:
        [cur_row, cur_col] = q[0]
        del q[0]

        if full_grid[cur_row - 1, cur_col] == target_num:
            full_grid[cur_row - 1, cur_col] = replacement_num
            q.append([cur_row - 1, cur_col])

        if full_grid[cur_row + 1, cur_col] == target_num:
            full_grid[cur_row + 1, cur_col] = replacement_num
            q.append([cur_row + 1, cur_col])

        if full_grid[cur_row, cur_col - 1] == target_num:
            full_grid[cur_row, cur_col - 1] = replacement_num
            q.append([cur_row, cur_col - 1])

        if full_grid[cur_row, cur_col + 1] == target_num:
            full_grid[cur_row, cur_col + 1] = replacement_num
            q.append([cur_row, cur_col + 1])

# grid_str[(start_pos)] = 'F'

# flood_fill(grid, (12, 15))
# iterative_flood_fill(grid, (12, 15))

# sys.setrecursionlimit(10000)
# grid_copy = grid.copy()

# flood_fill(grid, (max_height // 2 + 1, max_width // 2 + 1))#(876, 941))
# iterative_flood_fill(grid, (max_height // 2 + 1, max_width // 2 + 1))
# print(grid.sum())

# boundary_widths = {}
# for i in range(0, grid.shape[0]):
#     row = ''.join(grid[i].astype(int).astype(str))
#     boundary_blocks = row.replace('0', ' ').split()
#     boundary_blocks_widths = [len(x) for x in boundary_blocks]
#     boundary_widths[i] = boundary_blocks_widths
#
# volume = 0

# Fill in the middle
# interior_cells = []
# grid_orig = grid.copy()
# for i in range(0, grid.shape[0] - 2):
#     if sum(grid[i]) == 0:
#         continue
#     inside = False
#     row_boundary_num = 0
#     boundary_end_j = -1 # Nonsense initialisation value
#     # num_flips_in_current_boundary = 0
# #     one_block_size = 0
#     for j in range(0, grid.shape[1] - 2):
#
#         if grid_str[(i, j)] in ['^', 'v', 'L', 'J']:
#             inside = inside ^ True
#
#         if inside and grid_orig[i, j] == 0:
#             grid[i, j] = 1# 2 for debugging
#
#         # if sum(grid[:, j]) == 0:
#         #     continue
#         # if sum(grid[i, j:]) == 0:
#         #     break
#
#         # print(f"{i=}, {j=}, {grid[i,j]=}, {inside=}, {boundary_end_j=}, {row_boundary_num=}")
#         # print(f"{i=}, {j=}, {grid_str[i,j]=}, {inside=}, {num_flips_in_current_boundary=}")
#         # if (i, j) in boundary_cells and flipped_in_current_boundary:
#         #     continue
#
#         # if grid_orig[i, j] == 1:
#             # inside = inside ^ True
#             # if (not inside) and (grid_orig[i-1, j] == 1) and (grid_orig[i+1, j] == 0):
#             #     inside = inside ^ True
#             # elif inside and (grid_orig[i+1, j] == 1) and (grid_orig[i-1,j] == 0):
#             #     inside = inside ^ True
#         # if (grid_orig[i, j] == 1) and (grid_orig[i, j-1] == 1) and (grid_orig[i+1, j] == 1):
#         #     inside = True
#         # elif (grid_orig[i, j] == 1) and (grid_orig[i, j-1] == 1) and (grid_orig[i-1, j] == 1):
#         #     inside = False
#         # elif grid_orig[i, j] == 1:
#         #     inside = inside ^ True
#
#         # if inside and grid_orig[i, j] == 0:
#         #     grid[i, j] = 2 # 2 for debugging
#
#         # if grid[i, j] == 1 and j == boundary_end_j:
#         #     if grid[i-1, j] == 1:
#         #         # Got to edge of boundary, but boundary moves up afterwards, so need an extra flip
#         #         inside = inside ^ True
#         #         continue
#         # elif grid[i, j] == 1 and j <= boundary_end_j:
#         #     continue
#         # elif inside and grid[i, j] == 0 and j > boundary_end_j:
#         #     grid[i, j] = 2
#         #     if boundary_end_j != -1:
#         #         boundary_end_j = -1
#         #         row_boundary_num += 1
#         #
#         # if grid[i, j] == 1:
#         #     inside = inside ^ True
#         #     boundary_end_j = j + boundary_widths[i][row_boundary_num] - 1
#
#
#
#         # if grid_str[i, j] in ['^', 'v', '<', '>']:
#         #     inside = inside ^ True
#         #     num_flips_in_current_boundary += 1
#
#         # elif grid_str[i, j] in ['>', '<']:
#         #     continue
#         # else:
#         #     flipped_in_current_boundary = False
#         #     if inside:
#         #         grid_str[i, j] = 'x'
#         # if grid_str[i, j] in ['^', 'v']:
#         #     inside = inside ^ True
#         #     flipped_in_current_boundary = True
#         #
#         # elif grid_str[i, j] in ['>', '<']:
#         #     continue
#         # else:
#         #     if inside:
#         #         grid_str[i, j] = 'x'
#                 # interior_cells.append((i, j))
#
# #         # Don't bother looking through the rest of this row if there aren't anymore 1s
# #         if grid[i, j:].sum() == 0:
# #             break
# #         #
# #         # if (not inside) and (grid[i, j] == 0):
# #         #
# #         # if (not inside) and (grid[i, j] == 0) and (grid[i, j+1] == 1):
# #         #     # Work out how big the next block of 1s is going to be
# #         #     for k in range(j, grid.shape[1]):
# #         #         if grid[i, k+1] == 1:
# #         #             one_block_size += 1
# #         #             continue
# #         #         else:
# #         #             if one_block_size % 2 == 1:
# #         #                 inside = True
# #         #             else:
# #         #                 inside = False
# #         #             break
# #
# #         if grid[i, j] == 1:
# #             inside = inside ^ True
#
#         # if grid[i, j] == 1:
#         #     if (grid[i, j] != grid[i, j+1]):# or (grid[i, j] != grid[i, j-1]):
#         #         inside = inside ^ True
#         # else:
#         #     if inside:
#         #         interior_cells.append((i,j))
#         # if grid[i, j] == grid[i, j+1]:
#         #     continue
#
#         # if inside:
#         #     # grid[i, j] = 1 # 2 for debugging
#         #     interior_cells.append((i,j))
#
#         # if grid[i, j] != grid[i, j-1]:
#         #     inside = inside ^ True
#             # Move along a boundary - don't flip the inside flag
#             # if False:#(grid[i, j-1] == 1):# or (grid[i, j+1] == 1):
#             # if grid[i, j+1] == 1:
#             #     continue
#             # else:
#             #     inside = inside ^ True
#                 # if inside:
#                 #     if grid[i, j+1] == 0:
#                 #         inside = inside ^ True # Flip inside between True and False
#                 #         continue
#                 # else:
#                 #     if grid[i, j-1] == 0:
#                 #         inside = inside ^ True
#                 #         continue
#         # if grid[i, j:j+1] == 0:
#         #     inside = False
#         # if sum(grid[i:i+2:, j]) == 0:
#         #     inside = False
#
# # for i in range(0, grid.shape[0]):
# #     for j in range(0, grid.shape[1]):
# #         # if (i, j) in boundary_cells:
# #         #     grid[i, j] = 1
# #         # elif (i, j) in interior_cells:
# #         #     grid[i, j] = 2
# #         if grid_str[i, j] in ['<', '>', 'v', '^', 'J', '7', 'F', 'L']:
# #             grid[i, j] = 1
# #         if grid_str[i, j] == 'x':
# #             grid[i, j] = 2
#
# print(grid.sum())
# internal_size = grid.sum() - boundary_size

print('')

# Using Shoelace formula to get internal area, then adding on some of the boundary size to get the total area (which
# turns out to be using Pick's theorem)
# https://en.wikipedia.org/wiki/Shoelace_formula
# https://en.wikipedia.org/wiki/Pick%27s_theorem

total = 0
for i in range(0, len(vertices)-1):
    determinant = vertices[i][0] * vertices[i+1][1] - vertices[i][1] * vertices[i+1][0]
    total += determinant

internal_area = abs(total) / 2
total_area = internal_area + boundary_size / 2 + 1
print(f"Area = {total_area}")