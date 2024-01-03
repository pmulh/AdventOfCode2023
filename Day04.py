import re
import string

# with open('Day4SampleInput.txt') as f:
with open('Day4Input.txt') as f:
    data=f.read()

lines = data.split('\n')[:-1]

line_number = 0
total_winnings = 0
for line in lines:
    winning_numbers = set(line.split(': ')[1].split(' | ')[0].split())
    my_numbers = set(line.split(': ')[1].split(' | ')[1].split())
    overlap = winning_numbers.intersection(my_numbers)
    # print(overlap)
    num_matches = len(overlap)
    winnings = int(2 ** (num_matches - 1))
    total_winnings += winnings
    print(f"{line.split(': ')[0]} Winnings = {winnings}")
    # numbers = re.split('\.+', line)
    # Split on non-digits
print(f"Total winnings: {total_winnings}")
print('')
