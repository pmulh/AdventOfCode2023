import numpy as np
from collections import deque
from heapq import heappush, heappop

# with open('Day23SampleInput.txt') as f:
# with open('Day23SampleInput2.txt') as f:
with open('Day23Input.txt') as f:
    data = f.read()

lines = data.strip('\n').split('\n')
grid = np.array([list(x) for x in data.strip('\n').split('\n')])
print('')


def get_neighbours(full_grid, curr_position, prev_positions):
    x, y = curr_position

    available_directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    if x == 0:
        available_directions.remove((-1, 0))
    if x == full_grid.shape[0] - 1:
        available_directions.remove((1, 0))
    if y == 0:
        available_directions.remove((0, -1))
    if y == full_grid.shape[1] - 1:
        available_directions.remove((0, 1))

    # If current grid is "icy", need to move in direction of arrow
    if full_grid[curr_position] == '>':
        available_directions = [(0, 1)]
    elif full_grid[curr_position] == '<':
        available_directions = [(0, -1)]
    elif full_grid[curr_position] == 'v':
        available_directions = [(1, 0)]
    elif full_grid[curr_position] == '^':
        available_directions = [(-1, 0)]

    neighbours = []
    for direction in available_directions:
        neighbour = (x + direction[0], y + direction[1])
        if full_grid[neighbour] == '#':
            continue

        if neighbour not in prev_positions:
            neighbours.append(neighbour)

    return neighbours


def path_algorithm(grid, start_pos):
    q = [(start_pos, 0)] # list of tuples like (position, index to path so far in paths)
    paths = [[start_pos]]

    while q:
        q_pop = q.pop()
        curr_pos = q_pop[0]
        path_so_far_index = q_pop[1]
        path_so_far = paths[path_so_far_index]
        neighbours = get_neighbours(grid, curr_pos, prev_positions=path_so_far)

        if len(neighbours) < 1:
            continue
        elif len(neighbours) == 1:
            neighbour = neighbours[0]
            q.append((neighbour, path_so_far_index))
            paths[path_so_far_index].append(neighbour)
            continue

        # When there is more than one option, make copies of the path so far
        for neighbour in neighbours:
            new_path_index = len(paths)
            paths.append(path_so_far.copy())
            paths[-1].append(neighbour)
            q.append((neighbour, new_path_index))

    return paths

start_pos = (0, 1)
neighbours = get_neighbours(grid, start_pos, [])
paths = path_algorithm(grid, start_pos)

max_length = 0
for path in paths:
    start_pos = path[0]
    end_pos = path[-1]
    path_length = len(path) - 1
    # if end_pos == (22, 21): # Sample input
    # if end_pos == (140, 139): # Actual input
    if end_pos == (grid.shape[0] - 1, grid.shape[1] - 2):
        print(f"Path starting at {start_pos} ending at {end_pos} has length {path_length}")
        if path_length > max_length:
            max_length = path_length

print(f"Longest path has length {max_length}")

print('')