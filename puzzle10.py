def shift(elements, shift):
    if shift == 0:
        return  # No work to be done
    for _ in range(abs(shift)):
        if shift < 0:
            elements.append(elements.pop(0))  # Shift leftwards
        else:
            elements.insert(0, elements.pop())  # Shift rightwards


def complex_reverse(elements, index, length):
    shift(elements, -index)  # Move index to 0
    elements[:length] = reversed(elements[:length])
    shift(elements, index)  # Reverse first shift


def solve_part_1(puzzle_input):
    lengths = map(int, puzzle_input.split(','))
    numbers = list(range(256))  # Circular
    skip_size = 0
    current_index = 0
    for length in lengths:
        complex_reverse(numbers, current_index, length)
        current_index += length + skip_size
        skip_size += 1
    return numbers[0] * numbers[1]


def solve_part_2(puzzle_input):
    pass
