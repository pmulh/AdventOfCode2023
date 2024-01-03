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
    # Removed for part 2
    # if full_grid[curr_position] == '>':
    #     available_directions = [(0, 1)]
    # elif full_grid[curr_position] == '<':
    #     available_directions = [(0, -1)]
    # elif full_grid[curr_position] == 'v':
    #     available_directions = [(1, 0)]
    # elif full_grid[curr_position] == '^':
    #     available_directions = [(-1, 0)]

    neighbours = []
    for direction in available_directions:
        neighbour = (x + direction[0], y + direction[1])
        if full_grid[neighbour] == '#':
            continue

        if neighbour not in prev_positions:
            neighbours.append(neighbour)

    return neighbours


def get_neighbour_nodes(nodes, curr_position, prev_positions):
    neighbours = list(nodes[curr_position].keys())
    neighbours = [x for x in neighbours if x not in prev_positions]
    return neighbours


nodes = {}
for i in range(0, grid.shape[0]):
    for j in range(0, grid.shape[1]):
        if grid[i, j] == '#':
            continue
        neighbours = get_neighbours(grid, (i, j), [])
        if len(neighbours) > 2:
            nodes[(i, j)] = {}
            # print(len(neighbours))


def path_algorithm(grid, start_pos, nodes):
    q = [(start_pos, 0)] # list of tuples like (position, index to path so far in paths)
    paths = [[start_pos]]
    connected_nodes = []

    while q:
        q_pop = q.pop()
        curr_pos = q_pop[0]

        if curr_pos in nodes.keys() and curr_pos != start_pos:
            connected_nodes.append(curr_pos)
            continue

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

    return paths, connected_nodes


start_pos = (0, 1)
neighbours = get_neighbours(grid, start_pos, [])
paths, connected_nodes = path_algorithm(grid, start_pos, nodes)

nodes[(0,1)] = {}
nodes[(grid.shape[0]-1, grid.shape[1]-2)] = {}
for node in nodes.keys():
    paths, connected_nodes = path_algorithm(grid, node, nodes)
    for connected_node in connected_nodes:
        for path in paths:
            if path[0] == node and path[-1] == connected_node:
                nodes[node][connected_node] = len(path) - 1


def graph_path_algorithm(nodes, start_pos, node_before_final_node):
    q = [(start_pos, 0)] # list of tuples like (position, index to path so far in paths, path length)
    paths = [[start_pos]]

    while q:
        q_pop = q.pop()
        curr_pos = q_pop[0]
        if curr_pos == node_before_final_node:
            continue

        path_so_far_index = q_pop[1]
        # distance_so_far = q_pop[2]
        path_so_far = paths[path_so_far_index]
        neighbours = get_neighbour_nodes(nodes, curr_pos, path_so_far)#list(nodes[curr_pos].keys())#get_neighbours(grid, curr_pos, prev_positions=path_so_far)

        if len(neighbours) < 1:
            continue
        elif len(neighbours) == 1:
            neighbour = neighbours[0]
            q.append((neighbour, path_so_far_index))
            # q.append((neighbour, path_so_far_index, distance_so_far + nodes[curr_pos][neighbour]))
            paths[path_so_far_index].append(neighbour)
            continue

        # When there is more than one option, make copies of the path so far
        for neighbour in neighbours:
            new_path_index = len(paths)
            paths.append(path_so_far.copy())
            paths[-1].append(neighbour)
            q.append((neighbour, new_path_index))
            # q.append((neighbour, new_path_index, distance_so_far + nodes[curr_pos][neighbour]))

    return paths


# node_before_final_node = (19, 19)
node_before_final_node = (123, 125)
paths = graph_path_algorithm(nodes, (0,1), node_before_final_node)

longest_path = 0
for path in paths:
    path_length = 0
    if (path[0] != (0, 1)) or (path[-1] != node_before_final_node):
        continue

    for i in range(0, len(path)-1):
        path_length += nodes[path[i]][path[i+1]]

    if path_length > longest_path:
        longest_path = path_length

# Add on the distance between the 2nd to last and last node
longest_path += nodes[(grid.shape[0]-1, grid.shape[1]-2)][node_before_final_node]

print('')