import re
import string
import numpy as np
from collections import deque
from heapq import heappush, heappop

# with open('Day21SampleInput.txt') as f:
# with open('Day20SampleInput2.txt') as f:
with open('Day21Input.txt') as f:
    data = f.read()

lines = data.strip('\n').split('\n')
grid = np.array([list(x) for x in data.strip('\n').split('\n')])
# grid = data.astype(int)
# data_orig = data.copy()
print('')

start_pos = np.where(grid == 'S')
grid[start_pos] = '.'
start_pos = (start_pos[0][0], start_pos[1][0], 0, 0) # Simplify tuple
# replace start position with '.'
# q = []


def map_pos_from_infinite_to_finite_grid(finite_grid, pos):
    nrows, ncols = finite_grid.shape
    row, col, repeat_grid_row, repeat_grid_col = pos

    if row < 0:
        repeat_grid_row -= 1
    elif row > nrows - 1:
        repeat_grid_row += 1

    if col < 0:
        repeat_grid_col -= 1
    elif col > ncols - 1:
        repeat_grid_col += 1

    row = row % nrows
    col = col % ncols

    return row, col, repeat_grid_row, repeat_grid_col


def get_neighbours(full_grid, position, num_grids_needed):
    available_directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    repeat_grid_max = num_grids_needed - 1
    if (position[0] == 0) and (position[2] == -1 * repeat_grid_max):
        available_directions.remove((-1, 0))
    if (position[0] == full_grid.shape[0] - 1) and (position[2] == repeat_grid_max):
        available_directions.remove((1, 0))
    if (position[1] == 0) and (position[3] == -1 * repeat_grid_max):
        available_directions.remove((0, -1))
    if (position[1] == full_grid.shape[1] - 1) and (position[3] == repeat_grid_max):
        available_directions.remove((0, 1))

    neighbours = []
    for direction in available_directions:
        neighbour = (position[0] + direction[0], position[1] + direction[1], position[2], position[3])

        # Loop back onto grid if we've gone "off the edge"
        neighbour = map_pos_from_infinite_to_finite_grid(full_grid, neighbour)
        orig_grid_neighbour_pos = (neighbour[0], neighbour[1])

        if full_grid[orig_grid_neighbour_pos] == '#':
            continue

        neighbours.append(neighbour)

    return neighbours


# Work out how many repeated grids we'll need - assuming walking all the steps in one direction from the start position


# max_steps = 500
num_grids_needed = 0#max(max_steps // grid.shape[0],
                     #  max_steps // grid.shape[1]) + 1
cell_neighbours = {}
nodes = []
# for i in range(0, grid.shape[0]):
#     for j in range(0, grid.shape[1]):
#         for k in range(-num_grids_needed, num_grids_needed):
#             for l in range(-num_grids_needed, num_grids_needed):
#                 nodes.append((i, j, k, l))
#                 cell_neighbours[(i, j, k, l)] = get_neighbours(grid, (i, j, k, l), num_grids_needed)


def dijkstra_algorithm(full_grid, nodes_list, neighbour_nodes, start_node, num_grids_needed, max_allowed_steps):
    unvisited_nodes = nodes_list.copy()

    priority_q = [(0, start_node)]

    # For storing the cost of visiting each node (updated we move along the graph)
    shortest_path = {}
    # For storing the shortest known path to a node found so far
    previous_nodes = {}
    # We'll use max_value to initialize the "infinity" value of the unvisited nodes
    max_value = 1e9#sys.maxsize
    for node in unvisited_nodes:
        shortest_path[node] = max_value
    # However, we initialize the starting node's value with 0
    shortest_path[start_node] = 0

    while len(priority_q) > 0:
        min_dist, current_min_node = heappop(priority_q)
        if min_dist > max_allowed_steps:
            continue

        # The code block below retrieves the current node's neighbors and updates their distances
        neighbours = get_neighbours(grid, current_min_node, num_grids_needed)# neighbour_nodes[current_min_node]#, nrows, ncols)#graph.get_outgoing_edges(current_min_node)
        for neighbour in neighbours:
            # Minimum distance from current_min_node to neighbour
            tentative_value = shortest_path[current_min_node] + 1#full_grid[(neighbour[0], neighbour[1])]#graph.value(current_min_node, neighbour)
            # print(f"tentative value to {neighbour} in direction {direction}: {tentative_value}")
            if (neighbour not in shortest_path.keys()) or (tentative_value < shortest_path[neighbour]):
                shortest_path[neighbour] = tentative_value
                # We also update the best path to the current node
                previous_nodes[neighbour] = current_min_node
                heappush(priority_q, (tentative_value, neighbour))

        # if len(priority_q) % 1000 == 0:
        #     print(len(priority_q))

    return previous_nodes, shortest_path


grid_width = grid.shape[0]
positions_per_max_steps = {}
# Calculate the answer for specific multiples of the grid width, then use those outputs
for max_steps in [grid_width//2, grid_width+grid_width//2, 2*grid_width+grid_width//2,
                  3*grid_width+grid_width//2, 4*grid_width+grid_width//2]:
    shortest_path_nodes, shortest_path_lengths = dijkstra_algorithm(grid, nodes, cell_neighbours, start_pos, num_grids_needed, max_steps)

    num_possible_final_positions = 0
    for node in shortest_path_lengths:
        if (shortest_path_lengths[node] <= max_steps) and (shortest_path_lengths[node] % 2 == max_steps % 2):
            # print(node)
            num_possible_final_positions += 1

    positions_per_max_steps[max_steps] = num_possible_final_positions
    print(f"Total number of possible final positions after {max_steps} steps: {num_possible_final_positions}")

# import matplotlib.pyplot as plt
# plt.plot(list(positions_per_max_steps.keys()), list(positions_per_max_steps.values()))
# plt.plot([x for x in range(0, 1000)], [x**2 for x in range(0,1000)])
# plt.show()
print('')


# x = list(positions_per_max_steps.keys())
# y = list(positions_per_max_steps.values())
# test = {x: y for x,y in zip(positions_per_max_steps.keys(), positions_per_max_steps.values()) if x > 0}
# x = list(test.keys())
# y = list(test.values())
# x = [11,22,33,44]
# y = [63,261,644,1196]
x = [65,196,327,458]
y = [3802, 33732, 93480, 183046]
print(np.polynomial.Polynomial.fit(x, y, deg=2, domain=[], full=False))
# 19.39467397 + 1.72373405·x + 0.86877222·x²

# Apply the formula for 589 steps, and compare with output of dijkstra_algorithm approach above
# num positions = 0.86877222 * 589 ** 2 + 1.72373405 * 589 + 19.39467397 = 302430.00136404
# From dijkstra_algorithm approach: num_positions = 302430
#
# Apply to 26501365 steps to get the answer (needed to round the final answer up to nearest int)
