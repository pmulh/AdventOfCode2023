import re
import string
import numpy as np
from collections import deque
from heapq import heappush, heappop

# with open('Day22SampleInput.txt') as f:
with open('Day22Input.txt') as f:
    data = f.read()

lines = data.strip('\n').split('\n')

# Work out what size of grid we need
max_x, max_y, max_z = 1, 1, 1
bricks = {}
brick_num = 0
for line in lines:
    brick_num += 1
    start, end = line.split('~')
    x0, y0, z0 = [int(i) for i in start.split(',')]
    x1, y1, z1 = [int(i) for i in end.split(',')]
    if max(x0, x1) > max_x:
        max_x = max(x0, x1)
    if max(y0, y1) > max_y:
        max_y = max(y0, y1)
    if max(z0, z1) > max_z:
        max_z = max(z0, z1)

    positions = []
    for x in range(x0, x1+1):
        for y in range(y0, y1+1):
            for z in range(z0, z1+1):
                positions.append((x, y, z))
    bricks[brick_num] = positions
    print('')


grid = np.zeros([max_x+1, max_y+1, max_z+1], dtype=int)
grid_str = grid.astype(int).astype(str)


def update_grid(bricks, grid):
    # Reset everything to 0 (probably better approach, but this will do for now)
    grid[:] = 0
    for brick_num in bricks.keys():
        position_list = bricks[brick_num]
        for position in position_list:
            grid[position] = brick_num
            # grid_str[position] = brick_num
    return grid


def work_out_supports(bricks, grid, calc_supporting_too=False):
    supporting = {}
    supported_by = {}
    for brick_num in bricks.keys():
        positions = bricks[brick_num]
        supporting[brick_num] = set() # []
        supported_by[brick_num] = set() # []
        # Look at layer below to see what's supporting this brick
        # Layer below is one less than minimum z value for brick
        z_below = min([pos[2] for pos in positions]) - 1
        if z_below <= 0:
            # Append 0 to indicate this brick is supported by the ground
            # supported_by[brick_num].append(0)
            supported_by[brick_num].add(0)
        for pos in positions:
            layer_below_pos = (pos[0], pos[1], z_below)
            if (grid[layer_below_pos] != 0) and (grid[layer_below_pos] != brick_num):
                # print(f"Brick {brick_num} supported at position {layer_below_pos}")
                # Append on whatever brick number is supporting this brick
                # supported_by[brick_num].append(grid[layer_below_pos])
                supported_by[brick_num].add(grid[layer_below_pos])
        # # Drop any duplicate values
        # supported_by[brick_num] = list(set(supported_by[brick_num]))

        if not calc_supporting_too:
            continue

        # Look at layer above to see this brick is supporting
        # Layer above is one more than maximum z value for brick
        z_above = max([pos[2] for pos in positions]) + 1
        # if z_above >= grid.shape[2] - 1:
        #     # Append 0 to indicate this brick is at the top of
        #     supported_by[brick_num].append(0)
        for pos in positions:
            layer_above_pos = (pos[0], pos[1], z_above)
            if (grid[layer_above_pos] != 0) and (grid[layer_above_pos] != brick_num):
                # print(f"Brick {brick_num} is supporting brick {grid[layer_above_pos]} at position {layer_above_pos}")
                # Append on whatever brick number is supporting this brick
                # supporting[brick_num].append(grid[layer_above_pos])
                supporting[brick_num].add(grid[layer_above_pos])

    if calc_supporting_too:
        return supported_by, supporting
    return supported_by


def relax_bricks(bricks, supported_by, bricks_that_fall=None):
    for brick_num in bricks.keys():
        # This brick is supported by another, so don't need to do anything at this stage
        if len(supported_by[brick_num]) > 0:
            continue

        # Shift everything down by one layer
        positions = bricks[brick_num]
        new_positions = []
        for pos in positions:
            new_positions.append((pos[0], pos[1], pos[2] - 1))
        bricks[brick_num] = new_positions
        # For Part 2: Track which bricks move during relaxation
        bricks_that_fall.add(brick_num)

    return bricks, bricks_that_fall

bricks_that_fall = set() # Only really used in second part later on
previous_bricks = ''
while bricks != previous_bricks:
    grid = update_grid(bricks, grid)
    supported_by = work_out_supports(bricks, grid)
    previous_bricks = bricks.copy()
    bricks, bricks_that_fall = relax_bricks(bricks, supported_by, bricks_that_fall)

grid = update_grid(bricks, grid)
supported_by, supporting = work_out_supports(bricks, grid, calc_supporting_too=True)

# Work out which bricks can be safely removed
safe_to_remove = []
for brick_num in bricks.keys():
    # Safe to remove if all the bricks this brick is supporting are supported by more than 1 brick
    safe_to_remove_flag = True
    for b in supporting[brick_num]:
        if len(supported_by[b]) > 1:
            safe_to_remove_flag = True
        else:
            safe_to_remove_flag = False
            break

    if safe_to_remove_flag:
        safe_to_remove.append(brick_num)

safe_to_remove = list(set(safe_to_remove))
print(f"Number of bricks that can safely be disintegrated: {len(safe_to_remove)}")

# Removing any of the safe_to_remove bricks will have no effect, so only need to consider the remaining bricks
unsafe_to_remove = [i for i in bricks.keys() if i not in safe_to_remove]


grid_orig = grid.copy()
total_num_bricks_that_would_fall = 0
for removal_brick_num in unsafe_to_remove:
    bricks_minus_1 = bricks.copy()
    del bricks_minus_1[removal_brick_num]
    bricks_that_fall = set()

    previous_bricks = ''
    while bricks_minus_1 != previous_bricks:
        grid = update_grid(bricks_minus_1, grid)
        supported_by = work_out_supports(bricks_minus_1, grid)
        previous_bricks = bricks_minus_1.copy()
        bricks_minus_1, bricks_that_fall = relax_bricks(bricks=bricks_minus_1,
                                                        supported_by=supported_by,
                                                        bricks_that_fall=bricks_that_fall)
    total_num_bricks_that_would_fall += len(bricks_that_fall)
    print(f"Number of bricks that would fall when brick {removal_brick_num} is disintegrated: {len(bricks_that_fall)}")

print(f"Number of bricks that would fall: {total_num_bricks_that_would_fall}")
print('')
