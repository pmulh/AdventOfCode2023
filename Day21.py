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
start_pos = (start_pos[0][0], start_pos[1][0]) # Simplify tuple
# q = []


def get_neighbours(full_grid, position):
    available_directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    if position[0] == 0:
        available_directions.remove((-1, 0))
    if position[0] == full_grid.shape[0] - 1:
        available_directions.remove((1, 0))
    if position[1] == 0:
        available_directions.remove((0, -1))
    if position[1] == full_grid.shape[1] - 1:
        available_directions.remove((0, 1))

    neighbours = []
    for direction in available_directions:
        neighbour = (position[0] + direction[0], position[1] + direction[1])

        if full_grid[neighbour] == '#':
            continue

        neighbours.append(neighbour)

    return neighbours


cell_neighbours = {}
nodes = []
for i in range(0, grid.shape[0]):
    for j in range(0, grid.shape[1]):
        nodes.append((i, j))
        cell_neighbours[(i, j)] = get_neighbours(grid, (i, j))


def dijkstra_algorithm(full_grid, nodes_list, neighbour_nodes, start_node):
# def dijkstra_algorithm(graph, start_node, nrows, ncols):
    unvisited_nodes = nodes_list.copy()#list(graph.get_nodes())#*5
    # unvisited_nodes.reverse()

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
    # while unvisited_nodes:
        # current_min_node = None
        # # Start by finding the node with the lowest value (will be (0, 0) initially)
        # for node in unvisited_nodes:  # Iterate over the nodes
        #     if current_min_node is None:
        #         current_min_node = node
        #     elif shortest_path[node] < shortest_path[current_min_node]:
        #         current_min_node = node
        # current_min_node = find_min_node(unvisited_nodes, shortest_path)
        min_dist, current_min_node = heappop(priority_q)

        # The code block below retrieves the current node's neighbors and updates their distances
        neighbours = neighbour_nodes[current_min_node]#, nrows, ncols)#graph.get_outgoing_edges(current_min_node)
        # shuffle(neighbours)
        for neighbour in neighbours:
            # Minimum distance from current_min_node to neighbour
            tentative_value = shortest_path[current_min_node] + 1#full_grid[(neighbour[0], neighbour[1])]#graph.value(current_min_node, neighbour)
            # print(f"tentative value to {neighbour} in direction {direction}: {tentative_value}")
            if tentative_value < shortest_path[neighbour]:
                shortest_path[neighbour] = tentative_value
                # We also update the best path to the current node
                previous_nodes[neighbour] = current_min_node
                heappush(priority_q, (tentative_value, neighbour))

    return previous_nodes, shortest_path


shortest_path_nodes, shortest_path_lengths = dijkstra_algorithm(grid, nodes, cell_neighbours, start_pos)

max_steps = 64
num_possible_final_positions = 0
for node in shortest_path_lengths:
    if (shortest_path_lengths[node] <= max_steps) and (shortest_path_lengths[node] % 2 == 0):
        print(node)
        num_possible_final_positions += 1

print('hi')