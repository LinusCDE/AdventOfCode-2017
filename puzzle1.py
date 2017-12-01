log = None  # No neccessary. Only for your linter to know about the variable.

# Solutions are correct but can be coded better. Will get done soon.

def solve_part_1(puzzle_input):
    total_sum = 0
    last_digit = int(puzzle_input[0])
    for index in range(1, len(puzzle_input) + 1):
        # Using mod of total puzzle lenght to avoid overflows (will occur)
        digit = int(puzzle_input[index % len(puzzle_input)])
        if digit is last_digit:
            total_sum += digit # Adding digit num if the same
            log('Added %d' % digit)
        last_digit = digit
    return total_sum


def solve_part_2(puzzle_input):
    total_sum = 0
    half = (len(puzzle_input) // 2)
    log('Half: %d' % half)
    for index in range(0, len(puzzle_input)):
        # Using mod of total puzzle lenght to avoid overflows (will occur)
        digit = int(puzzle_input[index % len(puzzle_input)])
        next_digit = int(puzzle_input[(half + index) % len(puzzle_input)])
        if digit is next_digit:
            total_sum += digit  # Adding digit number if they're the same
            log('Found %d and %d' % (digit, next_digit))
        next_digit = digit
    return total_sum
