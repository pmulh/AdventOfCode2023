import re
import string

# with open('Day3SampleInput.txt') as f:
with open('Day3Input.txt') as f:
    data=f.read()

lines = data.split('\n')[:-1]

# dataarray = []
# for line in lines:
#     dataarray.append(line)
#
# for row in range(0, len(dataarray)):
#     for col in range(0, len(dataarray[0])):
#         val = dataarray[row][col]
#         if val.isnumeric():

line_number = 0
total_sum = 0
for line in lines:
    # numbers = re.split('\.+', line)
    # Split on non-digits
    numbers = re.split('\D+', line)
    for number in numbers:
        if not number.isnumeric():
            continue
        len_num = len(number)
        # num_start_idx = line.find(number)
        # num_start_idx = re.search('[^\d]' + number + '[^\d]', line).start() + 1
        # Negative lookbehind and lookahead assertions to avoid matching e.g. '3' with '233'
        num_start_idx = re.search('(?<![\d])' + number + '(?![\d])', line).start()
        num_end_idx = num_start_idx + len_num - 1
        # Can't let adjacent indexes go beyond length of line
        adj_start_idx = max(num_start_idx-1, 0)
        adj_end_idx = min(num_end_idx+1, len(line)-1)
        # print(line[num_start_idx:num_end_idx])

        adjacent = ''
        if line_number != 0:
            adjacent += lines[line_number - 1][adj_start_idx:adj_end_idx+1]
        if adj_start_idx != num_start_idx:
            adjacent += line[adj_start_idx:num_start_idx]
        if adj_end_idx != num_end_idx:
            adjacent += line[adj_end_idx]
        if line_number != len(lines) - 1:
            adjacent += lines[line_number + 1][adj_start_idx:adj_end_idx+1]

        # print('')
        # print(number)
        # print(f"num_start_idx: {num_start_idx}")
        # print(f"num_end_idx: {num_end_idx}")
        # print(f"adj_start_idx: {adj_start_idx}")
        # print(f"adj_end_idx: {adj_end_idx}")
        # print(adjacent)

        # print(adjacent)
        # [x for x in string.printable if x not in string.digits]
        # string.printable but then removing digits and period
        # nondigits = string.printable[10:].replace('.', '')
        # special characters from string printable, removing period
        # special_chars = string.printable[62:76].replace('.', '')
        # regexp = re.compile(r'[' + nondigits + ']')
        # regexp = re.compile(r'[*+$#]')
        # regexp = re.compile(r'[:]')
        # regexp = re.compile(r'[' + special_chars + ']')
        # Match anything that isn't a period or numeric

        # if number == '3':
        #     print('hi')

        regexp = re.compile(r'[^.0123456789]')
        # if '*' in adjacent:
        #     print(number)
        if regexp.search(adjacent):
            # print(number)
            total_sum += int(number)
        # else:
        #     print(f"{number} doesn't count")

    line_number += 1

print(total_sum)
# print(data)
