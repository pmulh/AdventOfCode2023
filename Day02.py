# with open('Day2SampleInput.txt') as f:
with open('Day2Input.txt') as f:
    data=f.read()

lines = data.split('\n')

possible_game_count = 0
power_sum = 0
for line in lines:
    colour_counts = {'red': 0, 'green': 0, 'blue': 0}

    if len(line) < 1:
        continue

    game = line.split(': ')[0].split(' ')[-1]
    reveals = line.split(': ')[1].split('; ')
    for reveal in reveals:
        one_ball = reveal.split(', ')
        for ball in one_ball:
            count, colour = ball.split(' ')
            if int(count) > colour_counts[colour]:
                colour_counts[colour] = int(count)
    if (colour_counts['red'] > 12) or (colour_counts['green'] > 13) or (colour_counts['blue'] > 14):
        print(f"Game {game}: Impossible")
    else:
        print(f"Game {game}: Possible")
        possible_game_count += int(game)
    power = colour_counts['red'] * colour_counts['green'] * colour_counts['blue']
    print(f"Game {game}: Power = {power}")
    power_sum += power

# print(colour_counts)
print(possible_game_count)
print(power_sum)