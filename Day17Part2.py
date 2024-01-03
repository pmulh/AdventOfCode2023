import re
import string
import numpy as np
import scipy
import sys
from random import shuffle
from heapq import heappush, heappop

# with open('Day17SampleInputSmall.txt') as f:
# with open('Day17SampleInput2.txt') as f:
# with open('Day17SampleInput.txt') as f:
# with open('Day17SampleInputPart2.txt') as f:
# with open('Day17Part2SampleInput2.txt') as f:
# with open('Day17Part2SampleInput3.txt') as f:
with open('Day17Part2SampleInput4.txt') as f:
# with open('Day17Input.txt') as f:
    data = f.read()

data = np.array([list(x) for x in data.strip('\n').split('\n')])
data = data.astype(int)
data_orig = data.copy()
print('')


# Taken from https://www.udacity.com/blog/2021/10/implementing-dijkstras-algorithm-in-python.html


def get_neighbour_nodes(node, nrows, ncols):
    available_directions = ['N', 'S', 'E', 'W']
    x = node[0]
    y = node[1]
    prev_dir = node[2]
    prev_dir_count = node[3]
    if x == 0:
        available_directions.remove('N')
    if x == nrows - 1:
        available_directions.remove('S')
    if y == 0:
        available_directions.remove('W')
    if y == ncols - 1:
        available_directions.remove('E')

    # Can't end up in the final square with prev_dir_count less than 4
    if y == ncols - 2:
        if (prev_dir == 'E' and prev_dir_count < 3) or (prev_dir != 'E'):
            available_directions.remove('E')
    if x == nrows - 2:
        if (prev_dir == 'S' and prev_dir_count < 3) or (prev_dir != 'S'):
            available_directions.remove('S')

    # You can't go back on yourself
    if prev_dir == 'N':
        if 'S' in available_directions:
            available_directions.remove('S')
    if prev_dir == 'S':
        if 'N' in available_directions:
            available_directions.remove('N')
    if prev_dir == 'E':
        if 'W' in available_directions:
            available_directions.remove('W')
    if prev_dir == 'W':
        if 'E' in available_directions:
            available_directions.remove('E')

    # Number here defines how often you have to turn
    # 1 - you have to change direction after every move
    # 2 - you have to change direction after every 2 moves in a straight line
    # 3 - you have to change direction after every 3 moves in a straight line
    if prev_dir_count >= 10:
        if prev_dir in available_directions:
            available_directions.remove(prev_dir)
    elif prev_dir_count < 4:
        available_directions = [i for i in available_directions if i == prev_dir]

    neighbours = []
    if 'N' in available_directions:
        if prev_dir == 'N':
            new_prev_dir_count = prev_dir_count + 1
        else:
            new_prev_dir_count = 1
        neighbours.append((x-1, y, 'N', new_prev_dir_count))
    if 'S' in available_directions:
        if prev_dir == 'S':
            new_prev_dir_count = prev_dir_count + 1
        else:
            new_prev_dir_count = 1
        neighbours.append((x+1, y, 'S', new_prev_dir_count))
    if 'W' in available_directions:
        if prev_dir == 'W':
            new_prev_dir_count = prev_dir_count + 1
        else:
            new_prev_dir_count = 1
        neighbours.append((x, y-1, 'W', new_prev_dir_count))
    if 'E' in available_directions:
        if prev_dir == 'E':
            new_prev_dir_count = prev_dir_count + 1
        else:
            new_prev_dir_count = 1
        neighbours.append((x, y+1, 'E', new_prev_dir_count))

    # Additional requirement now that cart has to have been travelling in the same direction for at least
    # 4 spaces before it can stop at the end
    # if (x == nrows - 1) and (y == ncols - 1)

    return neighbours


nrows, ncols = data.shape
nodes = []
for i in range(nrows):
    for j in range(ncols):
        for k in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]:
            for direction in ['N', 'S', 'E', 'W']:
                # if i == 0 and direction == 'S':
                #     continue
                # if (k - i) >= 1 and direction == 'S':
                #     # Similar to the condition above, but extended back a move
                #     # e.g.., if we're at the second row, the previous direction is S, and we've apparently moved
                #     # 2 spaces in this direction to get here, we must have start off grid, so this can't be a real node
                #     continue
                # # elif i == 1 and direction == 'S' and k == 2:
                # #     continue
                # # elif i == nrows - 1 and direction == 'N':
                # #     continue
                # elif i >= nrows - k and direction == 'N':
                #     continue
                # # elif j == 0 and direction == 'E':
                # #     continue
                # elif (k - j) >= 1 and direction == 'E':
                #     continue
                # # elif j == ncols - 1 and direction == 'W':
                # #     continue
                # elif j >= ncols - k and direction == 'W':
                #     continue
                #
                # # Additional requirement now that cart has to have been travelling in the same direction for at least
                # # 4 spaces before it can stop at the end
                # if (i == nrows - 1) and (j == ncols - 1):
                #     if k < 4:
                #         continue

                nodes.append((i, j, direction, k))


