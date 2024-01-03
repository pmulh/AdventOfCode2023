import re
import string
import numpy as np
import scipy

# with open('Day15SampleInput.txt') as f:
with open('Day15Input.txt') as f:
    data = f.read()

data = data.strip('\n').split(',')#np.array([list(x) for x in data.strip('\n').split('\n')])

def run_algorithm(input):
    value = 0
    for c in input:
        ascii_val = ord(c)
        value += ascii_val
        value = value * 17
        value = value % 256
    return value

total = 0
for step in data:
    total += run_algorithm(step)

print(total)