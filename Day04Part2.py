import re
import string

# with open('Day4SampleInput.txt') as f:
with open('Day4Input.txt') as f:
    data=f.read()

lines = data.split('\n')[:-1]

# Number of how many of each card we have
card_counts = {i: 1 for i in range(1, len(lines)+1)}
total_winnings = 0
for line in lines:
    card_number = int(line.split(': ')[0].split()[-1])
    winning_numbers = set(line.split(': ')[1].split(' | ')[0].split())
    my_numbers = set(line.split(': ')[1].split(' | ')[1].split())
    overlap = winning_numbers.intersection(my_numbers)
    # print(overlap)
    num_matches = len(overlap)
    print(f"Card {card_number} has {num_matches} matches")

    # Update how many of each card we have
    for i in range(1, num_matches+1):
        if i >= len(lines):
            continue
        # Not just +=1 because we can win multiple cards when we have multiple copies of this card
        card_counts[card_number+i] += card_counts[card_number]
    print(card_counts)

    # winnings = int(2 ** (num_matches - 1))
    # total_winnings += winnings
    # print(f"{line.split(': ')[0]} Winnings = {winnings}")
    # numbers = re.split('\.+', line)
    # Split on non-digits
print(f"Total scratchcards: {sum(card_counts.values())}")
print('')
