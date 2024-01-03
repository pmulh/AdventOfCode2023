import re
import string
import numpy as np


# with open('Day6SampleInput.txt') as f:
# with open('Day8SampleInput2.txt') as f:
# with open('Day6Input.txt') as f:
#     data = f.read()

# data = data.split('\n')[:-1]

# Sample Input
# races = {1: {'time_allowed': 7, 'record_distance': 9},
#          2: {'time_allowed': 15, 'record_distance': 40},
#          3: {'time_allowed': 30, 'record_distance': 200}
#          }

# Actual Input
# races = {1: {'time_allowed': 42, 'record_distance': 308},
#          2: {'time_allowed': 89, 'record_distance': 1170},
#          3: {'time_allowed': 91, 'record_distance': 1291},
#          4: {'time_allowed': 89, 'record_distance': 1467}
#          }

# Part 2 Sample:
# races = {1: {'time_allowed': 71530, 'record_distance': 940200}}

# Part 2 Actual:
races = {1: {'time_allowed': 42899189, 'record_distance': 308117012911467}}

total_ways_to_win = 1
for race in races.keys():
    time_allowed = races[race]['time_allowed']#30
    record_distance = races[race]['record_distance']#200

    a = 1
    b = -1 * time_allowed
    c = record_distance + 0.01 # Adding on a little bit to make sure we win and don't just tie with the record

    root1 = (-1 * b + np.sqrt((b**2 - 4 * a * c))) / (2 * a)
    root2 = (-1 * b - np.sqrt((b**2 - 4 * a * c))) / (2 * a)

    solutions = range(int(np.ceil(root2)), int(np.ceil(root1)))
    races[race]['num_ways_to_win'] = len(solutions)
    total_ways_to_win *= len(solutions)

print(total_ways_to_win)
print('')



