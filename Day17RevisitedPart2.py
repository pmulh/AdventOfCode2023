import numpy as np
from heapq import heappush, heappop

# with open('Day17SampleInput3.txt') as f:
# with open('Day17SampleInputPart2.txt') as f:
with open('Day17Input.txt') as f:
    data = f.read()

lines = data.strip('\n').split('\n')
grid = np.array([list(x) for x in data.strip('\n').split('\n')])
grid = grid.astype(int)
print('')

def get_neighbours(full_grid, curr_state):
    # curr_state is a tuple containing:
    # current row, current column, current direction, number of moves in current direction
    position = (curr_state[0], curr_state[1])
    curr_dir = curr_state[2]
    curr_dir_moves = curr_state[3]

    available_directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]

    if curr_dir_moves >= 10:
        if curr_dir in available_directions:
            available_directions.remove(curr_dir)
    if curr_dir_moves < 4:
        available_directions = [curr_dir]

    # Can't go back on yourself
    opposite_dir = (-1 * curr_dir[0], -1 * curr_dir[1])
    if opposite_dir in available_directions:
        available_directions.remove(opposite_dir)

    if curr_state[0] == 0:
        if (-1, 0) in available_directions:
            available_directions.remove((-1, 0))
    if position[0] == full_grid.shape[0] - 1:
        if (1, 0) in available_directions:
            available_directions.remove((1, 0))
    if position[1] == 0:
        if (0, -1) in available_directions:
            available_directions.remove((0, -1))
    if position[1] == full_grid.shape[1] - 1:
        if (0, 1) in available_directions:
            available_directions.remove((0, 1))

    neighbours = []
    for direction in available_directions:
        if direction == curr_dir:
            new_curr_dir_moves = curr_dir_moves + 1
        else:
            new_curr_dir_moves = 1

        neighbour = (position[0] + direction[0], position[1] + direction[1], # The position part
                     direction, new_curr_dir_moves) # The direction tracking part

        if (neighbour[0], neighbour[1]) == (full_grid.shape[0]-1, full_grid.shape[1]-1):
            if new_curr_dir_moves < 4:
                continue

        neighbours.append(neighbour)


    return neighbours


def dijkstra_algorithm(full_grid, start_node):

    priority_q = [(0, start_node)]

    # For storing the cost of visiting each node (updated we move along the graph)
    shortest_path = {}
    # For storing the shortest known path to a node found so far
    previous_nodes = {}
    # Initialize the starting node's value with 0
    shortest_path[start_node] = 0

    while len(priority_q) > 0:
        min_dist, current_min_node = heappop(priority_q)

        # The code block below retrieves the current node's neighbors and updates their distances
        neighbours = get_neighbours(grid, current_min_node)
        for neighbour in neighbours:
            # Minimum distance from current_min_node to neighbour
            tentative_value = shortest_path[current_min_node] + full_grid[(neighbour[0], neighbour[1])]
            # print(f"tentative value to {neighbour} in direction {direction}: {tentative_value}")
            if (neighbour not in shortest_path.keys()) or (tentative_value < shortest_path[neighbour]):
                shortest_path[neighbour] = tentative_value
                # We also update the best path to the current node
                previous_nodes[neighbour] = current_min_node
                heappush(priority_q, (tentative_value, neighbour))

    return previous_nodes, shortest_path


nrows, ncols = grid.shape
# start_node = (0, 1, (0,1), 1)
# I assumed from the examples that you had to go east initially, which gave slightly too high an answer
# Changing to go south initially gave the correct answer
start_node = (1, 0, (1,0), 1)
shortest_path_nodes, shortest_path_lengths = dijkstra_algorithm(grid, start_node)

# Add on value of start cell
start_nodes_value = grid[start_node[0], start_node[1]]
for node in shortest_path_lengths.keys():
    shortest_path_lengths[node] += start_nodes_value

min_at_end_node = 1e9#abs(sys.maxsize)
for node in shortest_path_nodes.keys():
    if (node[0] == nrows-1) and (node[1] == ncols-1):
        print(node, shortest_path_lengths[node])
        if abs(shortest_path_lengths[node]) < abs(min_at_end_node):
            min_at_end_node = abs(shortest_path_lengths[node])
            min_at_end_node_node = node
print(f"Min end node: {min_at_end_node_node} (distance: {min_at_end_node})")

# Plot out the path
grid_path = grid.copy().astype(str)
end_node = min_at_end_node_node
node = end_node
actual_shortest_path = 0
full_path = []
while node != start_node:
    grid_path[node[0], node[1]] = 'X'
    actual_shortest_path += grid[node[0], node[1]]
    full_path.append(node)
    node = shortest_path_nodes[node]
grid_path[node[0], node[1]] = 'X'
full_path.append(start_node)
full_path.reverse()

print('')