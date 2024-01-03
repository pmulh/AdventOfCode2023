with open('Day1Input.txt') as f:
    data=f.read()

lines = data.split('\n')
# print(lines)

def get_first_and_last_digits(text):
    if len(text) < 1:
        return 0

    digits_text = {'one': 1, 'two': 2, 'three': 3, 'four': 4, 'five': 5,
                   'six': 6, 'seven': 7, 'eight': 8, 'nine': 9}

    first_digit = None
    first_digit_idx = None
    i = 0
    for i in range(0, len(text)):
        if text[i].isdigit():
            first_digit = int(text[i])
            first_digit_idx = i
            break

    last_digit = None
    last_digit_idx = None
    i = len(text)
    for i in range(len(text)-1, -1, -1):
        if text[i].isdigit():
            last_digit = int(text[i])
            last_digit_idx = i
            break

    # Check for substrings
    for digit in digits_text.items():
        if digit[0] in text:
            if (first_digit_idx is None) or (text.find(digit[0]) < first_digit_idx):
                first_digit = digit[1]
                first_digit_idx = text.find(digit[0])
            if (last_digit_idx is None) or (text.rfind(digit[0]) > last_digit_idx):
                last_digit = digit[1]
                last_digit_idx = text.rfind(digit[0])

    print(text)
    print(first_digit, last_digit)

    return int(str(first_digit) + str(last_digit))

total = 0
for line in lines:
    # print(line)
    # print(get_first_and_last_digits(line))
    total += get_first_and_last_digits(line)
print(total)