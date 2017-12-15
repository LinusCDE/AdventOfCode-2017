FACTOR_A, FACTOR_B = 16807, 48271

print('Hint: Run this puzzle with \'pypy3\' about 33% more performance.')


def generator(value: int, factor: int):
    '''Generates the values using given 'value' to start and 'factor'.'''
    while True:
        value = (value * factor) % 2147483647
        yield value


def parse_start_values(puzzle_input):
    '''Parses the start-values from the 'puzzle_input'.
    Optionally the syntax 'NumberA,NumberB' is supported.
    '''

    if '\n' in puzzle_input:  # Multiline input:
        line1, line2 = puzzle_input.split('\n')
        start_a, start_b = line1.split()[4], line2.split()[4]
    else:  # Optinal singleline input:
        start_a, start_b = puzzle_input.replace(' ', '').split(',')

    return map(int, (start_a, start_b))  # Returns the startnumbers as ints


def count(generator_a, generator_b, cycles):
    '''Returns how often the judge successfully found fitting last 16 bits.'''
    count = 0  # The count

    for _, num_a, num_b in zip(range(cycles), generator_a, generator_b):
        if (num_a & 0xFFFF) == (num_b & 0xFFFF):
            count += 1

    return count


def solve_part_1(puzzle_input):
    start_a, start_b = parse_start_values(puzzle_input)

    generator_a = generator(start_a, FACTOR_A)
    generator_b = generator(start_b, FACTOR_B)

    return count(generator_a, generator_b, 40000000)


def solve_part_2(puzzle_input):
    start_a, start_b = parse_start_values(puzzle_input)

    generator_a = filter(lambda val: val % 4 == 0, generator(start_a, FACTOR_A))
    generator_b = filter(lambda val: val % 8 == 0, generator(start_b, FACTOR_B))

    return count(generator_a, generator_b, 5000000)
