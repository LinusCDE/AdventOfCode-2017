log = None  # Not neccessary. Only for your linter to know about the variable.


def elm_at(array: list, index: int):
    '''Gets element of a list and prevents overflowing.'''
    return array[index % len(array)]


def solve_part_1(puzzle_input):
    digits = tuple(int(val) for val in puzzle_input)  # As int-tuple
    total_sum = 0
    for index in range(len(puzzle_input)):
        digit, next_digit = digits[index], elm_at(digits, index + 1)
        if digit is next_digit:
            total_sum += digit
            log('+ %d', digit)
    return total_sum


def solve_part_2(puzzle_input):
    digits = tuple(int(val) for val in puzzle_input)  # As int-tuple
    total_sum = 0
    half = len(puzzle_input) // 2
    for index in range(len(puzzle_input)):
        # Using mod of total puzzle lenght to avoid overflows (will occur)
        digit, next_digit = digits[index], elm_at(digits, half + index)
        if digit is next_digit:
            total_sum += digit  # Adding digit number if they're the same
            log('+ %d' % digit)
    return total_sum
