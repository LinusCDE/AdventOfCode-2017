log = None
FACTOR_A, FACTOR_B = 16807, 48271


def generator(value, factor):
    while True:
        value = (value * factor) % 2147483647
        yield value


def lowest_16_bits(iterateable):
    for number in iterateable:
        bits = bin(number)[2:]
        bits_len = len(bits)
        if bits_len > 16:
            yield bits[bits_len-16:]
        else:
            yield bits


def parse_start_values(puzzle_input):
    start_a, start_b = -1, -1
    if '\n' in puzzle_input:
        lines = puzzle_input.split('\n')
        start_a, start_b = lines[0].split()[4], lines[1].split()[4]
    else:
        start_a, start_b = puzzle_input.replace(' ', '').split(',')

    return map(int, (start_a, start_b))


def count(bit_gen_a, bit_gen_b, cycles):
    count = 0
    output_count = 0

    for index, gen_a, gen_b in zip(range(cycles),
                                   lowest_16_bits(bit_gen_a),
                                   lowest_16_bits(bit_gen_b)):
        output_count += 1
        if output_count > 500000:
            output_count = 0
            log('Progress: %d' % ((index+1) * 100 / cycles) + '%')
        if len(gen_a) > len(gen_b) and gen_a.endswith(gen_b):
            count += 1
        elif gen_b.endswith(gen_a):
            count += 1

    return count


def solve_part_1(puzzle_input):
    start_a, start_b = parse_start_values(puzzle_input)

    numbers_a = generator(start_a, FACTOR_A)
    numbers_b = generator(start_b, FACTOR_B)

    return count(numbers_a, numbers_b, 40000000)


def solve_part_2(puzzle_input):
    start_a, start_b = parse_start_values(puzzle_input)

    numbers_a = filter(lambda val: val % 4 == 0, generator(start_a, FACTOR_A))
    numbers_b = filter(lambda val: val % 8 == 0, generator(start_b, FACTOR_B))

    return count(numbers_a, numbers_b, 5000000)
