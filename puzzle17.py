print('Hint: Run this puzzle with \'pypy3\' to get improved '
      'performance in part 2.')


def spin(steps, inserts=2018) -> tuple:
    '''Returns the buffer and last index after given
    insertions ('inserts') using given 'steps' to increment.
     '''
    buffer, index = [0], 0
    for inserting in range(1, inserts):
        index = ((index + steps) % inserting) + 1

        # 'list.insert()' inserts after the given index
        # hence the '+ 1'ed index becomes the correct one.
        buffer.insert(index, inserting)
    return buffer, index


def solve_part_1(puzzle_input):
    buffer, index = spin(steps=int(puzzle_input))
    return buffer[(index + 1) % len(buffer)]


def solve_part_2(puzzle_input):
    steps = int(puzzle_input)

    index, result = 0, 0
    # Didn't use 50_000_000 because pypy3 doesn't support underscores (_).
    for inserting in range(1, 50000000):  # Also the current buffer-size
        index = ((index + steps) % inserting) + 1

        if index == 1:  # The zero in buffer will always remain at index 0
            result = inserting

    return result
