import re
import string
import numpy as np
from collections import Counter

# with open('Day7SampleInput.txt') as f:
with open('Day7Input.txt') as f:
    data = f.read()


def classify_hand(hand):
    # Returns a classification and a made up "number of points" per hand

    # Count occurrences of each card in the hand
    counts = Counter(hand)

    if max(counts.values()) == 5:
        return 'FiveOfAKind', 10
    if max(counts.values()) == 4:
        return 'FourOfAKind', 9
    if (max(counts.values()) == 3) and (min(counts.values()) == 2):
        return 'FullHouse', 8
    if (max(counts.values()) == 3) and (min(counts.values()) == 1):
        return 'ThreeOfAKind', 7
    if (max(counts.values()) == 2) and (len(counts.values()) == 3):
        return 'TwoPair', 6
    if (max(counts.values()) == 2) and (len(counts.values()) == 4):
        return 'OnePair', 5
    if len(counts.values()) == 5:
        return 'HighCard', 4

    return 'UnknownHand', 'ERROR'


def reclassify_hand(hand, orig_class, orig_rank):
    # Count occurrences of each card in the hand
    counts = Counter(hand)

    num_jokers = counts['J']
    if num_jokers == 0:
        return orig_class, orig_rank

    if num_jokers == 4:
        if orig_class == 'FourOfAKind':
            return 'FiveOfAKind', 10
    elif num_jokers == 3:
        if orig_class == 'FullHouse':
            return 'FiveOfAKind', 10
        if orig_class == 'ThreeOfAKind':
            return 'FourOfAKind', 9
    elif num_jokers == 2:
        if orig_class == 'FullHouse':
            return 'FiveOfAKind', 10
        if orig_class == 'TwoPair':
            return 'FourOfAKind', 9
        if orig_class == 'OnePair':
            return 'ThreeOfAKind', 7
    elif num_jokers == 1:
        if orig_class == 'FourOfAKind':
            return 'FiveOfAKind', 10
        # if orig_class == 'FullHouse':
        #     return 'FourOfAKind', 9
        if orig_class == 'ThreeOfAKind':
            return 'FourOfAKind', 9
        if orig_class == 'TwoPair':
            return 'FullHouse', 8
        if orig_class == 'OnePair':
            return 'ThreeOfAKind', 7
        if orig_class == 'HighCard':
            return 'OnePair', 5
    return orig_class, orig_rank


def is_hand_stronger_than_other_hand(hand1, hand2):
    # Assumption is that hands are of the same type, so we just need to compare their individual card
    # values to determine the stronger hand
    for card_i in range(0, len(hand1)):
        if hand1[card_i] == hand2[card_i]:
            continue
        if card_ranks[hand1[card_i]] > card_ranks[hand2[card_i]]:
            return True
        if card_ranks[hand2[card_i]] > card_ranks[hand1[card_i]]:
            return False


card_ranks = {'A': 14, 'K': 13, 'Q': 12, 'J': 1, 'T': 10, '9': 9, '8': 8,
              '7': 7, '6': 6, '5': 5, '4': 4, '3': 3, '2': 2}

data = data.split('\n')[:-1]
hands = {}
hands_per_type = {}
hands_per_type['FiveOfAKind'] = []
hands_per_type['FourOfAKind'] = []
hands_per_type['FullHouse'] = []
hands_per_type['ThreeOfAKind'] = []
hands_per_type['TwoPair'] = []
hands_per_type['OnePair'] = []
hands_per_type['HighCard'] = []

for hand_and_bid in data:
    hand, bid = hand_and_bid.split(' ')
    hands[hand] = {}
    hand_type, type_rank = classify_hand(hand)
    hand_type, type_rank = reclassify_hand(hand, hand_type, type_rank)
    hands[hand]['Type'] = hand_type
    hands[hand]['TypeRank'] = type_rank
    hands[hand]['Bid'] = bid

    hands_per_type[hand_type].append(hand)
    # print(hand, bid)

# Rank each hand by comparing it with others in its group, starting with the weakest group and working up
group_base_rank = 1
for hand_type in ['HighCard', 'OnePair', 'TwoPair', 'ThreeOfAKind', 'FullHouse',
                  'FourOfAKind', 'FiveOfAKind']:
    temp_hands = hands_per_type[hand_type]
    if len(temp_hands) < 1:
        continue

    temp_winners = {}
    for i in range(0, len(temp_hands)):
        temp_winners[temp_hands[i]] = 0
        for j in range(0, len(temp_hands)):
            if is_hand_stronger_than_other_hand(temp_hands[i], temp_hands[j]):
                temp_winners[temp_hands[i]] += 1

    # Overall rank is total number of hands in lower type groups + rank within type group
    for hand in temp_hands:
        hands[hand]['Rank'] = group_base_rank + temp_winners[hand]

    group_base_rank = group_base_rank + len(temp_hands)

total_winnings = 0
for hand in hands.values():
    total_winnings += int(hand['Rank']) * int(hand['Bid'])

print(total_winnings)

# print(data)
