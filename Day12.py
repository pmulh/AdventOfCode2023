import re
import string
import numpy as np
import scipy
import itertools
from itertools import permutations, product


with open('Day12SampleInput.txt') as f:
# with open('Day12SampleInput2.txt') as f:
# with open('Day12Input.txt') as f:
    data = f.read()

lines = data.strip('\n').split('\n')
print(lines)

total_count = 0
for line in lines:
    print('#####################')
    print(line)
    springs = line.split(' ')[0]
    block_sizes = [int(x) for x in line.split(' ')[1].split(',')]
    # Part 2: "Unfold" - turn lists into 5 copies of itself
    # springs = (springs + '?') * 4 + springs
    # block_sizes = block_sizes * 5

    # blocks = springs.split('.')
    # blocks = re.split('\.+', springs)
    blocks = [s for s in springs.split('.') if s]
    # print(blocks)

    # for x in itertools.permutations(['.', '#'], 4):


    # Might be able to rule in/out some stuff straight away by looking from the start and end of the line
    # certain_block_idxs = []
    # for i in range(0, len(blocks)):
    #     if '?' not in blocks[i]:
    #         certain_block_idxs.append(i)
    #     else:
    #         break
    # for i in range(len(blocks)-1, -1, -1):
    #     if '?' not in blocks[i]:
    #         certain_block_idxs.append(i)
    #     else:
    #         break

    block_options = {}
    block_size_options_tracker = []
    num_blocks_options_tracker = []
    for block_num in range(0, len(blocks)):#lock in blocks:
        block = blocks[block_num]
        if block == '':
            continue
        if '?' not in block:
            block_options[block_num] = [block]
            continue
        temp = [''.join(list(x)) for x in product(['.','#'], repeat=len(block))]

        options = []
        temp_block_size_tracker = []
        temp_num_blocks_tracker = []
        for option in temp:
            # print(f"block: {block}")
            # print(f"option: {option}")
            possible_option = True
            for i in range(0, len(block)):
                if (block[i] != '?') and (block[i] != option[i]):
                    # break
                    possible_option = False

            if possible_option:
                num_blocks = len([s for s in option.split('.') if s])
                block_lengths = [len(s) for s in option.split('.') if s]

                # Look at what potential options we have to get to this point (e.g., what are the ways the previous
                # blocks could be split that would satisfy the block_sizes requirement?), and see if adding this
                # option on to the end would work with any of these
                if len(block_size_options_tracker) == 0:
                    if block_lengths == block_sizes[:num_blocks]:
                        options.append(option)
                        temp_block_size_tracker.append(block_lengths)
                        temp_num_blocks_tracker.append(num_blocks)
                else:
                    if (min(num_blocks_options_tracker) + num_blocks) <= num_blocks_required:
                        options.append(option)
                        temp_num_blocks_tracker.append(num_blocks)

                    # block_size_options_tracker.extend(block_lengths)
                # else:
                #     for previous_options_sizes in block_size_options_tracker:
                #         if previous_options_sizes.extend(block_lengths) == block_sizes[:len(previous_options_sizes)+num_blocks]:
                #             options.append(option)
                            # block_size_options_tracker.append(previous_options_sizes.extend(block_lengths))

        if len(num_blocks_options_tracker) < 1:
            num_blocks_options_tracker = list(set(temp_num_blocks_tracker))
        else:
            num_blocks_options_tracker = list(set([x+y for x in num_blocks_options_tracker for y in temp_num_blocks_tracker]))
        # if len(block_size_options_tracker) == 0:
            # block_size_options_tracker.

        # print('')
        # block_size_options_tracker.extend()
                # num_blocks = len([s for s in option.split('.') if s])
                # block_lengths = [len(s) for s in option.split('.') if s]
                # if num_blocks > 0:
                #     options.append({})#option)
                #     options[-1]['option'] = option
                #     options[-1]['num_blocks'] = num_blocks
                #     options[-1]['block_lengths'] = block_lengths

        # block_options.append(options)
        block_options[block_num] = options
        # block_options[block_num]['num_blocks'] = len([s for s in option.split('.') if s]

    print('')

    line_options = block_options[0]#[''.join(list(x)) for x in product(block_options[0], block_options[1])]
    for i in range(1, len(block_options)):
        line_options = ['.'.join(list(x)) for x in product(line_options, block_options[i])]

    # Check to see if each option gives the required block sizes
    num_valid_line_options = 0
    num_blocks_required = len(block_sizes)
    for option in line_options:
        blocks = [s for s in option.split('.') if s]
        if len(blocks) != num_blocks_required:
            continue
        if [len(b) for b in blocks] == block_sizes:
            # print(f"{option} is a valid option")
            num_valid_line_options += 1
    print(f"num_valid_line_options: {num_valid_line_options}")

    total_count += num_valid_line_options
    print('')

print(f"Total count: {total_count}")


    # num_options = 0
    # block_sizes_marker = 0
    # for options in block_options:
    #     for option in block_options[options]:
    #         print(f"block_lengths: {option['block_lengths']}")
    #         if option['block_lengths'] == block_sizes[block_sizes_marker:block_sizes_marker+option['num_blocks']]:
    #             print(f"{option} is a valid option")
    #             num_options += 1
    #             block_sizes_marker += option['num_blocks']


    # print()

    # print(num_options)
    # print('')

    #     temp = itertools.permutations(['.', '#'], len(block))
    #     block_permutations = []
    #     for x in temp:
    #         block_permutations.append(''.join([y for y in x]))



        # block_options = []
        # num_question_marks = str.count(block, '?')
        # temp = permutations(['.', '#'], len(block))
        # question_mark_permutations = []
        # for x in temp:
        #     question_mark_permutations.append(''.join([y for y in x]))
        #
        # block_permutations = []
        # for permutation in question_mark_permutations:
        #     block_permutations = ''
            # for i in range(0, len(block)):
                # if i !=
        # for i in range(0, len(question_mark_permutations))
        # if num_question_marks != len(block):
        #     for i in range(0, len(question_mark_permutations)):
        #         for i in range(0, len(block)):


    #     question_mark_permutations = [''.join([x for x in permutations(['.', '#'], 2)])]
    #     print('')
    #     #
    #     # option = ''
    #     # if i in damaged_idxs:
    #     #     option += '#'
    #     # else:
    #     #     option += '.'
    #
    #
    # print('')


