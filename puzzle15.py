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


def count(bit_gen_a, bit_gen_b):
    count = 0

    for index, gen_a, gen_b in zip(range(40000000), bit_gen_a, bit_gen_b):
        if index % 1000000 == 0:
            print(index)
        if len(gen_a) > len(gen_b) and gen_a.endswith(gen_b):
            count += 1
        elif gen_b.endswith(gen_a):
            count += 1

    return count


def solve_part_1(puzzle_input):
    start_a, start_b = parse_start_values(puzzle_input)

    bit_gen_a = lowest_16_bits(generator(start_a, FACTOR_A))
    bit_gen_b = lowest_16_bits(generator(start_b, FACTOR_B))

    return count(bit_gen_a, bit_gen_b)


def solve_part_2(puzzle_input):
    start_a, start_b = parse_start_values(puzzle_input)

    bit_gen_a = lowest_16_bits(filter(lambda val: val % 4 == 0,
                                      generator(start_a, FACTOR_A)))
    bit_gen_b = lowest_16_bits(filter(lambda val: val % 8 == 0,
                                      generator(start_b, FACTOR_B)))

    return count(bit_gen_a, bit_gen_b)
