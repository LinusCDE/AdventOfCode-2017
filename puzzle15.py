log = None
FACTOR_A, FACTOR_B = 16807, 48271

print('Hint: Run this puzzle with \'pypy3\' to get vastly improved '
      'performance.')


def generator(value: int, factor: int):
    '''Generates the values using given 'value' to start and 'factor'.'''
    while True:
        value = (value * factor) % 2147483647
        yield value


def lowest_16_bits(iterateable):
    '''Returns the last 16 bits for each number in 'iterable'.'''
    for number in iterateable:
        bits = bin(number)[2:]
        bits_len = len(bits)

        if bits_len > 16:
            yield bits[bits_len-16:]
        else:
            yield bits


def parse_start_values(puzzle_input):
    '''Parses the start-values from the 'puzzle_input'.
    Optionally the syntax 'NumberA,Number2' is supported.
    '''

    if '\n' in puzzle_input:  # Multiline input:
        line1, line2 = puzzle_input.split('\n')
        start_a, start_b = line1.split()[4], line2.split()[4]
    else:  # Optinal singleline input:
        start_a, start_b = puzzle_input.replace(' ', '').split(',')

    return map(int, (start_a, start_b))  # Returns the startnumbers as ints


def count(bit_gen_a, bit_gen_b, cycles):
    '''Returns how often the judge successfully found fitting last 16 bits.'''
    count = 0  # The count
    output_count = 0  # Count for verbosity-puroses

    for index, bits_a, bits_b in zip(range(cycles),
                                     lowest_16_bits(bit_gen_a),
                                     lowest_16_bits(bit_gen_b)):
        # Print progress every half million cycles:
        output_count += 1
        if output_count > 500000:
            output_count = 0
            log('Progress: %d' % ((index+1) * 100 / cycles) + '%')

        # Pretty shitty comparison of the last 16 bits:
        if len(bits_a) > len(bits_b) and bits_a.endswith(bits_b):
            count += 1
        elif bits_b.endswith(bits_a):
            count += 1

    return count


def solve_part_1(puzzle_input):
    start_a, start_b = parse_start_values(puzzle_input)

    numbers_a = generator(start_a, FACTOR_A)
    numbers_b = generator(start_b, FACTOR_B)

    return count(numbers_a, numbers_b, 40000000)  # 40 Million cycles


def solve_part_2(puzzle_input):
    start_a, start_b = parse_start_values(puzzle_input)

    numbers_a = filter(lambda val: val % 4 == 0, generator(start_a, FACTOR_A))
    numbers_b = filter(lambda val: val % 8 == 0, generator(start_b, FACTOR_B))

    return count(numbers_a, numbers_b, 5000000)  # 5 Million cycles with filter