def find_min_node(unvisited_nodes, shortest_path):
    current_min_node = None
    # Start by finding the node with the lowest value (will be (0, 0) initially)
    for node in unvisited_nodes:  # Iterate over the nodes
        if current_min_node is None:
            current_min_node = node
        elif shortest_path[node] < shortest_path[current_min_node]:
            current_min_node = node
    return current_min_node


def dijkstra_algorithm(data, start_node, end_node_short, nrows, ncols):
# def dijkstra_algorithm(graph, start_node, nrows, ncols):
    unvisited_nodes = nodes.copy()#list(graph.get_nodes())#*5
    unvisited_nodes.reverse()

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
        neighbours = get_neighbour_nodes(current_min_node, nrows, ncols)#graph.get_outgoing_edges(current_min_node)
        # shuffle(neighbours)
        for neighbour in neighbours:
            # Minimum distance from current_min_node to neighbour
            tentative_value = shortest_path[current_min_node] + data[(neighbour[0], neighbour[1])]#graph.value(current_min_node, neighbour)
            # print(f"tentative value to {neighbour} in direction {direction}: {tentative_value}")
            if tentative_value < shortest_path[neighbour]:
                shortest_path[neighbour] = tentative_value
                # We also update the best path to the current node
                previous_nodes[neighbour] = current_min_node
                heappush(priority_q, (tentative_value, neighbour))

        # print(len(priority_q))
        # unvisited_nodes.remove(current_min_node)
        # Optional early stopping
        # if (current_min_node[0] == end_node_short[0]) and (current_min_node[1] == end_node_short[1]):
        #     # print('')
        #     return previous_nodes, shortest_path
        # if len(unvisited_nodes) % 1000 == 0:
        #     print(len(unvisited_nodes))

    return previous_nodes, shortest_path


# start_node = (0, 4, 'E', 4)
start_node = (0, 1, 'E', 1)
end_node_short = (nrows-1, ncols-1)
previous_nodes, shortest_path = dijkstra_algorithm(data, start_node, end_node_short, nrows, ncols)
# previous_nodes, shortest_path = dijkstra_algorithm(graph, start_node, nrows, ncols)

# Add on value of start cells
# start_nodes_value = (data[start_node[0], start_node[1]]
#                      + data[start_node[0], start_node[1] - 1]
#                      + data[start_node[0], start_node[1] - 2]
#                      + data[start_node[0], start_node[1] - 3])
start_nodes_value = data[start_node[0], start_node[1]]
for node in shortest_path.keys():
    shortest_path[node] += start_nodes_value

min_at_end_node = 1e9#abs(sys.maxsize)
for node in shortest_path.keys():
    if (node[0] == nrows-1) and (node[1] == ncols-1):
        print(node, shortest_path[node])
        if abs(shortest_path[node]) < abs(min_at_end_node):
            min_at_end_node = abs(shortest_path[node])
            min_at_end_node_node = node
print(f"Min end node: {min_at_end_node_node} (distance: {min_at_end_node})")

# end_node = (3, 3, 'S', 1)
# node = end_node
# while node != start_node:
#     print(node)
#     node = previous_nodes[node]

# Plot out the path
data_path = data.copy().astype(str)
# for i in range(nrows):
#     for j in range(ncols):
#         data_path[i, j] = ''
end_node = min_at_end_node_node#(12, 12, 'E', 1)
node = end_node
actual_shortest_path = 0
full_path = []
while node != start_node:
    # print(node)
    data_path[node[0], node[1]] = 'X'
    actual_shortest_path += data[node[0], node[1]]
    full_path.append(node)
    # full_path.append((node[0], node[1]))
    node = previous_nodes[node]
data_path[node[0], node[1]] = 'X'
full_path.append(start_node)
full_path.reverse()

import cProfile

print('')

